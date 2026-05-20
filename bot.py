import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from openai import OpenAI
from dotenv import load_dotenv
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios import SCENARIOS
from prompts.base_prompt import BASE_PROMPT
from prompts.levels import LEVELS
from prompts.scenarios_manager import SCENARIOS

from prompts.scenarios.airport import SCENARIO as AIRPORT
from prompts.scenarios.hotel import SCENARIO as HOTEL
from prompts.scenarios.celeb import SCENARIO as CELEB
from prompts.scenarios.choosing_prof import SCENARIO as PROFESSION
from prompts.scenarios.clothes_shop import SCENARIO as CLOTHES
from prompts.scenarios.doctor import SCENARIO as DOCTOR
from prompts.scenarios.ecology import SCENARIO as ECOLOGY
from prompts.scenarios.exam import SCENARIO as EXAM
from prompts.scenarios.family_rules import SCENARIO as FAMILY
from prompts.scenarios.it_safety import SCENARIO as SAFETY
from prompts.scenarios.job_interview import SCENARIO as INTERVIEW
from prompts.scenarios.social_media import SCENARIO as MEDIA
from prompts.scenarios.sports import SCENARIO as SPORTS
from prompts.scenarios.teacher_conversation import SCENARIO as TEACHER
from prompts.scenarios.university import SCENARIO as UNIVERSITY

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
            f"Level {text} selected. Now choose a scenario:",
            reply_markup=scenario_keyboard
        )
        return
    
    if text == "👨‍👩‍👧 Family Rules":
        user_scenarios[user_id] = "family_rules"

    elif text == "🩺 At the Doctor’s":
        user_scenarios[user_id] = "doctor"

    elif text == "👩‍🏫 Talking to a Teacher":
        user_scenarios[user_id] = "teacher"

    elif text == "💼 Choosing a Profession":
        user_scenarios[user_id] = "profession"

    elif text == "🛍 Buying Clothes":
        user_scenarios[user_id] = "clothes"

    elif text == "✈️ Airport Check-in":
        user_scenarios[user_id] = "airport"

    elif text == "🌍 Ecology Discussion":
        user_scenarios[user_id] = "ecology"

    elif text == "📱 Social Media Discussion":
        user_scenarios[user_id] = "social_media"

    elif text == "🏨 Hotel Problem":
        user_scenarios[user_id] = "hotel"

    elif text == "⭐ Famous Person":
        user_scenarios[user_id] = "famous_person"

    elif text == "😰 Exam Stress":
        user_scenarios[user_id] = "exam_stress"

    elif text == "🧑‍💼 Job Interview":
        user_scenarios[user_id] = "job_interview"

    elif text == "🔒 Internet Safety":
        user_scenarios[user_id] = "internet_safety"

    elif text == "⚽ Sports Discussion":
        user_scenarios[user_id] = "sports"

    elif text == "🎓 University Open Day":
        user_scenarios[user_id] = "university"

    if user_id not in user_contexts:

        scenario = user_scenarios.get(user_id, "airport")
        scenario_prompt = SCENARIOS[scenario]

        level = user_levels.get(user_id, "A2")
        level_prompt = LEVELS[level]

        system_prompt = f"""
        {BASE_PROMPT}

        {level_prompt}

        {scenario_prompt}
        """

        user_contexts[user_id] = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    user_contexts[user_id].append(
        {"role": "user", "content": text}
    )

    response = client.chat.completions.create(
        model="meta-llama/llama-3.2-3b-instruct",
        messages=user_contexts[user_id],
        temperature=0.7,
        max_tokens=200
    )

    reply = response.choices[0].message.content or "No response"

    user_contexts[user_id].append(
        {"role": "assistant", "content": reply}
    )

    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())