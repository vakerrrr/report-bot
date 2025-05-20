from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import (Message,
                           ReplyKeyboardRemove)
from keyboards.all_kb import points_kb
import text
from states import ReportStates
from text import POINT_PLANS, user_report
from aiogram.fsm.context import FSMContext
router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(text.start_text, reply_markup=ReplyKeyboardRemove())

@router.message(Command('report'))
async def cmd_report(message: Message, state: FSMContext):
    await state.set_state(ReportStates.waiting_for_point)
    await message.answer('🚀Выберите свою точку:',reply_markup=points_kb())

@router.message(ReportStates.waiting_for_point, F.text.in_(POINT_PLANS.keys()))
async def point_selected(message: Message, state: FSMContext):
    point = message.text
    user_report[message.from_user.id] = {
        'point': point,
        'point_data': POINT_PLANS[point]
    }
    await state.set_state(ReportStates.waiting_for_sim)
    await message.answer(f'Ваша точка: {point}\n'
                         f'План по SIM:{POINT_PLANS[point]['sim_plan']}\n'
                         'Введите колличество проданных SIM:',
                         reply_markup=ReplyKeyboardRemove())