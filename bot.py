from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8505227641:AAEOxgKBs_nKoxquu7MjJ2deMV4f-ZiKmkI"

active_order = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚚 بوت التوصيل جاهز")

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_order
    if active_order:
        await update.message.reply_text("❌ في طلب شغّال حالياً")
        return

    active_order = True

    keyboard = [
        [InlineKeyboardButton("✅ استلام الطلب", callback_data="take_order")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚚 طلب توصيل جديد\n📍 التفاصيل...\n\nأول من يستلم يضغط الزر 👇",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_order
    query = update.callback_query

    if not active_order:
        await query.answer("الطلب تم استلامه")
        return

    active_order = False
    await query.edit_message_text(
        f"✅ تم استلام الطلب بواسطة: {query.from_user.first_name}"
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("order", order))
    app.add_handler(CallbackQueryHandler(button))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
