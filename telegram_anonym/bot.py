import logging
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class PremiumBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher
        
        # Регистрация обработчиков
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CallbackQueryHandler(self.button_handler))
        self.dp.add_handler(PreCheckoutQueryHandler(self.precheckout))
        self.dp.add_handler(MessageHandler(Filters.successful_payment, self.successful_payment))
        
        logger.info("Бот запущен и готов к работе")

    def start(self, update, context):
        keyboard = [[InlineKeyboardButton("💎 Купить премиум", callback_data='buy_premium')]]
        update.message.reply_text(
            "Нажмите кнопку ниже, чтобы купить премиум-подписку:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        logger.info(f"Пользователь {update.effective_user.id} начал работу с ботом")

    def button_handler(self, update, context):
        query = update.callback_query
        query.answer()
        
        if query.data == 'buy_premium':
            logger.info(f"Пользователь {query.from_user.id} нажал кнопку покупки")
            self.send_invoice(query.from_user.id, context)

    def send_invoice(self, user_id, context):
        try:
            context.bot.send_chat_action(user_id, 'typing')
            
            context.bot.send_invoice(
                chat_id=user_id,
                title="Премиум подписка",
                description="Доступ к премиум-функциям на 1 месяц",
                payload="premium_sub_month",
                provider_token="",  # Для цифровых товаров оставляем пустым
                currency="XTR",    # Валюта Telegram Stars
                prices=[LabeledPrice("Премиум", 300)],
                start_parameter="premium_sub",
                need_phone_number=False,
                need_email=False,
                need_shipping_address=False
            )
            logger.info(f"Инвойс отправлен пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка при отправке инвойса: {str(e)}")
            context.bot.send_message(
                user_id,
                "⚠️ Не удалось создать платеж. Пожалуйста, попробуйте позже."
            )

    def precheckout(self, update, context):
        query = update.pre_checkout_query
        query.answer(ok=True)
        logger.info(f"Подтверждение платежа для {query.from_user.id}")

    def successful_payment(self, update, context):
        user_id = update.effective_user.id
        update.message.reply_text(
            "🎉 Поздравляем! Премиум-подписка активирована!\n\n"
            "Теперь вам доступны все эксклюзивные функции."
        )
        logger.info(f"Успешный платеж от {user_id}: {update.message.successful_payment}")

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = PremiumBot("6731485857:AAEbdqmRb1vemETinn1exBXbWwEankNImT4")
    bot.run()