#!/usr/bin/env python3

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import subprocess
import sys

PROJECT = Path.home() / "Rebecca"
SOURCE = PROJECT / "data" / "memory" / "rebecca.db"
BACKUP_DIR = PROJECT / "backups" / "memory"

REMOTE = "rebecca_drive:Rebecca-Backup/memory"

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

    if age <= timedelta(hours=24):
        return True

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


def sync_to_drive():
    print("Sincronizando memoria con Google Drive...")

    try:
        result = subprocess.run(
            [
                "/usr/bin/rclone",
                "sync",
                str(BACKUP_DIR),
                REMOTE,
                "--verbose",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )

    except FileNotFoundError:
        print("ERROR: no se encontro rclone en /usr/bin/rclone")
        return False

    except subprocess.TimeoutExpired:
        print("ERROR: rclone excedio el tiempo limite de 300 segundos")
        return False

    if result.stdout:
        print(result.stdout.rstrip())

    if result.stderr:
        print(result.stderr.rstrip())

    if result.returncode != 0:
        print(
            f"ERROR: la sincronizacion con Google Drive fallo "
            f"con codigo {result.returncode}"
        )
        return False

    print("Google Drive: sincronizacion completada")
    return True


if __name__ == "__main__":
    create_backup()
    cleanup_backups()

    if not sync_to_drive():
        sys.exit(1)
