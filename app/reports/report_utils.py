from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import io
import os
from decimal import Decimal

def formato_guaranies(valor):
    """Formatea números con separador de miles para guaraníes paraguayos
    Ejemplos: 1000 -> 1.000 | 1000000 -> 1.000.000
    """
    try:
        if valor is None:
            return '0'
        numero = float(valor)
        # Formatear con separador de miles usando punto
        return '{:,.0f}'.format(numero).replace(',', '.')
    except (ValueError, TypeError):
        return str(valor)

def crear_membrete_empresa(empresa, styles):
    """
    Crea el membrete empresarial con logo para los reportes PDF
    
    Args:
        empresa: Objeto Empresa con los datos
        styles: Estilos de ReportLab
        
    Returns:
        Lista de elementos para agregar al story
    """
    elementos = []
    
    # Datos de la empresa
    empresa_data = []
    
    # Si hay logo, incluirlo
    if empresa and empresa.logo_path:
        try:
            # Construir ruta absoluta al logo
            from flask import current_app
            # logo_path ya incluye "empresa/logo_123.png"
            logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], empresa.logo_path)
            
            if os.path.exists(logo_path):
                # Crear imagen con tamaño proporcional
                img = Image(logo_path)
                img._restrictSize(2*inch, 1*inch)  # Max 2x1 pulgadas
                
                # Información de la empresa
                empresa_info = []
                if empresa.nombre:
                    empresa_info.append(Paragraph(f"<b>{empresa.nombre}</b>", styles['Normal']))
                if empresa.ruc:
                    empresa_info.append(Paragraph(f"RUC: {empresa.ruc}", styles['Normal']))
                if empresa.direccion:
                    direccion_completa = empresa.direccion
                    if empresa.ciudad:
                        direccion_completa += f" - {empresa.ciudad}"
                    empresa_info.append(Paragraph(direccion_completa, styles['Normal']))
                if empresa.telefono or empresa.email:
                    contacto = []
                    if empresa.telefono:
                        contacto.append(f"Tel: {empresa.telefono}")
                    if empresa.email:
                        contacto.append(f"Email: {empresa.email}")
                    empresa_info.append(Paragraph(" | ".join(contacto), styles['Normal']))
                
                # Crear tabla con logo e información
                membrete_data = [[img, empresa_info]]
                membrete_table = Table(membrete_data, colWidths=[2*inch, 5.5*inch])
                membrete_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                
                elementos.append(membrete_table)
                elementos.append(Spacer(1, 0.2*inch))
                
                # Línea separadora
                line_data = [['', '']]
                line_table = Table(line_data, colWidths=[7.5*inch])
                line_table.setStyle(TableStyle([
                    ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#003366')),
                ]))
                elementos.append(line_table)
                elementos.append(Spacer(1, 0.15*inch))
                
                return elementos
        except Exception as e:
            print(f"Error al cargar logo en PDF: {e}")
            # Continuar sin logo
    
    # Si no hay logo o hubo error, usar membrete de texto simple
    if empresa and empresa.nombre:
        empresa_style = ParagraphStyle(
            'EmpresaStyle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=3,
        )
        
        elementos.append(Paragraph(f"<b>{empresa.nombre}</b>", empresa_style))
        
        if empresa.ruc:
            elementos.append(Paragraph(f"RUC: {empresa.ruc}", empresa_style))
        
        if empresa.direccion:
            direccion_completa = empresa.direccion
            if empresa.ciudad:
                direccion_completa += f" - {empresa.ciudad}"
            elementos.append(Paragraph(direccion_completa, empresa_style))
        
        if empresa.telefono or empresa.email:
            contacto = []
            if empresa.telefono:
                contacto.append(f"Tel: {empresa.telefono}")
            if empresa.email:
                contacto.append(f"Email: {empresa.email}")
            elementos.append(Paragraph(" | ".join(contacto), empresa_style))
        
        elementos.append(Spacer(1, 0.2*inch))
        
        # Línea separadora
        line_data = [['', '']]
        line_table = Table(line_data, colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#003366')),
        ]))
        elementos.append(line_table)
        elementos.append(Spacer(1, 0.15*inch))
    
    return elementos

