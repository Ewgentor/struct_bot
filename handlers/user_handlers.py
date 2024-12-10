from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, PollAnswer
from buttons.knopki import create_inline_kb, BUTTONS

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    btn_1 = KeyboardButton(text='Создать опрос')
    btn_2 = KeyboardButton(text='Создать викторину')

    keyboard = ReplyKeyboardMarkup(keyboard=[[btn_1, btn_2,]], resize_keyboard=True)

    await message.answer(text='Это учебный бот. Что вы хотите создать?', reply_markup=keyboard)


@router.message(F.text == '/help')
async def process_help(message: Message):
    await message.answer(text="/start - запустить бота\n"
                              "/help - показать все команды\n"
                              "/buttons - тест инлайн кнопок\n")


@router.message(F.text == 'Создать опрос')
async def create_poll(message: Message):
    questions = [
        ("Сколько вам лет?", ["0 - 17", "18 - 49", "50+"]),
        ("Кем вы работаете?", ["Преподаватель", "Студент", "Безработный"]),
        ("Ваш любимый цвет?", ["Красный", "Чёрный", "Синий"])
    ]

    for question, options in questions:
        await message.answer_poll(
            question=question,
            options=options,
            is_anonymous=False
        )


@router.message(F.text == 'Создать викторину')
async def create_quiz(message: Message):
    questions = [
        ("Как называется еврейский Новый год?", ["Ханука", "Йом Кипур", "Кванза"], 0),
        ("В какой стране проходили летние Олимпийские игры 2016 года?", ["Китай", "Ирландия", "Бразилия", "Италия"], 2),
        ("Какая планета самая горячая? ", ["Венера", "Сатурн", "Меркурий"], 0),
    ]

    # Инициализация состояния викторины
    user_id = message.from_user.id
    quiz_state[user_id] = {'current_question': 0, 'correct_answers': 0, 'questions': questions}

    await ask_question(user_id, message)


@router.message(Command('buttons'))
async def process_buttons_command(message: Message):
    # Создание начальной инлайн-клавиатуры с одной кнопкой
    keyboard = create_inline_kb(1,5, **BUTTONS)
    await message.answer(
        text='Это инлайн-клавиатура',
        reply_markup=keyboard
    )


quiz_state = {}


async def ask_question(user_id, poll_answer):
    questions = quiz_state[user_id]['questions']
    current_question = quiz_state[user_id]['current_question']

    if current_question < len(questions):
        question, options, correct_index = questions[current_question]
        if isinstance(poll_answer, PollAnswer):
            await poll_answer.bot.send_poll(
                chat_id=user_id,
                question=question,
                options=options,
                is_anonymous=False,
                type='quiz',
                correct_option_id=correct_index
            )
        else:
            await poll_answer.answer_poll(
                # chat_id=user_id,
                question=question,
                options=options,
                is_anonymous=False,
                type='quiz',
                correct_option_id=correct_index
            )
    else:
        # Завершение викторины
        if isinstance(poll_answer, PollAnswer):
            await poll_answer.bot.send_message(
                chat_id=user_id,
                text=f"Вы ответили правильно на {quiz_state[user_id]['correct_answers']} из {len(questions)} вопросов."
            )
        else:
            await poll_answer.answer(
                # chat_id=user_id,
                text=f"Вы ответили правильно на {quiz_state[user_id]['correct_answers']} из {len(questions)} вопросов."
            )
        del quiz_state[user_id]



@router.poll_answer()
async def handle_poll_answer(poll_answer: Message):
    user_id = poll_answer.user.id
    if user_id in quiz_state:
        current_question = quiz_state[user_id]['current_question']
        questions = quiz_state[user_id]['questions']

        if poll_answer.option_ids[0] == questions[current_question][2]:
            quiz_state[user_id]['correct_answers'] += 1

        quiz_state[user_id]['current_question'] += 1
        await ask_question(user_id, poll_answer)

# Обработчик нажатия на инлайн-кнопку


@router.callback_query()
async def process_callback(callback_query: CallbackQuery):
    if callback_query.data == 'btn_1':
        # Создание новой инлайн-клавиатуры с тремя кнопками
        new_keyboard = create_inline_kb(1,1, 'but_1', 'but_2', 'but_3')
        await callback_query.message.edit_text(
            text='Выберите одну из кнопок:',
            reply_markup=new_keyboard
        )
    elif callback_query.data == 'btn_2':
        # Создание новой инлайн-клавиатуры с тремя кнопками
        new_keyboard = create_inline_kb(2,1, 'but_1', 'but_2', 'but_3')
        await callback_query.message.edit_text(
            text='Выберите одну из кнопок:',
            reply_markup=new_keyboard
        )
    elif callback_query.data == 'btn_3':
        # Создание новой инлайн-клавиатуры с тремя кнопками
        new_keyboard = create_inline_kb(3,1, 'but_1', 'but_2', 'but_3')
        await callback_query.message.edit_text(
            text='Выберите одну из кнопок:',
            reply_markup=new_keyboard
        )
    elif callback_query.data == 'btn_4':
        # Создание новой инлайн-клавиатуры с тремя кнопками
        new_keyboard = create_inline_kb(4,1, 'but_1', 'but_2', 'but_3')
        await callback_query.message.edit_text(
            text='Выберите одну из кнопок:',
            reply_markup=new_keyboard
        )
    elif callback_query.data == 'btn_5':
        # Создание новой инлайн-клавиатуры с тремя кнопками
        new_keyboard = create_inline_kb(5,1, 'but_1', 'but_2', 'but_3')
        await callback_query.message.edit_text(
            text='Выберите одну из кнопок:',
            reply_markup=new_keyboard
        )
    elif callback_query.data == 'but_1':
        # Возвращаемся к начальному состоянию с одной кнопкой
        initial_keyboard = create_inline_kb(1,5, **BUTTONS)
        await callback_query.message.edit_text(
            text='Это инлайн-клавиатура',
            reply_markup=initial_keyboard
        )
    elif callback_query.data == 'but_2':
        # Отправляем пословицу
        await callback_query.message.answer("Пословица: \"Тише едешь — дальше будешь.\"")
    elif callback_query.data == 'but_3':
        # Пишем сообщение
        await callback_query.message.answer("Это сообщение в ответ на нажатие кнопки.")

    await callback_query.answer()  # Отправляем ответ на callback