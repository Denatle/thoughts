from aiogram import Router, types, F
from aiogram.filters import Text, StateFilter, Command
from aiogram.fsm.context import FSMContext
from configs.keyboards import cancel_key, start_keyboard
from configs.localization import *
from configs.localization import Buttons
from modules.database import DataBase
from modules.states import Thoughts

db = DataBase()
router = Router()


@router.message(StateFilter(None), Text(Buttons.start_keys[0]))
async def new_thought(message: types.Message, state: FSMContext) -> None:
    """
    This function is used to start the process of creating a new thought.
    It sets the state of the conversation to NewThought.thought_message and
    sends a message to the user asking them to send the message of the thought.
    """
    await state.set_state(Thoughts.thought_new_message)
    await message.answer(new_thought_message,
                         reply_markup=cancel_key())


@router.message(Thoughts.thought_new_message, F.text)
async def new_thought_listen(message: types.Message, state: FSMContext) -> None:
    """
    This function is used to create a new thought.
    """
    db.add_thought(message.text)
    await state.clear()
    await message.answer(after_state_message,
                         reply_markup=start_keyboard())


@router.message(StateFilter(None), Text(Buttons.start_keys[1]))
async def random_thought(message: types.Message) -> None:
    """
    This function is used to send a random thought.
    """
    id, rating, thought = db.get_thought_random().values()
    await message.answer(thought_message.format(thought, id))


# @router.message(StateFilter(None), Text(Buttons.start_keys[2]))
# async def rate_mode(message: types.Message, state: FSMContext):
#     pass


# @router.message(StateFilter(None), Text(Buttons.start_keys[3]))
# async def fight_mode(message: types.Message, state: FSMContext):
#     await state.set_state(Thoughts.fight_mode)
#     await message.answer()


@router.message(Thoughts.fight_mode)
async def fight_mode_listen(message: types.Message, state: FSMContext):
    pass


@router.message(Command("thought_id"), StateFilter(None))
async def get_thought_by_id(message: types.Message, state: FSMContext):
    await state.set_state(Thoughts.by_id)
    await message.answer(what_id)


@router.message(F.text, Thoughts.by_id)
async def get_thought_by_id_listener(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        id, rating, thought = db.get_thought_id(message.text).values()
        if thought:
            await message.answer(thought_message.format(thought, id))
        else:
            await message.answer(no_such_thought)
    else:
        await message.answer(no_such_thought)
    await state.clear()
