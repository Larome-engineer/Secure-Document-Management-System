from aiogram import types, Dispatcher
from sdms_bot_creating import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils import password_encryption
from aiogram.dispatcher.filters import Text
from DAO import person_dao
from templates import notification


class FSMUser(StatesGroup):
    post = State()
    username = State()
    password = State()
    user_tg_id = State()


async def start_registration_position(message: types.Message):  # Start of registration
    user_id = person_dao.search_on_exists(message.from_user.id)

    if not user_id:  # If account doesn't exist
        await FSMUser.post.set()
        await bot.send_message(message.from_user.id, notification.secret_code_notification)

    elif user_id:  # If account already exist
        await bot.send_message(message.from_user.id, notification.account_exists_notification)


async def cancel_appointment(message: types.Message, state: FSMContext):  # To canceling registration at any moment
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[0])


async def enter_code(message: types.Message, state: FSMContext):  # A special indicator for determining the user's post
    if message.text == str('123'):

        async with state.proxy() as data:
            data['post'] = 'ADMIN'

        await FSMUser.next()
        await bot.send_message(message.from_user.id, notification.user_name_notification)

    elif message.text == str('456'):
        async with state.proxy() as data:
            data['post'] = 'HEAD'
        await FSMUser.next()
        await bot.send_message(message.from_user.id, notification.user_name_notification)

    elif message.text == str('789'):
        async with state.proxy() as data:
            data['post'] = 'SPEC'
        await FSMUser.next()
        await bot.send_message(message.from_user.id, notification.user_name_notification)

    else:
        await bot.send_message(message.from_user.id, notification.code_doesnt_exist)
        await state.finish()


async def enter_username(message: types.Message, state: FSMContext):  # Enter username
    async with state.proxy() as data:
        data['username'] = message.text

    await FSMUser.next()
    await bot.send_message(message.from_user.id, notification.pass_notification)


async def enter_password(message: types.Message, state: FSMContext):  # Enter password and completion registration
    async with state.proxy() as data:
        data['password'] = password_encryption.encrypt(message.text)  # Encrypt password by RSA
        data['user_tg_id'] = message.from_user.id

        person_dao.create_person(int(data['user_tg_id']), data['username'], data['post'], data['password'])

    await bot.send_message(message.from_user.id, notification.reg_ready_notification)
    await state.finish()


def reg_register(dp: Dispatcher):  # Register of reg_handlers
    dp.register_message_handler(start_registration_position, Text(equals='регистрация', ignore_case=True), state=None)
    dp.register_message_handler(cancel_appointment, Text(equals="отмена регистрации", ignore_case=True), state="*")
    dp.register_message_handler(enter_code, state=FSMUser.post)
    dp.register_message_handler(enter_username, state=FSMUser.username)
    dp.register_message_handler(enter_password, state=FSMUser.password)



