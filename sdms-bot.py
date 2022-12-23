from aiogram import executor
from sdms_bot_creating import dispatcher
from handlers import start_handlers, oops_handlers
from services import assignment_service, document_service, authorization_service, registartion_service


start_handlers.start_register(dispatcher)

registartion_service.reg_register(dispatcher)
authorization_service.auth_register(dispatcher)

assignment_service.assignment_register(dispatcher)
document_service.document_register(dispatcher)

oops_handlers.oops_register(dispatcher)


executor.start_polling(dispatcher)
