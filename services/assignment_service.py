import datetime

from DAO import assignment_dao
from sdms_bot_creating import bot
from templates import notification
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from services.authorization_service import whitelist
from keyboards.auth_menu_keyboard import auth_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.assignment_keyboards.assignment_menu import a_menu
from keyboards.assignment_keyboards.cancel_assignment_keyboard import cancel_a
from keyboards.recipient_keyboard import recipient_for_admin, recipient_for_head

posts = ['ADMIN', 'HEAD', 'SPEC']


class Assignment(StatesGroup):  # Assignment State class
    recipient = State()
    name = State()
    desc = State()
    owner = State()

    name_for_cancel = State()

    delegated = State()
    name_for_delegated = State()


async def assignments_menu(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Выберите опцию:", reply_markup=a_menu)


async def create_new_assignment(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    elif whitelist[message.from_user.id][0] == 'SPEC':
        await bot.send_message(message.from_user.id, notification.cant_give_assignments[0])

    elif whitelist[message.from_user.id][0] == 'HEAD':
        await Assignment.recipient.set()
        await bot.send_message(message.from_user.id, notification.recipient_assignment, reply_markup=recipient_for_head)
    else:
        await Assignment.recipient.set()
        await bot.send_message(message.from_user.id, notification.recipient_assignment,
                               reply_markup=recipient_for_admin)


async def cancel_creating_assignment(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[1], reply_markup=a_menu)


async def recipient_assignment(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['recipient'] = message.text

        if message.text == 'ADMIN':
            await bot.send_message(message.from_user.id, notification.cant_give_assignments[1], reply_markup=a_menu)
            await state.finish()

        elif whitelist[message.from_user.id][0] == 'HEAD' and message.text == 'HEAD' or \
                whitelist[message.from_user.id][0] == 'ADMIN' and data['recipient'] == 'ADMIN':

            await bot.send_message(message.from_user.id, notification.cant_give_assignments[1], reply_markup=a_menu)
            await state.finish()

        elif message.text not in posts:
            await bot.send_message(message.from_user.id, notification.user_doesnt_exist, reply_markup=a_menu)
            await state.finish()

        else:
            await Assignment.next()
            await bot.send_message(message.from_user.id, notification.assignment_name, reply_markup=cancel_a)


async def name_assignment(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        exits_records = assignment_dao.check_on_exists(data['name'])

        if exits_records:
            await bot.send_message(message.from_user.id, notification.assignment_already_exist)
            await state.finish()

        elif not exits_records:
            await Assignment.next()
            await bot.send_message(message.from_user.id, notification.assignment_desc)


async def desc_assignment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await owner_assignment(message, state)


async def owner_assignment(message: types.Message, state: FSMContext):
    date = datetime.datetime.now().date()
    async with state.proxy() as data:
        owner = whitelist[message.from_user.id][0]
        assignment_dao.create_assignment(data['name'], data['desc'], date, owner, data['recipient'])

    await bot.send_message(message.from_user.id, notification.assignment_ready, reply_markup=a_menu)
    await state.finish()


async def start_cancel_assignment(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)
    elif whitelist[message.from_user.id][0] == 'SPEC':
        await bot.send_message(message.from_user.id, notification.cant_cancel_assignment)
    else:
        await Assignment.name_for_cancel.set()
        await bot.send_message(message.from_user.id, notification.assignment_name)


async def cancel_canceling_assignment(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[2])


async def cancel_assignment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_for_cancel'] = message.text

        owner = assignment_dao.search_owner_by_a_name(data['name_for_cancel'])
        a_id = assignment_dao.search_a_id_by_a_name(data['name_for_cancel'])

        if owner is None:
            await bot.send_message(message.from_user.id, notification.assignment_doesnt_exist, reply_markup=a_menu)
            await state.finish()

        elif owner[0] == 'ADMIN' and whitelist[message.from_user.id][0] != 'ADMIN':
            await bot.send_message(message.from_user.id, notification.cant_cancel_assignment)
            await state.finish()

        else:
            assignment_dao.cancel_assignment(a_id[0])

            await bot.send_message(message.from_user.id, notification.assignment_cancel)
            await state.finish()


async def assignment_delegate(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    elif whitelist[message.from_user.id][0] == 'SPEC':
        await bot.send_message(message.from_user.id, notification.cant_delegated_assignment)
    else:
        await Assignment.delegated.set()
        await bot.send_message(message.from_user.id, notification.delegated_recipient)


async def cancel_delegated_assignment(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[3], reply_markup=a_menu)


async def post_for_delegated(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delegated'] = message.text

        if message.text == 'ADMIN' or message.text == 'HEAD':
            await bot.send_message(message.from_user.id, notification.cant_delegated_admin, reply_markup=a_menu)
            await state.finish()

        else:
            await Assignment.next()
            await bot.send_message(message.from_user.id, notification.assignment_name)


async def name_for_delegated(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_for_delegated'] = message.text

        a_id = assignment_dao.search_a_id_by_a_name(message.text)
        a_active = assignment_dao.check_on_active(a_id[0])

        if a_id is None:
            await bot.send_message(message.from_user.id, notification.assignment_doesnt_exist)
            await state.finish()

        elif a_id is not None:
            if a_active[0] == 'Закрыто':
                await bot.send_message(message.from_user.id, notification.a_is_closed, reply_markup=a_menu)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, notification.a_is_closed, reply_markup=a_menu)
                assignment_dao.delegated_assignment(data['delegated'], a_id[0])
                await bot.send_message(message.from_user.id, notification.delegated_success)
                await state.finish()


async def find_all_assignments(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    else:
        if whitelist[message.from_user.id][0] == 'ADMIN':
            admin_assignments = assignment_dao.find_all_assignment()
            if not admin_assignments:
                await bot.send_message(message.from_user.id, notification.no_active_assignment)

            else:
                assignment = "\n📃 ".join(admin_assignments)
                await bot.send_message(message.from_user.id, f"{notification.all_assignments} \n\n📃 {assignment}")

        elif whitelist[message.from_user.id][0] == 'HEAD':
            head_assignments = assignment_dao.find_all_assignment_for_head()
            if not head_assignments:
                await bot.send_message(message.from_user.id, notification.no_active_assignment)

            else:
                assignment = "\n📃 ".join(head_assignments)
                await bot.send_message(message.from_user.id, f"{notification.all_assignments} \n\n📃 {assignment}")

        elif whitelist[message.from_user.id][0] == 'SPEC':
            spec_assignments = assignment_dao.find_all_assignment_for_spec()
            if not spec_assignments:
                await bot.send_message(message.from_user.id, notification.no_active_assignment)

            else:
                assignment = "\n📃 ".join(spec_assignments)
                await bot.send_message(message.from_user.id, f"{notification.all_assignments} \n\n📃 {assignment}")


def assignment_register(dp: Dispatcher):
    dp.register_message_handler(assignments_menu, Text(equals="поручения", ignore_case=True))

    dp.register_message_handler(create_new_assignment, Text(equals='новое поручение', ignore_case=True), state=None)
    dp.register_message_handler(cancel_creating_assignment, Text(equals='отменить создание', ignore_case=True),
                                state="*")
    dp.register_message_handler(recipient_assignment, state=Assignment.recipient)
    dp.register_message_handler(name_assignment, state=Assignment.name)
    dp.register_message_handler(desc_assignment, state=Assignment.desc)
    dp.register_message_handler(owner_assignment, state=Assignment.owner)

    dp.register_message_handler(find_all_assignments, Text(equals="все поручения", ignore_case=True))

    dp.register_message_handler(start_cancel_assignment, Text(equals="закрыть поручение", ignore_case=True),
                                state=None)
    dp.register_message_handler(cancel_canceling_assignment, Text(equals="отменить закрытие", ignore_case=True),
                                state="*")
    dp.register_message_handler(cancel_assignment, state=Assignment.name_for_cancel)

    dp.register_message_handler(assignment_delegate, Text(equals="делегировать поручение", ignore_case=True),
                                state=None)
    dp.register_message_handler(cancel_delegated_assignment, Text(equals='отменить делегирование', ignore_case=True),
                                state="*")
    dp.register_message_handler(post_for_delegated, state=Assignment.delegated)
    dp.register_message_handler(name_for_delegated, state=Assignment.name_for_delegated)
