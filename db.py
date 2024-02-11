from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as BaseSession
from models import Base, User, Message
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_user_by_telegram_id(telegram_id: int, session: BaseSession):
    return session.query(User).filter(User.telegram_id == telegram_id).first()

def create_or_update_user(telegram_id: int, api_key: str, session: BaseSession):
    user = get_user_by_telegram_id(telegram_id, session)
    if user is None:
        user = User(telegram_id=telegram_id, api_key=api_key)
        session.add(user)
    else:
        user.api_key = api_key
    session.commit()
    return user

def update_user_api_key(telegram_id: int, api_key: str, session: BaseSession):
    user = get_user_by_telegram_id(telegram_id, session)
    if user:
        user.api_key = api_key
        session.commit()

def update_user_model(telegram_id: int, model_id: str, max_tokens: int, session: BaseSession):
    user = get_user_by_telegram_id(telegram_id, session)
    if user:
        user.model_id = model_id
        user.max_tokens = max_tokens
        session.commit()

def add_message(user_id: int, text: str, timestamp: str, direction: str, session: BaseSession):
    new_message = Message(user_id=user_id, text=text, timestamp=timestamp, direction=direction)
    session.add(new_message)
    session.commit()
    return new_message

def get_user_messages(user_id: int, session: BaseSession):
    return session.query(Message).filter(Message.user_id == user_id).all()

def delete_user_messages(user_id: int, session: BaseSession):
    session.query(Message).filter(Message.user_id == user_id).delete()
    session.commit()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
