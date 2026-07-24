import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackQueryHandler, CommandHandler, PreCheckoutQueryHandler, MessageHandler, filters

# التوكن الخاص بك
BOT_TOKEN = "8631033587:AAFPlnhYB_BRpeG3NxYVJdnMr-k-Z89V07k"

# قاعدة بيانات لحفظ عدد المستخدمين الفريدين
users_database = set()

# القائمة الرئيسية
def get_main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎓 الكليات والمسارات الأكاديمية", callback_data="colleges"),
            InlineKeyboardButton("📺 قنوات وكورسات اليوتيوب", callback_data="youtube_courses")
        ],
        [
            InlineKeyboardButton("🛠️ المختبرات والأدوات العملية", callback_data="labs_tools"),
            InlineKeyboardButton("📚 المكتبة الرقمية والكتب", callback_data="library")
        ],
        [
            InlineKeyboardButton("🏆 الساحات والتحديات (CTF)", callback_data="ctf_arena"),
            InlineKeyboardButton("📝 الامتحانات والاختبارات القصيرة", callback_data="quizzes")
        ],
        [
            InlineKeyboardButton("💡 نصائح وإرشادات التخرج", callback_data="tips"),
            InlineKeyboardButton("⭐ دعم وتبرع بالنجوم", callback_data="donate_stars")
        ]
    ])

def get_back_btn():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏛️ العودة لبهو الجامعة الرئيسي", callback_data="back_home")]])

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_database.add(user_id)
    
    welcome_text = (
        "🏛️ **أهلاً بك في أكاديمية وجامعة الأمن السيبراني الرقمية (Cyber University)** 🛡️✨\n\n"
        "هذا الصرح البرمجي مُصمم ليأخذ بيد الطالب من الصفر المطلق وحتى الاحتراف.\n"
        "اختر الكلية أو القسم الذي تود استكشافه أدناه:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# أمر /stats لمعرفة عدد المستخدمين
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(users_database)
    await update.message.reply_text(
        f"📊 **إحصائيات الأكاديمية السيبرانية:**\n\n"
        f"👥 عدد الأشخاص الذين استخدموا البوت حتى الآن: **{total_users}** طالب وطالبة 🛡️",
        parse_mode="Markdown"
    )

# معالجة الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "colleges":
        text = (
            "🎓 **كليات ومسارات الجامعة (Roadmaps):**\n\n"
            "1️⃣ **كلية علوم الحاسب والشبكات:** (OSI, TCP/IP, DNS, Subnetting)\n"
            "2️⃣ **كلية أنظمة التشغيل:** إتقان نظام Linux وسطر الأوامر.\n"
            "3️⃣ **كلية أمن الويب:** ثغرات OWASP Top 10 (SQLi, XSS).\n"
            "4️⃣ **كلية الهجمات والدفاع:** Penetration Testing & Forensics."
        )
    elif data == "youtube_courses":
        text = (
            "📺 **قاعات المحاضرات المرئية:**\n\n"
            "• قناة NetworkChuck للشبكات واللينكس.\n"
            "• قناة John Hammond لتحديات CTF.\n"
            "• منصة PortSwigger Academy لأمن الويب."
        )
    elif data == "labs_tools":
        text = (
            "🛠️ **المختبرات والأدوات:**\n\n"
            "• أنظمة: Kali Linux / Parrot OS\n"
            "• أدوات: Nmap, Wireshark, Burp Suite\n"
            "• منصات: TryHackMe & HackTheBox"
        )
    elif data == "library":
        text = "📚 **المكتبة الرقمية:**\n\n• Linux Basics for Hackers\n• The Web Application Hacker's Handbook"
    elif data == "ctf_arena":
        text = "🏆 **ساحة التحديات (CTF):**\n\n• PicoCTF\n• OverTheWire (Bandit)"
    elif data == "quizzes":
        quiz_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🧠 ابدأ اختبار الشبكات السريع", callback_data="start_quiz_net")],
            [InlineKeyboardButton("⬅️ رجوع لبهو الجامعة", callback_data="back_home")]
        ])
        await query.edit_message_text("📝 **قاعة الاختبارات والامتحانات السريعة:**", reply_markup=quiz_kb, parse_mode="Markdown")
        return
    elif data == "start_quiz_net":
        await query.answer("سؤال 1: البروتوكول المسؤول عن تحويل الأسماء إلى آيبات؟ الجواب: DNS", show_alert=True)
        return
    elif data == "tips":
        text = "💡 **إرشادات العمادة:**\n1. لا تدرس كل شيء دفعة واحدة.\n2. التطبيق العملي أهم بـ 80%.\n3. الصبر والاستمرار."
    elif data == "donate_stars":
        text = "⭐ **صندوق دعم الأكاديمية (Telegram Stars):**\nاختر حجم الدعم المناسب:"
        donate_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ 10 نجوم", callback_data="pay_star_10"),
             InlineKeyboardButton("⭐ 50 نجمة", callback_data="pay_star_50")],
            [InlineKeyboardButton("⭐ 100 نجمة", callback_data="pay_star_100"),
             InlineKeyboardButton("⭐ 200 نجمة", callback_data="pay_star_200")],
            [InlineKeyboardButton("⭐ 400 نجمة", callback_data="pay_star_400"),
             InlineKeyboardButton("⭐ 800 نجمة", callback_data="pay_star_800")],
            [InlineKeyboardButton("⭐ 1900 نجمة", callback_data="pay_star_1900"),
             InlineKeyboardButton("⭐ 3400 نجمة", callback_data="pay_star_3400")],
            [InlineKeyboardButton("⬅️ العودة للبهو", callback_data="back_home")]
        ])
        await query.edit_message_text(text, reply_markup=donate_kb, parse_mode="Markdown")
        return
    elif data.startswith("pay_star_"):
        stars_amt = int(data.split("_")[2])
        try:
            await context.bot.send_invoice(
                chat_id=query.message.chat_id,
                title=f"دعم الأكاديمية بـ {stars_amt} نجمة ⭐",
                description="شكراً لكونك جزءاً من جامعة الأمن السيبراني! دعمك يساعدنا على الاستمرار.",
                payload=f"support_stars_{stars_amt}",
                currency="XTR",
                prices=[LabeledPrice(f"دعم {stars_amt} نجوم", stars_amt)]
            )
        except Exception as e:
            await query.answer(f"خطأ في إنشاء الفاتورة: {e}", show_alert=True)
        return
    elif data == "back_home":
        await query.edit_message_text(
            "🏛️ **أهلاً بك مجدداً في بهو أكاديمية الأمن السيبراني (Cyber University)** 🛡️✨\n\nاختر الكلية أو القسم:",
            reply_markup=get_main_menu(), parse_mode="Markdown"
        )
        return

    await query.edit_message_text(text, reply_markup=get_back_btn(), parse_mode="Markdown")

# معالجة الدفع بالنجوم
async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    await update.message.reply_text(f"🎉 ألف شكر! تم استلام دعمك بـ **{payment.total_amount} نجمة** بنجاح ⭐🛡️", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    print("🤖 Bot is running successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
