"""Migration script to encrypt existing API keys stored in plaintext."""
from __future__ import annotations

import logging
from typing import Tuple

from sqlalchemy.orm import Session

from db import SessionLocal
from encryption import DecryptionError, EncryptionKeyMissingError
from models import User

logger = logging.getLogger(__name__)


def _process_user(user: User, session: Session) -> bool:
    stored_value = user.api_key_encrypted
    if not stored_value:
        return False
    try:
        # If decryption succeeds, the value is already encrypted with the active key.
        _ = user.api_key  # Access triggers decryption.
        return False
    except DecryptionError:
        # Value is likely stored in plaintext, so re-encrypt it using the helper.
        user.set_api_key(stored_value)
        session.add(user)
        return True


def migrate() -> Tuple[int, int]:
    """Encrypt plaintext API keys for all users.

    Returns a tuple with the number of processed users and how many of them were updated.
    """
    processed = 0
    updated = 0
    with SessionLocal() as session:
        users = session.query(User).all()
        for user in users:
            processed += 1
            if _process_user(user, session):
                updated += 1
        session.commit()
    return processed, updated


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    try:
        processed, updated = migrate()
    except EncryptionKeyMissingError as exc:
        logger.error("Не удалось выполнить миграцию: %s", exc)
        raise SystemExit(1) from exc
    logger.info("Миграция завершена. Обработано пользователей: %s, обновлено: %s", processed, updated)


if __name__ == "__main__":
    main()
