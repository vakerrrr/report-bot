from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

#все статусы бота от ожидания точки до подтверждения
class ReportStates(StatesGroup):
    waiting_for_point = State()
    waiting_for_sim = State()
    waiting_for_cubes = State()
    waiting_for_credit = State()
    waiting_for_double = State()
    confirmation = State()
    final_confirmation = State()