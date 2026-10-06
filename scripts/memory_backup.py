#!/usr/bin/env python3

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import sys

PROJECT = Path.home() / "Rebecca"
SOURCE = PROJECT / "data" / "memory" / "rebecca.db"
BACKUP_DIR = PROJECT / "backups" / "memory"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def create_backup():
    if not SOURCE.exists():
        print(f"ERROR: no existe la base de datos: {SOURCE}")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    timestamped = BACKUP_DIR / f"rebecca-{timestamp}.db"
    latest = BACKUP_DIR / "rebecca-latest.db"

    source_db = None
    backup_db = None

    try:
        source_db = sqlite3.connect(SOURCE)
        backup_db = sqlite3.connect(timestamped)

        source_db.backup(backup_db)

        backup_db.close()
        backup_db = None

        source_db.close()
        source_db = None

        check_db = sqlite3.connect(timestamped)

        result = check_db.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        check_db.close()

        if result != "ok":
            timestamped.unlink(missing_ok=True)
            print(f"ERROR: integrity_check devolvio: {result}")
            sys.exit(1)

        shutil.copy2(timestamped, latest)

        print(f"Backup creado: {timestamped}")
        print(f"Backup actualizado: {latest}")
        print("Integrity check: ok")

        return timestamped

    except Exception as error:
        if backup_db is not None:
            backup_db.close()

        if source_db is not None:
            source_db.close()

        timestamped.unlink(missing_ok=True)

        print(f"ERROR durante el backup: {error}")
        sys.exit(1)


def parse_backup_time(path):
    try:
        name = path.stem
        timestamp = name.removeprefix("rebecca-")
        return datetime.strptime(
            timestamp,
            "%Y-%m-%d_%H-%M-%S",
        )
    except ValueError:
        return None


def should_keep(path, now, backups):
    backup_time = parse_backup_time(path)

    if backup_time is None:
        return True

    age = now - backup_time

    # Últimas 24 horas:
    # conservar todas las copias.
    if age <= timedelta(hours=24):
        return True

    # Entre 24 horas y 7 días:
    # conservar una copia por hora.
    if age <= timedelta(days=7):
        same_hour = [
            other
            for other in backups
            if other != path
            and parse_backup_time(other) is not None
            and parse_backup_time(other).replace(
                minute=0,
                second=0,
                microsecond=0,
            )
            == backup_time.replace(
                minute=0,
                second=0,
                microsecond=0,
            )
        ]

        return not any(
            parse_backup_time(other) > backup_time
            for other in same_hour
        )

    # Más de 7 días:
    # conservar una copia diaria.
    same_day = [
        other
        for other in backups
        if other != path
        and parse_backup_time(other) is not None
        and parse_backup_time(other).date()
        == backup_time.date()
    ]

    return not any(
        parse_backup_time(other) > backup_time
        for other in same_day
    )


def cleanup_backups():
    now = datetime.now()

    backups = sorted(
        BACKUP_DIR.glob("rebecca-*.db"),
        key=lambda path: parse_backup_time(path)
        or datetime.min,
        reverse=True,
    )

    for backup in backups:
        if not should_keep(
            backup,
            now,
            backups,
        ):
            backup.unlink(missing_ok=True)
            print(f"Backup antiguo eliminado: {backup}")


if __name__ == "__main__":
    create_backup()
    cleanup_backups()
