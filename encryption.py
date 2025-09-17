"""Utilities for encrypting and decrypting sensitive values."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken


class EncryptionKeyMissingError(RuntimeError):
    """Raised when the Fernet key is not configured."""


class DecryptionError(RuntimeError):
    """Raised when a value cannot be decrypted."""


def _load_key() -> bytes:
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise EncryptionKeyMissingError(
            "Environment variable ENCRYPTION_KEY must be set with a valid Fernet key."
        )
    if isinstance(key, str):
        key_bytes = key.encode("utf-8")
    else:
        key_bytes = key
    return key_bytes


@lru_cache(maxsize=1)
def _get_cipher() -> Fernet:
    return Fernet(_load_key())


def encrypt_api_key(api_key: Optional[str]) -> Optional[str]:
    """Encrypt a plain API key using the configured Fernet cipher."""
    if api_key is None:
        return None
    cipher = _get_cipher()
    encrypted = cipher.encrypt(api_key.encode("utf-8"))
    return encrypted.decode("utf-8")


def decrypt_api_key(encrypted_api_key: Optional[str]) -> Optional[str]:
    """Decrypt an API key previously encrypted with :func:`encrypt_api_key`."""
    if encrypted_api_key is None:
        return None
    cipher = _get_cipher()
    try:
        decrypted = cipher.decrypt(encrypted_api_key.encode("utf-8"))
    except InvalidToken as exc:  # pragma: no cover - specific to cryptography internals
        raise DecryptionError("Failed to decrypt API key.") from exc
    return decrypted.decode("utf-8")


def is_encrypted_api_key(value: Optional[str]) -> bool:
    """Best-effort check whether the provided value is already encrypted."""
    if not value:
        return False
    try:
        decrypt_api_key(value)
    except DecryptionError:
        return False
    return True
