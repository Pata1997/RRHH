"""Script para renovar contratos cuya fecha_fin está próxima.
Uso:
  python scripts\auto_renew_contracts.py --days 30 --dry-run

Este script busca contratos con fecha_fin entre hoy y hoy+days.
Crea un nuevo contrato copiando contenido y extendiendo fechas (por la misma duración).
"""
import argparse
from datetime import date, timedelta
from app import create_app
from app.models import db, Contrato
import json


def add_months(d, months):
    # simple month addition (approx)
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, 28)  # keep safe
    return date(year, month, day)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=30, help='Número de días para buscar contratos próximos a vencer')
    parser.add_argument('--dry-run', action='store_true', help='No realiza cambios, solo muestra lo que haría')
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        hoy = date.today()
        limite = hoy + timedelta(days=args.days)
        contratos = Contrato.query.filter(Contrato.fecha_fin != None, Contrato.fecha_fin <= limite).all()
        print(f'Encontrados {len(contratos)} contratos por renovar (fecha_fin <= {limite})')

        for c in contratos:
            print(f' - Contrato {c.numero_contrato} (empleado_id={c.empleado_id}) vence {c.fecha_fin}')
            if args.dry_run:
                continue

            # Intentamos estimar duración en meses
            if c.fecha_inicio and c.fecha_fin:
                diff_days = (c.fecha_fin - c.fecha_inicio).days
                meses = max(1, diff_days // 30)
            else:
                meses = 12

            new_inicio = c.fecha_fin + timedelta(days=1) if c.fecha_fin else hoy
            new_fin = add_months(new_inicio, meses)

            new_num = f"{c.numero_contrato}-R{int(date.today().strftime('%Y%m%d'))}"
            # Intentar regenerar PDF si existen variables
            variables = None
            if c.variables:
                try:
                    variables = json.loads(c.variables)
                except Exception:
                    variables = None

            if variables:
                # actualizar fechas en variables
                new_inicio = c.fecha_fin + timedelta(days=1) if c.fecha_fin else hoy
                meses = variables.get('meses') or meses
                # intentar parsear meses
                try:
                    meses = int(meses)
                except Exception:
                    meses = 12
                new_fin = add_months(new_inicio, meses)
                variables['fecha_inicio'] = new_inicio.strftime('%d/%m/%Y')
                variables['fecha_fin'] = new_fin.strftime('%d/%m/%Y')

                # Regenerar PDF usando la función del app (import dinámico)
                try:
                    from app.routes.rrhh import generar_pdf_contrato
                    pdf_bytes = generar_pdf_contrato(variables)
                except Exception:
                    pdf_bytes = c.contenido

            new_c = Contrato(
                empleado_id=c.empleado_id,
                numero_contrato=new_num,
                tipo_contrato=c.tipo_contrato,
                fecha_inicio=new_inicio,
                fecha_fin=new_fin,
                contenido=pdf_bytes,
                variables=json.dumps(variables) if variables else None
            )
            db.session.add(new_c)
            print(f'   -> Creando renovación {new_num} ({new_inicio} - {new_fin})')
        if not args.dry_run:
            db.session.commit()
            print('Renovaciones guardadas en la base de datos.')

if __name__ == '__main__':
    main()
