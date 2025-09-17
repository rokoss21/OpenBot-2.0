#main.py
# Необходимые импорты
import asyncio
import logging
import time
from datetime import datetime
from typing import Optional, Tuple

import httpx
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TELEGRAM_BOT_TOKEN, AVAILABLE_MODELS, API_VALIDATE_URL
from log_config import setup_logging
# Импортируйте SessionLocal для создания сессий и Session для аннотации
from db import (get_user_by_telegram_id, create_or_update_user, update_user_api_key, update_user_model,
                add_message, get_user_messages, delete_user_messages, SessionLocal)
from openrouter import send_to_openrouter
from models import User
from sqlalchemy.orm import Session  # Только для аннотации типов




# Настройка логгирования
setup_logging()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def send_typing_action(chat_id, context):
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(1)

def start(update: Update, context: CallbackContext) -> None:
    welcome_message = """
    🤖 Привет! Я - бот, помогающий взаимодействовать с ИИ через OpenRouter.
    Для начала, пожалуйста, введите ваш API ключ от OpenRouter командой /api <API_KEY>.
    Это позволит мне обрабатывать ваши запросы с использованием выбранной модели ИИ.
    """
    update.message.reply_text(welcome_message)

async def _validate_api_key_request(api_key: str) -> httpx.Response:
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        return await client.get(API_VALIDATE_URL, headers=headers)


def _update_user_validity(session: Session, user_id: int, is_valid: bool) -> None:
    user = session.query(User).filter(User.telegram_id == user_id).first()
    if user:
        user.is_valid = is_valid
        session.commit()


async def validate_api_key_async(api_key: str, user_id: int, session: Session) -> Tuple[bool, Optional[str]]:
    is_valid = False
    error_message: Optional[str] = None

    try:
        response = await _validate_api_key_request(api_key)
    except httpx.HTTPError as exc:
        logger.error(f"Error validating API key for user {user_id}: {exc}")
        error_message = "Не удалось проверить API ключ. Попробуйте позже."
    except Exception as exc:
        logger.error(f"Unexpected error validating API key for user {user_id}: {exc}")
        error_message = "Не удалось проверить API ключ. Попробуйте позже."
    else:
        if response.status_code == 200:
            is_valid = True
            logger.info(f"API key for user {user_id} is valid.")
        elif response.status_code in (401, 403):
            error_message = "API ключ недействителен. Пожалуйста, введите другой ключ командой /api."
            logger.warning(
                f"API key validation failed for user {user_id} with status code {response.status_code}: {response.text}"
            )
        else:
            error_message = (
                "Не удалось проверить API ключ. Код ответа: "
                f"{response.status_code}. Попробуйте позже."
            )
            logger.error(
                f"API key validation for user {user_id} returned unexpected status {response.status_code}: {response.text}"
            )

    _update_user_validity(session, user_id, is_valid)

    if is_valid:
        return True, None

    return False, error_message or "Не удалось проверить API ключ. Попробуйте позже."


def validate_api_key(api_key: str, user_id: int, session: Session) -> Tuple[bool, Optional[str]]:
    return asyncio.run(validate_api_key_async(api_key, user_id, session))

def api(update: Update, context: CallbackContext) -> None:
    send_typing_action(update.message.chat_id, context)
    api_key = ' '.join(context.args)
    if not api_key:
        update.message.reply_text('Пожалуйста, отправьте API ключ после команды /api.')
        return

    user_id = update.effective_user.id
    # Используем SessionLocal для создания новой сессии
    with SessionLocal() as session:
        is_valid, error_message = validate_api_key(api_key, user_id, session)
        if is_valid:
            # Обновляем или создаем пользователя с новым ключом внутри сессии
            user = create_or_update_user(user_id, api_key, session)
            # Дополнительная логика с пользователем, если нужно
            context.user_data['api_key_valid'] = True
            update.message.reply_text('API ключ действителен. Теперь вы можете выбрать модель командой /model.')
        else:
            context.user_data['api_key_valid'] = False
            update.message.reply_text(error_message)
        # Сессия автоматически закроется после выхода из блока with





