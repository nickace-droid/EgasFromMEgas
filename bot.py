import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Логирование
logging.basicConfig(level=logging.INFO)

# Клавиатура для вызова кальянщика
def get_hookah_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔥 Поменять угли", callback_data="coals")],
        [InlineKeyboardButton("💨 Перезабить кальян", callback_data="reload")],
        [InlineKeyboardButton("📝 Принять заказ", callback_data="order")],
        [InlineKeyboardButton("🚨 Срочная помощь", callback_data="emergency")],
        [InlineKeyboardButton("✏️ Другое", callback_data="other")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура меню
def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🍓 Клубничный микс", callback_data="mix_strawberry")],
        [InlineKeyboardButton("🍉 Арбузный чил", callback_data="mix_watermelon")],
        [InlineKeyboardButton("❄️ Мятная свежесть", callback_data="mix_mint")],
        [InlineKeyboardButton("🍏 Яблочный лед", callback_data="mix_apple")],
        [InlineKeyboardButton("🌟 Мегас Special", callback_data="mix_special")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 Привет! Я Ега из Мегаса\n"
        "Чем могу помочь?",
        reply_markup=get_hookah_keyboard()
    )

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    reasons = {
        "coals": "🔥 Поменять угли",
        "reload": "💨 Перезабить кальян", 
        "order": "📝 Принять заказ",
        "emergency": "🚨 Срочная помощь",
        "other": "✏️ Другое"
    }
    
    if query.data in reasons:
        # Отправляем уведомление в чат кальянщиков
        message = f"🎯 ВЫЗОВ КАЛЬЯНЩИКА\nПричина: {reasons[query.data]}\nСтол: {query.from_user.id}"
        
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )
        
        await query.edit_message_text(f"✅ Кальянщик вызван! Причина: {reasons[query.data]}")
    
    elif query.data.startswith('mix_'):
        mixes = {
            "mix_strawberry": "🍓 Клубничный микс",
            "mix_watermelon": "🍉 Арбузный чил", 
            "mix_mint": "❄️ Мятная свежесть",
            "mix_apple": "🍏 Яблочный лед",
            "mix_special": "🌟 Мегас Special"
        }
        
        await query.edit_message_text(f"✅ Заказан: {mixes[query.data]}\nКальянщик уже готовит!")

# Главная функция
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.run_polling()

if __name__ == "__main__":
    main()
