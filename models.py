#models.py
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

from config import DATABASE_URL
from encryption import decrypt_api_key, encrypt_api_key

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    _api_key_encrypted = Column("api_key", String(250), nullable=True)
    model_id = Column(String(250), nullable=True)  # Поле для хранения выбранной модели
    max_tokens = Column(Integer, nullable=True)  # Поле для хранения max_tokens
    is_valid = Column(Boolean, default=True)  # Добавленное поле для индикации валидности API ключа

    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")

    def set_api_key(self, api_key: Optional[str]) -> None:
        """Store the provided API key in encrypted form."""
        if api_key is None:
            self._api_key_encrypted = None
        else:
            self._api_key_encrypted = encrypt_api_key(api_key)

    @property
    def api_key(self) -> Optional[str]:
        """Return the decrypted API key for application use."""
        if not self._api_key_encrypted:
            return None
        return decrypt_api_key(self._api_key_encrypted)

    @property
    def api_key_encrypted(self) -> Optional[str]:
        """Expose the stored encrypted API key value."""
        return self._api_key_encrypted

    def has_api_key(self) -> bool:
        return bool(self._api_key_encrypted)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(String(100), nullable=False)
    direction = Column(String(10), nullable=False)  # 'in' для входящих, 'out' для исходящих

    user = relationship("User", back_populates="messages")

# Создание базы данных
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

# Настройка сессии
Session = sessionmaker(bind=engine)
session = Session()
