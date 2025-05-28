import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from sympy import sympify, SympifyError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7870332594:AAFcbUyP6fh9gZc1SszbDm9OXQtfCY9uM8s"

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    update.message.reply_text(
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

def help_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /help"""
    update.message.reply_text(
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

def solve_math(update: Update, context: CallbackContext) -> None:
    """Обработчик математических выражений"""
    try:
        # Получаем текст сообщения
        expr_text = update.message.text
        
        # Пытаемся вычислить выражение
        expr = sympify(expr_text)
        result = expr.evalf()
        
        # Отправляем результат
        update.message.reply_text(f"Результат: {result}")
        
    except SympifyError:
        update.message.reply_text("Не могу разобрать выражение. Пожалуйста, проверьте правильность ввода.")
    except Exception as e:
        logger.error(f"Ошибка при вычислении: {e}")
        update.message.reply_text("Произошла ошибка при вычислении. Попробуйте другое выражение.")

def main() -> None:
    """Запуск бота"""
    # Создаем Updater и передаем ему токен бота
    updater = Updater(TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, solve_math))

    # Запускаем бота
    updater.start_polling()

    # Бот работает до принудительной остановки
    updater.idle()

if __name__ == '__main__':
    main()
