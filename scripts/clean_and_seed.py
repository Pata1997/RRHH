"""scripts/clean_and_seed.py
Utility to inspect and optionally clean historical HR tables and remove files from uploads/ and instance/.

Usage examples (PowerShell):
    # Dry-run: shows counts and files that WOULD be deleted
    python scripts\clean_and_seed.py --dry-run

    # Apply DB cleanup and delete files (requires --yes to confirm)
    python scripts\clean_and_seed.py --apply-clean --delete-files --yes

This script is intentionally conservative: by default it only reports. You must pass
--apply-clean to change the DB and --yes to confirm destructive file deletions.

It targets these tables: Asistencia, Permiso, Sancion, Vacacion, Liquidacion, IngresoExtra, Descuento
It will NOT touch empleados, cargos, contratos.

Make a backup before running destructive operations!
"""

import argparse
import os
import shutil
from datetime import date

from app import create_app
from app.models import db, Asistencia, Permiso, Sancion, Vacacion, Liquidacion, IngresoExtra, Descuento
from sqlalchemy import func

TARGET_TABLES = [
    (Asistencia, 'asistencias'),
    (Permiso, 'permisos'),
    (Sancion, 'sanciones'),
    (Vacacion, 'vacaciones'),
    (Liquidacion, 'liquidaciones'),
    (IngresoExtra, 'ingresos_extras'),
    (Descuento, 'descuentos'),
]

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'uploads')
INSTANCE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
BACKUP_SUGGESTION = "Please create a DB backup (pg_dump) and copy of uploads/ and instance/ before applying changes."


def human_count(n):
    try:
        return int(n)
    except Exception:
        return n


def gather_counts(app):
    results = {}
    with app.app_context():
        for model, name in TARGET_TABLES:
            try:
                cnt = db.session.query(func.count(model.id)).scalar()
            except Exception:
                # fallback: try model.query.count()
                try:
                    cnt = model.query.count()
                except Exception:
                    cnt = 'ERROR'
            results[name] = human_count(cnt)
    return results


def perform_db_cleanup(app, dry_run=True):
    counts = gather_counts(app)
    print('\nDB table counts (current):')
    for name, cnt in counts.items():
        print(f'  - {name}: {cnt}')

    if dry_run:
        print('\nDry-run: nothing will be deleted. Use --apply-clean --yes to actually remove data.')
        return counts

    # Actual deletion
    with app.app_context():
        print('\nApplying DB cleanup...')
        for model, name in TARGET_TABLES:
            print(f'  Deleting rows from {name}...')
            try:
                deleted = db.session.query(model).delete()
                print(f'    deleted: {deleted} rows')
            except Exception as e:
                print(f'    ERROR deleting from {name}: {e}')
        db.session.commit()
        print('DB cleanup committed.')

    return counts


def list_files_to_delete(base_dirs):
    files = []
    for base in base_dirs:
        if not os.path.exists(base):
            continue
        for root, dirs, filenames in os.walk(base):
            for fn in filenames:
                files.append(os.path.join(root, fn))
    return files


def perform_file_cleanup(base_dirs, dry_run=True):
    files = list_files_to_delete(base_dirs)
    print('\nFiles found to delete:')
    for f in files:
        print('  -', f)
    if dry_run:
        print('\nDry-run: files not deleted. Use --delete-files --yes to actually remove.')
        return files

    print('\nDeleting files...')
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f'  ERROR deleting {f}: {e}')

    # Remove empty directories under each base
    for base in base_dirs:
        for root, dirs, filenames in os.walk(base, topdown=False):
            try:
                if not os.listdir(root):
                    os.rmdir(root)
            except Exception:
                pass
    print('File cleanup completed.')
    return files


def main():
    parser = argparse.ArgumentParser(description='Clean historical HR tables and optionally delete uploads/instance files.')
    parser.add_argument('--dry-run', action='store_true', help='Only show what would be done (default)')
    parser.add_argument('--apply-clean', action='store_true', help='Apply DB cleanup (destructive)')
    parser.add_argument('--delete-files', action='store_true', help='Delete files under uploads/ and instance/ (destructive)')
    parser.add_argument('--yes', action='store_true', help='Confirm destructive operations (required with --apply-clean or --delete-files)')
    parser.add_argument('--seed', action='store_true', help='(Optional) seed simple asistencias from today to month-end after cleanup')
    parser.add_argument('--employees', default='all', help='Comma-separated employee IDs or "all" (default)')
    args = parser.parse_args()

    # Default behavior: dry-run if no destructive flags
    if not args.apply_clean and not args.delete_files and not args.seed:
        args.dry_run = True

    if (args.apply_clean or args.delete_files) and not args.yes:
        print('\nRefusing to run destructive operation without --yes.')
        print(BACKUP_SUGGESTION)
        print('If you have a backup and understand the consequences, re-run with --yes.')
        return

    # Create app
    app = create_app('development')

    # Dry-run or apply DB cleanup
    if args.apply_clean:
        perform_db_cleanup(app, dry_run=False)
    else:
        perform_db_cleanup(app, dry_run=True)

    # Files
    base_dirs = [UPLOADS_DIR, INSTANCE_DIR]
    if args.delete_files:
        perform_file_cleanup(base_dirs, dry_run=False)
    else:
        perform_file_cleanup(base_dirs, dry_run=True)

    # Optional seed: create asistencias from today to month end
    if args.seed:
        if args.apply_clean is False:
            print('\nWarning: you are seeding without --apply-clean. That may mix with old data.')
        # parse employees
        emp_list = []
        if args.employees.strip().lower() == 'all':
            with app.app_context():
                from app.models import Empleado
                emp_list = [e.id for e in Empleado.query.all()]
        else:
            emp_list = [int(x) for x in args.employees.split(',') if x.strip()]

        if not emp_list:
            print('No employees found to seed.')
            return

        print('\nSeeding asistencias from today until month-end for employees:', emp_list)
        from calendar import monthrange
        today = date.today()
        year = today.year
        month = today.month
        last_day = monthrange(year, month)[1]
        days = [date(year, month, d) for d in range(today.day, last_day + 1)]

        with app.app_context():
            created = 0
            for emp in emp_list:
                for d in days:
                    # simple rule: weekdays -> presente
                    if d.weekday() < 5:
                        a = Asistencia(empleado_id=emp, fecha=d, presente=True)
                        db.session.add(a)
                        created += 1
            db.session.commit()
            print(f'Created {created} asistencia records.')

    print('\nDone.')


if __name__ == '__main__':
    main()
