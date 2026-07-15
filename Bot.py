from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8915153077: AAHjedqJvz-qwrsmKbaaSf esT_mM9aaQ8qY"
ADMIN_ID = 1003007082

PHONE, PACKAGE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛒 Buy Internet"]]

    await update.message.reply_text(
        "Ku soo dhawoow Somnet Internet Bot",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

async def buy(update, context):
    await update.message.reply_text(
        "Fadlan geli lambarka Somnet:"
    )
    return PHONE

async def phone(update, context):
    context.user_data["phone"] = update.message.text

    keyboard = [
        ["24-saacadood - $0.5"],
        ["6-saacadood - $0.2"],
        ["12-saacadood - $0.35"]
        ["15-maalin - $7.5"],
    ]

    await update.message.reply_text(
        "Dooro xirmada:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

    return PACKAGE

async def package(update, context):
    pkg = update.message.text

    context.user_data["package"] = pkg

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Waan bixiyay",
                callback_data="paid"
            )
        ]
    ])

    await update.message.reply_text(
        "Lacagta ku dir:\n25261XXXXXXX\n\nKadib riix Waan bixiyay",
        reply_markup=keyboard
    )

    return ConversationHandler.END

async def paid(update, context):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    phone = context.user_data.get("phone")
    pkg = context.user_data.get("package")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Completed",
                callback_data=f"done_{user.id}"
            )
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
ORDER CUSUB

Magac: {user.full_name}
Username: @{user.username}

Lambar: {phone}
Xirmo: {pkg}
        """,
        reply_markup=keyboard
    )

    await query.message.reply_text(
        "Order-kaaga waa la helay."
    )

async def completed(update, context):
    query = update.callback_query

    await query.answer()

    user_id = int(
        query.data.replace("done_", "")
    )

    await context.bot.send_message(
        chat_id=user_id,
        text="✅ Internet-kaaga waa lagu shubay. Mahadsanid."
    )

    await query.edit_message_text(
        "Order completed."
    )

app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("🛒 Buy Internet"),
            buy
        )
    ],
    states={
        PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                phone
            )
        ],
        PACKAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                package
            )
        ]
    },
    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv)
app.add_handler(
    CallbackQueryHandler(
        paid,
        pattern="paid"
    )
)
app.add_handler(
    CallbackQueryHandler(
        completed,
        pattern="done_"
    )
)

app.run_polling()