class ReportUtils:
    """Utilidades para generar reportes PDF con ReportLab"""
    
    @staticmethod
    def generar_recibo_salario(empleado, liquidacion, empresa=None):
        """
        Genera un recibo de salario en PDF
        
        Args:
            empleado: Objeto Empleado
            liquidacion: Objeto Liquidacion
            empresa: Objeto Empresa (opcional, para membrete)
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Membrete con logo de empresa
        if empresa:
            story.extend(crear_membrete_empresa(empresa, styles))
        
        # Encabezado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("RECIBO DE SALARIO", title_style))
        story.append(Spacer(1, 0.15*inch))
        
        # Información general
        info_data = [
            ['Periodo:', liquidacion.periodo, 'Fecha de Emisión:', datetime.now().strftime('%d/%m/%Y')],
            ['Empleado:', empleado.nombre_completo, 'Código:', empleado.codigo],
            ['CI:', empleado.ci, 'Cargo:', empleado.cargo.nombre],
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Detalles de liquidación
        bonif_familiar = liquidacion.bonificacion_familiar or Decimal('0')
        subtotal_ingresos = liquidacion.salario_base + liquidacion.ingresos_extras + bonif_familiar
        total_descuentos = liquidacion.descuentos + liquidacion.aporte_ips
        
        detail_data = [
            ['CONCEPTO', 'VALOR'],
            ['Salario Base', f"₲ {formato_guaranies(liquidacion.salario_base)}"],
            ['Ingresos Extras', f"₲ {formato_guaranies(liquidacion.ingresos_extras)}"],
            ['Bonificación Familiar', f"₲ {formato_guaranies(bonif_familiar)}"],
            ['Subtotal Ingresos', f"₲ {formato_guaranies(subtotal_ingresos)}"],
            ['', ''],
        ]
        
        # Agregar desglose de descuentos si existen
        descuento_ausencias = liquidacion.descuento_ausencias or Decimal('0')
        descuento_anticipos = liquidacion.descuento_anticipos or Decimal('0')
        descuento_sanciones = liquidacion.descuento_sanciones or Decimal('0')
        descuento_otros = liquidacion.descuento_otros or Decimal('0')
        
        if descuento_ausencias > 0:
            detail_data.append(['  - Descuento por Ausencias', f"₲ {formato_guaranies(descuento_ausencias)}"])
        if descuento_anticipos > 0:
            detail_data.append(['  - Descuento por Anticipos', f"₲ {formato_guaranies(descuento_anticipos)}"])
        if descuento_sanciones > 0:
            detail_data.append(['  - Descuento por Sanciones', f"₲ {formato_guaranies(descuento_sanciones)}"])
        if descuento_otros > 0:
            detail_data.append(['  - Otros Descuentos', f"₲ {formato_guaranies(descuento_otros)}"])
        
        # Si hubo descuentos, mostrar el total
        if liquidacion.descuentos > 0:
            detail_data.append(['Total Descuentos', f"₲ {formato_guaranies(liquidacion.descuentos)}"])
        
        detail_data.extend([
            ['Aporte IPS (9.625%)', f"₲ {formato_guaranies(liquidacion.aporte_ips)}"],
            ['Total a Descontar', f"₲ {formato_guaranies(total_descuentos)}"],
            ['', ''],
            ['SALARIO NETO', f"₲ {formato_guaranies(liquidacion.salario_neto)}"],
        ])
        
        detail_table = Table(detail_data, colWidths=[4*inch, 2*inch])
        detail_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(detail_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Nota
        note_style = ParagraphStyle(
            'Note',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Este recibo fue generado automáticamente por el sistema de RRHH", note_style))
        story.append(Paragraph(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", note_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_planilla_mensual(empleados_liquidaciones, periodo, empresa=None):
        """
        Genera planilla consolidada mensual
        
        Args:
            empleados_liquidaciones: Lista de tuplas (empleado, liquidacion)
            periodo: String con formato YYYY-MM
            empresa: Objeto Empresa (opcional, para membrete)
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.3*inch, leftMargin=0.3*inch,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Membrete con logo de empresa
        if empresa:
            story.extend(crear_membrete_empresa(empresa, styles))
        
        # Encabezado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("PLANILLA DE LIQUIDACIÓN DE SALARIOS", title_style))
        story.append(Paragraph(f"Período: {periodo}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Tabla de datos
        data = [['Código', 'Empleado', 'Cargo', 'Salario Base', 'Ingresos', 'Bonif. Fam.', 'Descuentos', 'IPS', 'Neto']]
        
        total_salario_base = Decimal('0')
        total_ingresos = Decimal('0')
        total_bonif_fam = Decimal('0')
        total_descuentos = Decimal('0')
        total_ips = Decimal('0')
        total_neto = Decimal('0')
        
        for empleado, liquidacion in empleados_liquidaciones:
            bonif_fam = liquidacion.bonificacion_familiar or Decimal('0')
            data.append([
                empleado.codigo,
                empleado.nombre_completo,
                empleado.cargo.nombre,
                f"₲ {float(liquidacion.salario_base):,.0f}",
                f"₲ {float(liquidacion.ingresos_extras):,.0f}",
                f"₲ {float(bonif_fam):,.0f}",
                f"₲ {float(liquidacion.descuentos):,.0f}",
                f"₲ {float(liquidacion.aporte_ips):,.0f}",
                f"₲ {float(liquidacion.salario_neto):,.0f}",
            ])
            
            total_salario_base += liquidacion.salario_base
            total_ingresos += liquidacion.ingresos_extras
            total_bonif_fam += bonif_fam
            total_descuentos += liquidacion.descuentos
            total_ips += liquidacion.aporte_ips
            total_neto += liquidacion.salario_neto
        
        # Fila de totales
        data.append([
            '',
            'TOTAL',
            '',
            f"₲ {float(total_salario_base):,.0f}",
            f"₲ {float(total_ingresos):,.0f}",
            f"₲ {float(total_bonif_fam):,.0f}",
            f"₲ {float(total_descuentos):,.0f}",
            f"₲ {float(total_ips):,.0f}",
            f"₲ {float(total_neto):,.0f}",
        ])
        
        table = Table(data, colWidths=[0.6*inch, 1.8*inch, 1.2*inch, 0.9*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
            ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Resumen
        note_style = ParagraphStyle(
            'Note',
            parent=styles['Normal'],
            fontSize=7,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", note_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_contrato_pdf(empleado, cargo, fecha_inicio, fecha_fin=None, empresa=None):
        """
        Genera un contrato de trabajo en PDF
        
        Args:
            empleado: Objeto Empleado
            cargo: Objeto Cargo
            fecha_inicio: fecha de inicio del contrato
            fecha_fin: fecha de fin del contrato (opcional)
            empresa: Objeto Empresa (opcional, para membrete)
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Membrete con logo de empresa
        if empresa:
            story.extend(crear_membrete_empresa(empresa, styles))
        
        # Encabezado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("CONTRATO DE TRABAJO", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Cuerpo del contrato
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        fecha_inicio_str = fecha_inicio.strftime('%d de %B de %Y') if hasattr(fecha_inicio, 'strftime') else str(fecha_inicio)
        
        contenido = f"""
        <b>ENTRE:</b><br/>
        El suscrito COOPERATIVA RRHH, por una parte, y {empleado.nombre_completo}, 
        portador de Cédula de Identidad Nº {empleado.ci}, mayor de edad, capaz según la ley, 
        por la otra parte, acuerdan celebrar el presente Contrato de Trabajo bajo los siguientes términos:<br/><br/>
        
        <b>PRIMERO:</b> El empleador contrata al trabajador para que desempeñe las funciones 
        correspondientes al cargo de {cargo.nombre}, con un salario base de ₲ {float(cargo.salario_base):,.2f} mensual.<br/><br/>
        
        <b>SEGUNDO:</b> El presente contrato comenzará a regir desde el {fecha_inicio_str} 
        y durará por tiempo indeterminado, salvo disposición contraria de ambas partes.<br/><br/>
        
        <b>TERCERO:</b> El trabajador se compromete a cumplir con sus obligaciones laborales, 
        acatar la disciplina de la empresa y respetar las normas internas de convivencia.<br/><br/>
        
        <b>CUARTO:</b> El empleador se obliga a pagar el salario en la forma y oportunidad establecida 
        en la ley, así como proporcionar las condiciones de seguridad e higiene en el trabajo.<br/><br/>
        
        Firmado en la ciudad de Asunción, a los {datetime.now().strftime('%d')} días del mes de {datetime.now().strftime('%B')} de {datetime.now().strftime('%Y')}.<br/>
        """
        
        story.append(Paragraph(contenido, body_style))
        story.append(Spacer(1, 0.4*inch))
        
        # Firmas
        firma_style = ParagraphStyle(
            'FirmaStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        story.append(Paragraph("_________________________", firma_style))
        story.append(Paragraph("Empleador", firma_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("_________________________", firma_style))
        story.append(Paragraph(f"{empleado.nombre_completo}", firma_style))
        story.append(Paragraph("Trabajador", firma_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
