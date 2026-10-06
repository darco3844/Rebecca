#!/usr/bin/env python3

import sqlite3
from datetime import datetime
from pathlib import Path
import shutil
import sys

PROJECT = Path.home() / "Rebecca"
SOURCE = PROJECT / "data" / "memory" / "rebecca.db"
BACKUP_DIR = PROJECT / "backups" / "memory"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

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
