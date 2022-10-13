from aiogram import Router, types
from configs.localization import *

router = Router()

@router.message()
async def mistake(message: types.Message):
    await message.answer(mistake_message)