import os
import datetime
import urllib.request

from sdms_bot_creating import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from DAO import document_dao, assignment_dao
from templates import notification, variables
from services.authorization_service import whitelist
from keyboards.auth_menu_keyboard import auth_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.document_keyboards.document_menu import doc_menu

from keyboards.document_keyboards.cancel_keyboard import k_cancel_downloading, k_cancel_signing, \
    k_cancel_revision, k_cancel_deleting


class Document(StatesGroup):  # Document State class
    assignment_id = State()
    desc = State()
    name = State()
    name_on_deleting = State()
    name_on_sign = State()
    name_for_revision = State()


async def create_new_document(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    else:
        await Document.assignment_id.set()
        await bot.send_message(message.from_user.id, notification.assignment_name, reply_markup=k_cancel_downloading)


async def cancel_creating_document(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[4], reply_markup=doc_menu)


async def set_assignment_id(message: types.Message, state: FSMContext):
    a_id = assignment_dao.search_a_id_by_a_name(message.text)
    active = assignment_dao.check_on_active(a_id[0])

    if a_id is None:
        await bot.send_message(message.from_user.id, notification.assignment_doesnt_exist +
                               notification.repeat_downloading, reply_markup=doc_menu)
        await state.finish()

    elif active is None:
        await bot.send_message(message.from_user.id, notification.assignment_doesnt_exist)
        await state.finish()

    elif active[0] == 'Закрыто':
        await bot.send_message(message.from_user.id, notification.assignment_is_close, reply_markup=doc_menu)
        await state.finish()

    elif a_id[0]:
        async with state.proxy() as data:
            data['a_id'] = a_id[0]

        await Document.next()
        await bot.send_message(message.from_user.id, notification.document_desc)


async def desc_document(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await Document.next()
    await bot.send_message(message.from_user.id, notification.download_doc)


async def send_document(message: types.Message, state: FSMContext):
    date = datetime.datetime.now().date()
    async with state.proxy() as data:
        data['name'] = message.document.file_name
        name = data['name']

        document_id = message.document.file_id
        file_info = await bot.get_file(document_id)
        file_path = file_info.file_path

        urllib.request.urlretrieve(variables.tg_api + file_path, variables.server_path + name)
        doc_id = document_dao.search_doc_id_by_name(variables.server_path + name)

        if doc_id:
            await bot.send_message(message.from_user.id, notification.doc_already_exist, reply_markup=doc_menu)
            await state.finish()
        else:
            document_dao.create_document(data['a_id'], variables.server_path + name, data['desc'], date)

            await bot.send_message(message.from_user.id, notification.success_downloading)
            await state.finish()


async def find_all_documents(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    else:
        if whitelist[message.from_user.id][0] == 'ADMIN':
            admin_docx = document_dao.find_all_docx_for_admin()
            if not admin_docx:
                await bot.send_message(message.from_user.id, notification.no_active_document)

            else:
                document = "\n\n📄 ".join(admin_docx)
                await bot.send_message(message.from_user.id, f"{notification.all_documents} \n\n📄"+document)

        elif whitelist[message.from_user.id][0] == 'HEAD':
            admin_docx = document_dao.find_all_docx_for_head()
            if not admin_docx:
                await bot.send_message(message.from_user.id, notification.no_active_document)

            else:
                document = "\n📄 ".join(admin_docx)
                await bot.send_message(message.from_user.id, f"{notification.all_documents} \n\n📄 {document}")

        elif whitelist[message.from_user.id][0] == 'SPEC':
            admin_docx = document_dao.find_all_docx_for_spec()
            if not admin_docx:
                await bot.send_message(message.from_user.id, notification.no_active_document)

            else:
                document = "\n📄 ".join(admin_docx)
                await bot.send_message(message.from_user.id, f"{notification.all_documents} \n\n📄 {document}")


async def delete_document_by_name(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    else:
        await Document.name_on_deleting.set()
        await bot.send_message(message.from_user.id, notification.doc_name, reply_markup=k_cancel_deleting)


async def cancel_deleting(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[5], reply_markup=doc_menu)


async def doc_name_for_deleting(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['del_name'] = message.text
        name = variables.server_path + data['del_name']

        doc_id = document_dao.search_doc_id_by_name(name)
        sign = document_dao.check_on_sign(name)

        if doc_id is None and sign is None:
            await bot.send_message(message.from_user.id, notification.doc_doesnt_exist, reply_markup=doc_menu)
            await state.finish()

        elif sign[0] != 'Нет подписи':
            await bot.send_message(message.from_user.id, notification.cant_delete_sign, reply_markup=doc_menu)
            await state.finish()

        elif sign[0] == 'Нет подписи':
            document_dao.delete_doc_by_id(doc_id[0])
            os.remove(variables.server_path + data['del_name'])
            await bot.send_message(message.from_user.id, "Документ удален", reply_markup=doc_menu)
            await state.finish()


async def sign_document(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    else:
        await Document.name_on_sign.set()
        await bot.send_message(message.from_user.id, notification.doc_name, reply_markup=k_cancel_signing)


async def cancel_signing(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[6], reply_markup=doc_menu)


async def name_doc_for_sign_document(message: types.Message, state: FSMContext):
    post = whitelist.get(message.from_user.id)[0]
    async with state.proxy() as data:
        data['sign_name'] = message.text
        sign_check = document_dao.check_on_sign(variables.server_path + message.text)
        if sign_check is None:
            await bot.send_message(message.from_user.id, notification.doc_doesnt_exist, reply_markup=doc_menu)
            await state.finish()

        elif sign_check[0] == 'ADMIN':
            await bot.send_message(message.from_user.id, notification.doc_already_sign_by_admin, reply_markup=doc_menu)
            await state.finish()

        elif sign_check[0] == 'HEAD' and post == 'SPEC':
            await bot.send_message(message.from_user.id, notification.doc_already_sign_by_head, reply_markup=doc_menu)
            await state.finish()

        else:
            a_id = document_dao.search_a_id_by_doc_name(variables.server_path + data['sign_name'])
            document_dao.signing_by(variables.server_path+message.text, a_id[0], post)

            await bot.send_message(message.from_user.id, f"{notification.doc_sign_by}{post}", reply_markup=doc_menu)
            await state.finish()


async def send_to_revision(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    elif whitelist[message.from_user.id][0] == 'SPEC':
        await bot.send_message(message.from_user.id, notification.cant_revision)

    else:
        await Document.name_for_revision.set()
        await bot.send_message(message.from_user.id, notification.doc_name, reply_markup=k_cancel_revision)


async def cancel_sending_to_revision(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, notification.cancel_notifications[7], reply_markup=doc_menu)


async def name_for_revision(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_for_revision'] = message.text

        doc_id = document_dao.search_doc_id_by_name(variables.server_path + data['name_for_revision'])

        if doc_id is None:
            await bot.send_message(message.from_user.id, notification.doc_doesnt_exist, reply_markup=doc_menu)
            await state.finish()

        else:

            if whitelist[message.from_user.id][0] == 'ADMIN':
                sign_by = 'SPEC'
            elif whitelist[message.from_user.id][0] == 'HEAD':
                sign_by = 'Нет подписи'

            document_dao.send_to_revision(doc_id[0], sign_by)
            await bot.send_message(message.from_user.id, notification.revision_success)
            await state.finish()


async def doc_on_revision(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)
    else:

        if whitelist[message.from_user.id][0] == 'HEAD':
            docx = document_dao.find_all_docx_on_revision_for_head()

            if docx is None:
                await bot.send_document(message.from_user.id, notification.no_under_rev, reply_markup=doc_menu)
            elif docx is not None:
                document = "\n📄 ".join(docx)
                await bot.send_message(message.from_user.id, f'{notification.all_documents_under_revision}'
                                                                 f'\n\n{document}', reply_markup=doc_menu)

        elif whitelist[message.from_user.id][0] == 'SPEC':
            docx = document_dao.find_all_docx_on_revision_for_spec()

            if docx is None:
                await bot.send_document(message.from_user.id, notification.no_under_rev, reply_markup=doc_menu)

            elif docx is not None:
                document = "\n📄 ".join(docx)
                await bot.send_message(message.from_user.id, f'{notification.all_documents_under_revision}'
                                                                 f'\n\n{document}', reply_markup=doc_menu)


async def document_menu(message: types.Message):
    if message.from_user.id not in whitelist:
        await bot.send_message(message.from_user.id, notification.auth_notification, reply_markup=auth_keyboard)

    else:
        await bot.send_message(message.from_user.id, notification.select_option, reply_markup=doc_menu)


def document_register(dp: Dispatcher):
    dp.register_message_handler(create_new_document, Text(equals='загрузить документ', ignore_case=True),
                                state=None)
    dp.register_message_handler(cancel_creating_document, Text(equals='отменить загрузку документа', ignore_case=True),
                                state="*")
    dp.register_message_handler(set_assignment_id, state=Document.assignment_id)
    dp.register_message_handler(desc_document, state=Document.desc)
    dp.register_message_handler(send_document, content_types=['document'], state=Document.name)

    dp.register_message_handler(find_all_documents, Text(equals='все документы', ignore_case=True))

    dp.register_message_handler(delete_document_by_name, Text(equals='удалить документ', ignore_case=True), state=None)
    dp.register_message_handler(cancel_deleting, Text(equals='отменить удаление', ignore_case=True), state="*")
    dp.register_message_handler(doc_name_for_deleting, state=Document.name_on_deleting)

    dp.register_message_handler(sign_document, Text(equals='подписать документ', ignore_case=True), state=None)
    dp.register_message_handler(cancel_signing, Text(equals='отменить подписание', ignore_case=True), state="*")
    dp.register_message_handler(name_doc_for_sign_document, state=Document.name_on_sign)

    dp.register_message_handler(send_to_revision, Text(equals="отправить на доработку", ignore_case=True),
                                state=None)
    dp.register_message_handler(doc_on_revision, Text(equals="документы на доработке", ignore_case=True))
    dp.register_message_handler(cancel_sending_to_revision, Text(equals='отменить доработку', ignore_case=True),
                                state="*")
    dp.register_message_handler(name_for_revision, state=Document.name_for_revision)
    dp.register_message_handler(document_menu, Text(equals="документы", ignore_case=True))
