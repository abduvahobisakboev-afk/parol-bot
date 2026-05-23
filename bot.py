import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from utils import analyze_password

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Botni sozlash
bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔒 Loyiha haqida", callback_query_data="about_project"),
            InlineKeyboardButton(text="💡 Maslahatlar", callback_query_data="security_tips")
        ]
    ])

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    welcome_text = (
        f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
        f"🛡 <b>Parol Simulyatori Botiga xush kelibsiz!</b>\n\n"
        f"Menga tekshirib ko'rmoqchi bo'lgan parolingizni yuboring. "
        f"Men uni zamonaviy superkompyuterlar qancha vaqtda buzolishini (Brute force) "
        f"<b>yil, oy va kunlarda</b> hisoblab beraman.\n\n"
        f"⚠️ <i>Xavfsizlik uchun: Haqiqiy shaxsiy parollaringizni yubormang!</i>"
    )
    await message.answer(text=welcome_text, reply_markup=get_main_menu())

@dp.message(F.text)
async def password_handler(message: Message) -> None:
    password = message.text
    if password.startswith('/'):
        return

    processing_msg = await message.answer("🔄 Parol tahlil qilinmoqda, kuting...")
    
    try:
        res = analyze_password(password)
        lower_status = "✅" if res["has_lower"] else "❌"
        upper_status = "✅" if res["has_upper"] else "❌"
        digit_status = "✅" if res["has_digits"] else "❌"
        special_status = "✅" if res["has_special"] else "❌"

        response_text = (
            f"📊 <b>PAROL TAHLILI NATIJASI</b>\n"
            f"----------------------------------------\n"
            f"🔑 <b>Kiritilgan parol:</b> ||{html.quote(password)}||\n"
            f"📏 <b>Uzunligi:</b> {res['length']} ta belgi\n"
            f"🛡 <b>Reyting:</b> {res['rating']}\n\n"
            f"🔢 <b>Tarkibi:</b>\n"
            f"└ Kichik harflar [a-z]: {lower_status}\n"
            f"└ Katta harflar [A-Z]: {upper_status}\n"
            f"└ Raqamlar [0-9]: {digit_status}\n"
            f"└ Maxsus belgilar: {special_status}\n\n"
            f"⏰ <b>Buzib o'tish uchun ketadigan vaqt:</b>\n"
            f"👉 <code>{res['time_formatted']}</code>\n"
            f"----------------------------------------\n"
            f"ℹ️ <i>Ushbu vaqt sekundiga 10 mlrd kombinatsiya tekshira oladigan tizim uchun hisoblangan.</i>"
        )
        await processing_msg.edit_text(text=response_text)
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        await processing_msg.edit_text("❌ Hisoblashda xatolik yuz berdi.")

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())