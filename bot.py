import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts.airport import SYSTEM_PROMPT
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from scenarios import SCENARIOS

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_scenarios = {}

scenario_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✈ Airport")],
        [KeyboardButton(text="🏨 Hotel")],
        [KeyboardButton(text="🍽 Restaurant")]
    ],
    resize_keyboard=True
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.aitunnel.ru/v1/",
)

user_contexts = {}

@dp.message()
async def chat(message: Message):

    user_id = message.from_user.id
    text = message.text

    if text == "✈ Airport":
        user_scenarios[user_id] = "airport"
        await message.answer("Airport scenario selected. Let's start!")
        return

    elif text == "🏨 Hotel":
        user_scenarios[user_id] = "hotel"
        await message.answer("Hotel scenario selected. Let's start!")
        return

    elif text == "🍽 Restaurant":
        user_scenarios[user_id] = "restaurant"
        await message.answer("Restaurant scenario selected. Let's start!")
        return

    if user_id not in user_contexts:

        scenario = user_scenarios.get(user_id, "airport")
        system_prompt = SCENARIOS[scenario]

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