import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from openai import OpenAI
from dotenv import load_dotenv
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from prompts.base_prompt import BASE_PROMPT
from prompts.levels import LEVELS
from prompts.scenarios_manager import SCENARIOS

from prompts.scenarios.airport import SYSTEM_PROMPT as AIRPORT
from prompts.scenarios.hotel import SYSTEM_PROMPT as HOTEL
from prompts.scenarios.celeb import SYSTEM_PROMPT as CELEB
from prompts.scenarios.choosing_prof import SYSTEM_PROMPT as PROFESSION
from prompts.scenarios.clothes_shop import SYSTEM_PROMPT as CLOTHES
from prompts.scenarios.doctor import SYSTEM_PROMPT as DOCTOR
from prompts.scenarios.ecology import SYSTEM_PROMPT as ECOLOGY
from prompts.scenarios.exam import SYSTEM_PROMPT as EXAM
from prompts.scenarios.family_rules import SYSTEM_PROMPT as FAMILY
from prompts.scenarios.it_safety import SYSTEM_PROMPT as SAFETY
from prompts.scenarios.job_interview import SYSTEM_PROMPT as INTERVIEW
from prompts.scenarios.social_media import SYSTEM_PROMPT as MEDIA
from prompts.scenarios.sports import SYSTEM_PROMPT as SPORTS
from prompts.scenarios.teacher_conversation import SYSTEM_PROMPT as TEACHER
from prompts.scenarios.university import SYSTEM_PROMPT as UNIVERSITY

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_scenarios = {}
user_levels = {}

level_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A2")],
        [KeyboardButton(text="B1")],
        [KeyboardButton(text="B2")]
    ],
    resize_keyboard=True
)

scenario_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨‍👩‍👧 Family Rules")],
        [KeyboardButton(text="🩺 At the Doctor’s")],
        [KeyboardButton(text="👩‍🏫 Talking to a Teacher")],
        [KeyboardButton(text="💼 Choosing a Profession")],
        [KeyboardButton(text="🛍 Buying Clothes")],
        [KeyboardButton(text="✈️ Airport Check-in")],
        [KeyboardButton(text="🌍 Ecology Discussion")],
        [KeyboardButton(text="📱 Social Media Discussion")],
        [KeyboardButton(text="🏨 Hotel Problem")],
        [KeyboardButton(text="⭐ Famous Person")],
        [KeyboardButton(text="😰 Exam Stress")],
        [KeyboardButton(text="🧑‍💼 Job Interview")],
        [KeyboardButton(text="🔒 Internet Safety")],
        [KeyboardButton(text="⚽ Sports Discussion")],
        [KeyboardButton(text="🎓 University Open Day")]
    ],
    resize_keyboard=True
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.aitunnel.ru/v1/",
)

user_contexts = {}

def build_system_prompt(user_id: int):
    scenario = user_scenarios.get(user_id, "airport")
    level = user_levels.get(user_id, "A2")

    scenario_prompt = SCENARIOS[scenario]
    level_prompt = LEVELS[level]

    return f"""
    {BASE_PROMPT}

    {level_prompt}

    {scenario_prompt}
    """

def reset_context(user_id: int):
    if user_id not in user_levels:
        return
    if user_id not in user_scenarios:
        return
    user_contexts[user_id] = [
        {"role": "system", "content": build_system_prompt(user_id)}
    ]

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Choose your English level:",
        reply_markup=level_keyboard
    )

@dp.message()
async def chat(message: Message):

    user_id = message.from_user.id
    text = message.text

    if text in ["A2", "B1", "B2"]:
        user_levels[user_id] = text

        await message.answer(
            "Level selected. Now choose scenario:",
            reply_markup=scenario_keyboard   # 🔥 ВАЖНО
        )
        return
    
    if text == "👨‍👩‍👧 Family Rules":
        user_scenarios[user_id] = "family_rules"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🩺 At the Doctor’s":
        user_scenarios[user_id] = "doctor_appointment"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "👩‍🏫 Talking to a Teacher":
        user_scenarios[user_id] = "teacher_conversation"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "💼 Choosing a Profession":
        user_scenarios[user_id] = "choosing_profession"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🛍 Buying Clothes":
        user_scenarios[user_id] = "buying_clothes"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "✈️ Airport Check-in":
        user_scenarios[user_id] = "airport"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🌍 Ecology Discussion":
        user_scenarios[user_id] = "ecology_discussion"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "📱 Social Media Discussion":
        user_scenarios[user_id] = "social_media_discussion"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🏨 Hotel Problem":
        user_scenarios[user_id] = "hotel"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "⭐ Famous Person":
        user_scenarios[user_id] = "famous_person"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "😰 Exam Stress":
        user_scenarios[user_id] = "final_exam"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🧑‍💼 Job Interview":
        user_scenarios[user_id] = "job_interview"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🔒 Internet Safety":
        user_scenarios[user_id] = "internet_safety"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "⚽ Sports Discussion":
        user_scenarios[user_id] = "sports_discussion"
        if user_id in user_levels:
            reset_context(user_id)

    elif text == "🎓 University Open Day":
        user_scenarios[user_id] = "university_open_day"
        if user_id in user_levels:
            reset_context(user_id)

    user_contexts[user_id].append({"role": "user", "content": text})

    if user_id not in user_contexts:
        reset_context(user_id)

    scenario = user_scenarios.get(user_id)
    level = user_levels.get(user_id)

    if not scenario or not level:
        await message.answer("Please select level and scenario first.")
        return
    
    response = client.chat.completions.create(
        model="openai/gpt-5.3-chat",
        messages=user_contexts[user_id],
        temperature=0.7,
        max_tokens=200
    )

    reply = response.choices[0].message.content or "No response"

    user_contexts[user_id].append(
        {"role": "assistant", "content": reply}
    )

    print(user_contexts[user_id])

    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())