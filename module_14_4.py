from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from crud_functions import initiate_db, get_all_products
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

initiate_db()
api = '7701580394:AAHk88GGRw8Sh7vqi3MvYqa1V1FpKZcY'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')

kb.add(button1, button2)
kb.add(button3)
kbInline = InlineKeyboardMarkup()
buttonInlKalories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
buttonInlFormula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kbInline.add(buttonInlKalories, buttonInlFormula)
kbInline1 = InlineKeyboardMarkup()
buttonInlChoise = InlineKeyboardButton(text="Выберите продукт для покупки:", callback_data='product_buying')
kbInline1.add(buttonInlChoise)


class UserState(StatesGroup):
    sex = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я помогу тебе рассчитать ежедневную норму калорий'
                         , reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    count_ = 1
    product_list = []
    for product in products:
        product_list.append(product)
    for el in product_list:
        photo_path = f'images/product{count_}.png'
        await message.answer_photo(photo=open(photo_path, 'rb'),
                                   caption=f'Название: {el[1]} | Описание: описание {el[2]} | Цена: {el[3]}',
                                   reply_markup=kbInline1)
        count_+=1


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text="Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup=kbInline)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("Калории рассчитываются по формулам Миффлина-Сан Жеора.")
    await call.answer()


# @dp.message_handler(text='Рассчитать')
@dp.callback_query_handler(text='calories')
async def set_sex(call):
    await call.message.answer('Введите свой пол: Муж или Жен')
    await UserState.sex.set()
    await call.answer()


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Я бот, который поможет тебе определить норму потребления '
                         'калорий, нажми "Рассчитать"')


@dp.message_handler(state=UserState.sex)
async def set_age(message, state):
    await state.update_data(sex=message.text)  # Сохранение пола
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['sex'] == 'Муж':
        recomendation = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    else:
        recomendation = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161

    await message.answer(f'Ежедневно Вы должны потреблять не более - {recomendation}')
    await state.finish()
    print(recomendation)


@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
