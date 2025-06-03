import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from sympy import sympify, SympifyError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7870332594:AAFcbUyP6fh9gZc1SszbDm9OXQtfCY9uM8s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Я - математический бот. Отправь мне математическое выражение, "
        "и я попробую его решить.\n\n"
        "Примеры:\n"
        "• 2 + 2 * 2\n"
        "• sqrt(16)\n"
        "• sin(pi/2)\n"
        "• integrate(x**2, x)\n"
        "• diff(x**2, x)\n\n"
        "Поддерживаются основные операции, тригонометрия, логарифмы, "
        "производные и интегралы."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        "Просто отправьте мне математическое выражение, и я попробую его вычислить.\n\n"
        "Доступные функции:\n"
        "• Основные операции: +, -, *, /, ^ или **\n"
        "• Тригонометрия: sin, cos, tan, asin, acos, atan\n"
        "• Логарифмы: log, ln\n"
        "• Корни: sqrt\n"
        "• Константы: pi, E, I\n"
        "• Производные: diff(f(x), x)\n"
        "• Интегралы: integrate(f(x), x)\n\n"
        "Примеры:\n"
        "2*(3+4)\n"
        "sin(pi/2) + cos(0)\n"
        "integrate(x^2, x)"
    )

async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик математических выражений"""
    try:
        # Получаем текст сообщения
        expr_text = update.message.text
        
        # Пытаемся вычислить выражение
        expr = sympify(expr_text)
        result = expr.evalf()
        
        # Отправляем результат
        await update.message.reply_text(f"Результат: {result}")
        
    except SympifyError:
        await update.message.reply_text("Не могу разобрать выражение. Пожалуйста, проверьте правильность ввода.")
    except Exception as e:
        logger.error(f"Ошибка при вычислении: {e}")
        await update.message.reply_text("Произошла ошибка при вычислении. Попробуйте другое выражение.")

def main() -> None:
    """Запуск бота"""
    # Создаем Application и передаем ему токен бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