def restricted_access(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        with SessionLocal() as session:  # Используйте context manager для создания сессии
            db_user = get_user_by_telegram_id(user_id, session)  # Передайте сессию как аргумент
            if db_user and db_user.api_key and db_user.is_valid:
                return func(update, context, *args, **kwargs)
            else:
                update.message.reply_text('Пожалуйста, введите действующий API ключ командой /api.')
                return
    return wrapper




@restricted_access
def help_command(update: Update, context: CallbackContext) -> None:
    send_typing_action(update.message.chat_id, context)
    help_text = """
    🤖 Этот бот позволяет общаться с ИИ через OpenRouter.

    Команды:
    /start - начать диалог.
    /api <API_KEY> - установить ваш API ключ.
    /model - выбрать модель ИИ для диалога.
    /new - начать новую сессию, очистив историю сообщений.
    /help - показать эту справку.
    """
    update.message.reply_text(help_text)

@restricted_access
def model(update: Update, context: CallbackContext) -> None:
    send_typing_action(update.message.chat_id, context)
    user_id = update.effective_user.id
    
    with SessionLocal() as session:  # Создаем новую сессию
        db_user = get_user_by_telegram_id(user_id, session)  # Передаем сессию как аргумент
        if db_user and db_user.model_id:
            current_model_info = f"Текущая модель: {db_user.model_id}, токены: {db_user.max_tokens if db_user.max_tokens else 'не указано'}."
            update.message.reply_text(current_model_info)
            
        message = "Выберите модель, отправив её номер:\n\n"
        for key, value in AVAILABLE_MODELS.items():
            message += f"{key}: {value['name']}\n"
        update.message.reply_text(message)
        context.user_data['awaiting_model_choice'] = True


@restricted_access
def new_session(update: Update, context: CallbackContext) -> None:
    send_typing_action(update.message.chat_id, context)
    user_id = update.effective_user.id
    context.user_data.clear()

    with SessionLocal() as session:  # Создание новой сессии
        delete_user_messages(user_id, session)  # Передача сессии как аргумента

    update.message.reply_text('Новая сессия начата. Ваши предыдущие данные очищены.')


@restricted_access
def handle_message(update: Update, context: CallbackContext) -> None:
    send_typing_action(update.message.chat_id, context)
    user_id = update.effective_user.id
    
    with SessionLocal() as session:  # Создаем новую сессию
        db_user = get_user_by_telegram_id(user_id, session)  # Передаем сессию как аргумент
        
        if 'awaiting_model_choice' in context.user_data and context.user_data['awaiting_model_choice']:
            try:
                choice = int(update.message.text)
                if choice in AVAILABLE_MODELS:
                    chosen_model = AVAILABLE_MODELS[choice]
                    # Убедитесь, что функция update_user_model принимает сессию как аргумент
                    update_user_model(user_id, chosen_model['name'], chosen_model.get('max_tokens', 1024), session)
                    update.message.reply_text(f"Модель успешно изменена на {chosen_model['name']} с максимальным количеством токенов {chosen_model.get('max_tokens', 1024)}.")
                    context.user_data['awaiting_model_choice'] = False
                else:
                    update.message.reply_text("Выбран недопустимый номер модели. Пожалуйста, выберите модель из списка командой /model.")
            except ValueError:
                update.message.reply_text("Пожалуйста, введите номер модели из списка, предоставленного командой /model.")
        else:
            if db_user and db_user.api_key and db_user.model_id:
                message_history = [msg.text for msg in get_user_messages(user_id, session)]  # Передаем сессию как аргумент
                response_message = send_to_openrouter(update.message.text, db_user.api_key, db_user.model_id, max_tokens=db_user.max_tokens, message_history=message_history)
                add_message(user_id, update.message.text, datetime.now(), 'in', session)  # Передаем сессию как аргумент
                add_message(user_id, response_message, datetime.now(), 'out', session)  # Передаем сессию как аргумент
                update.message.reply_text(response_message)
            else:
                update.message.reply_text("Модель не выбрана. Пожалуйста, выберите модель командой /model.")




def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("api", api, pass_args=True))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("model", model))
    dispatcher.add_handler(CommandHandler("new", new_session))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
