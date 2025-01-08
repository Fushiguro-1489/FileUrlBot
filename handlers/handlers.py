from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext

from config import FREE_LINK_LIMIT
from database.db import SessionLocal
from database.tables import User, Link
from keyboards.keyboards import main_menu_keyboard
from states import AddLink

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message):
    """
    Команда-обработчик для просмотра стартовой информации.
    """
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        user = User(telegram_id=message.from_user.id)
        session.add(user)
        session.commit()
        await message.reply("Привет! Я помогу сохранить твои ссылки.\n"
                            "Используй /add для добавления ссылки.", reply_markup=main_menu_keyboard())
    else:
        await message.reply("С возвращением! Используй /add для добавления ссылки.", reply_markup=main_menu_keyboard())
    session.close()


@router.message(Command('help'))
@router.message(F.data == 'help')
async def help_command(message: types.Message):
    """
    Команда-обработчик для просмотра справочной информации.
    """
    await message.reply('Бот позволяет: TODO')


@router.message(Command('add'), StateFilter(None))
@router.message(F.data == 'add')
@router.message(F.text.lower() == "добавить")
@router.message(F.text.lower() == "добавить ссылку")
async def add_url_command(message: types.Message, state: FSMContext):
    """
    Обработчик добавления ссылки.
    """

    await message.answer(
        "Напишите URL"
    )
    await state.set_state(AddLink.choosing_url)
    return

    # # Если не переданы никакие аргументы, то
    # # command.args будет None
    # if command is not None:
    #     if command.args is None:
    #
    #     # Пробуем разделить аргументы на две части по первому встречному пробелу
    #     try:
    #         url, name = command.args.split(" ", maxsplit=1)
    #     # Если получилось меньше двух частей, вылетит ValueError
    #     except ValueError:
    #         await message.answer(
    #             "Ошибка: неправильный формат команды. Пример:\n"
    #             "/add <url> <name>"
    #         )
    #         return
    #
    # session = SessionLocal()
    # user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    #
    # if not user:
    #     await message.reply("Сначала используй /start для регистрации.")
    #     session.close()
    #     return
    #
    # if not user.is_premium and len(user.links) >= FREE_LINK_LIMIT:
    #     await message.reply(f"У вас уже {FREE_LINK_LIMIT} ссылок. "
    #                         "Оформите премиум, чтобы добавить больше.")
    #     session.close()
    #     return
    #
    # # Save link to the database
    # new_link = Link(url=url, title=name, user=user)
    # session.add(new_link)
    # session.commit()
    #
    # session.close()


@router.message(
    AddLink.choosing_url,
)
async def add_link_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, напишите имя."
    )
    await state.set_state(AddLink.choosing_name)


@router.message(
    AddLink.choosing_name,
)
async def add_link_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = message.text.lower()

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

    link = session.query(Link).filter_by(url=data['url']).first()
    if link:
        await message.reply('Данная ссылка уже есть в БД.\nДобавление отменено.')
        await state.clear()
        return

    # Save link to the database
    new_link = Link(url=data['url'], title=name, user=user)
    session.add(new_link)
    session.commit()

    await message.answer(
        text="Спасибо! Данные сохранены."
    )
    await state.clear()


@router.message(Command('links'))
@router.message(F.data == 'links')
@router.message(F.text.lower() == "ссылки")
async def links_command(message: types.Message):
    """
    Обработчик просмотра ссылок.
    """
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

    if not user:
        await message.reply("Сначала используй /start для регистрации.")
        session.close()
        return

    if not user.links:
        await message.reply("У вас ещё нет ссылок. Добавьте с помощью /add.")
    else:
        links_text = "\n".join([f"{link.title}: {link.url}" for link in user.links])
        await message.reply(f"Ваши ссылки:\n{links_text}")

    session.close()
