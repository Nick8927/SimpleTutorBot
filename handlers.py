from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from database.db import SessionLocal
from database.models import User, MessageLog

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    """реагирует на команду /start"""
    session = SessionLocal()
    tg_id = message.from_user.id
    user = session.query(User).filter(User.telegram_id == tg_id).first()
    if not user:
        user = User(
            telegram_id=tg_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )
        session.add(user)
        session.commit()
        await message.answer('Вы зарегистрированы')
    else:
        await message.answer('Вы уже зарегистрированы')
    session.close()


@router.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
    print(message.from_user.id)
    if user:
        await message.answer(
            f"Ваш id: {user.telegram_id}\n"
            f"Ваш никнейм: {user.username}\n"
            f"Регистрация: {user.registered_at}\n"
        )
    else:
        await message.answer('Нет регистрации')
    session.close()


@router.message(F.text.regexp(r"^(?!\/).+"))
async def log_message(message: types.Message):
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == message.from_user.id).first()

    if user:
        log = MessageLog(user_id=user.id, message_text=message.text)
        session.add(log)
        session.commit()

    session.close()

@router.message(Command('history'))
async def history_handler(message: types.Message):
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == message.from_user.id).first()

    if user:
        messages = (session.query(MessageLog).
                    filter(MessageLog.user_id == user.id).
                    order_by(MessageLog.timestamp.desc()).
                    limit(3).
                    all())
        if messages:
            text = "\n".join([f"{m.timestamp}: {m.message_text}" for m in messages])
            await message.answer('Последние сообщения: ', text)

    session.close()