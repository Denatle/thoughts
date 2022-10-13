import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text
from configs import config as cf
from configs.localization import *
from configs.keyboards import *
from routers import thoughts, mistakes

bot = Bot(token=cf.TOKEN, parse_mode="html")
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Text(start_words, ignore_case=True))
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext) -> None:
    """
    This function is called when the user sends the /start command.
    It clears the state and sends a message to the user.
    """
    await state.clear()
    await message.answer(start_message.format(message.from_user.full_name), 
                         reply_markup=start_keyboard())

@dp.message(Text(cancel_words, ignore_case=True))
@dp.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(cancel_message, 
                         reply_markup=start_keyboard())


if __name__ == "__main__":
    dp.include_router(thoughts.router)
    
    # needs to be the last one
    dp.include_router(mistakes.router)

    asyncio.run(dp.start_polling(bot))
