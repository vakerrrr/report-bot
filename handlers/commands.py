from aiogram import F, types
from aiogram.filters import Command
from aiogram.types import (Message,
                           ReplyKeyboardRemove,
                           KeyboardButton)
from keyboards.all_kb import points_kb, easter, get_confirm_kb
from classes import text
from classes.states import ReportStates
from classes.text import POINT_PLANS, user_report
from aiogram.fsm.context import FSMContext
from functions.func import format_report
from create_bot import bot, admin, router

#те самые инлайн кнопки
@router.message(F.text == 'Кто твой создатель?')
async def easter_text(message: Message):
    await message.answer('Мой создатель Родников Владислав.\n Самый харизматичный, трудолюбивый, крутой и скромный парень.', reply_markup=easter())
#...(дальше команды, нужно дописать команду для показа планов по точке, пока что лень)...
@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(text.start_text, reply_markup=ReplyKeyboardRemove())

@router.message(Command('report'))
async def cmd_report(message: Message, state: FSMContext):
    await state.set_state(ReportStates.waiting_for_point)
    await message.answer('🚀<b>Поздравляю с завершением рабочего дня!</b>\n\n'
                         '<u>📍Выберите свою точку:</u>',reply_markup=points_kb())
#тут реагируем на нажатие кнопки выбора точки
@router.message(ReportStates.waiting_for_point, F.text.in_(POINT_PLANS.keys()))
async def point_selected(message: Message, state: FSMContext):
    point = message.text
    user_report[message.from_user.id] = {
        'point': point,
        'point_data': POINT_PLANS[point]
    }
    if point == 'S312': #тут пасхалочка
        await message.answer('<b>ОТДЕЛЬНО ПОЗДРАВЛЯЕМ КАЖДОГО СОТРУДИКА С ЗАВЕРШЕНИЕМ СМЕНЫ!!!</b>\n\n'
                             '<b>МЫ ДАЖЕ НЕ ПРЕДСТАВЛЯЕМ КАК ВЫ ВЫЖИЛИ В ЭТОМ АДУ 0_0</b>')
        await state.set_state(ReportStates.waiting_for_sim)
        await message.answer(f'<b>✅Ваша точка: <u>{point}</u></b>\n\n'
                             f'📍<b>План по SIM на твою точку: <u>{POINT_PLANS[point]['sim_plan']}</u></b>\n\n'
                           '<u>📋Введите колличество проданных SIM:</u>',
                             #cancel_button
                          reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(ReportStates.waiting_for_sim)
        await message.answer(f'<b>✅Ваша точка: <u>{point}</u></b>\n\n'
                            f'📍<b>План по SIM на твою точку: <u>{POINT_PLANS[point]['sim_plan']}</u></b>\n\n'
                            '<u>📋Введите колличество проданных SIM:</u>',
                            # cancel_button
                            reply_markup=ReplyKeyboardRemove())
#...(дальше обработчики)...
@router.message(ReportStates.waiting_for_sim)
async def process_sim(message: Message, state: FSMContext):
    sim_sold = int(message.text)
    user_report[message.from_user.id]['sim_sold'] = sim_sold
    await state.set_state(ReportStates.waiting_for_cubes)
    await message.answer(f'<b>✅Продано SIM: <u>{sim_sold}</u></b>\n\n'
                         f'📍<b>План по кубикам на твою точку: <u>{user_report[message.from_user.id]['point_data']['cubes_plan']}</u></b>\n\n'
                         '📋<u>Введите колличество проданных кубиков:</u>')

@router.message(ReportStates.waiting_for_cubes)
async def process_cubes(message: Message, state: FSMContext):
    cubes_sold = int(message.text)
    user_report[message.from_user.id]['cubes_sold'] = cubes_sold
    await state.set_state(ReportStates.waiting_for_credit)
    await message.answer(f'✅<b>Продано кубиков: <u>{cubes_sold}</u></b>\n\n'
                         f'📍<b>План по кредитным заявкам на твою точку: <u>{user_report[message.from_user.id]['point_data']['credit_plan']}</u></b>\n\n'
                         '📋<u>Введите колличество заявок на кредит:</u>')

@router.message(ReportStates.waiting_for_credit)
async def process_credit(message: Message, state: FSMContext):
    credit_apps = int(message.text)
    user_report[message.from_user.id]['credit_apps'] = credit_apps
    await state.set_state(ReportStates.waiting_for_double)
    await message.answer(f'✅<b>Заявок сегодня: <u>{credit_apps}</u></b>\n\n'
                         f'📍<b>План по SIM с двойной выгодой на твою точку: <u>{user_report[message.from_user.id]['point_data']['double_plan']}</u></b>\n\n'
                         '📋<u>Введите колличество проданных SIM с двойной выгодой:</u>')

@router.message(ReportStates.waiting_for_double)
async def process_double(message: Message, state: FSMContext):
    double_sold = int(message.text)
    user_report[message.from_user.id]['double_sold'] = double_sold
    await state.set_state(ReportStates.confirmation)
    await message.answer('✅Отлично, отчёт готов!\n\n'
                         '📋Теперь введите комментарий с причинами невыполнения ежедневных планов по направлениям.\n\n'
                         'Или нажмите пропустить.', reply_markup=types.ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Пропустить')]], resize_keyboard=True))
#пишем ком и отправляем руководству
@router.message(ReportStates.confirmation)
async def confirm(message: Message, state: FSMContext):
    if message.text.lower() != 'Пропустить':
        user_report[message.from_user.id]['comment'] = message.text
    report = format_report(user_report[message.from_user.id])
    await message.answer('📝<b>Предварительный просмотр отчета:</b>\n\n' + report, parse_mode='HTML', reply_markup=get_confirm_kb())
    await state.set_state(ReportStates.final_confirmation)

@router.message(ReportStates.final_confirmation, F.text == '✅Отправить')
async def send_report(message: Message, state: FSMContext):
    report = format_report(user_report[message.from_user.id])
    await bot.send_message(admin, report, parse_mode='HTML')
    await message.answer('✅Отчёт успешно отправлен!', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(ReportStates.final_confirmation, F.text == '✏️Редактировать')
async def edit_report(message: Message, state: FSMContext):
    await state.set_state(ReportStates.waiting_for_sim)
    await message.answer('<b>Повторно заполните корректный отчёт.</b>\n\n'
                         '<u>📋Введите колличество проданных SIM:</u>', reply_markup=ReplyKeyboardRemove())