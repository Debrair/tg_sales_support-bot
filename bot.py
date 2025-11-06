import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CoachDBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        
        # Callback query handlers for buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_main_menu, pattern='^main_'))
        self.application.add_handler(CallbackQueryHandler(self.handle_plans_flow, pattern='^plans_'))
        self.application.add_handler(CallbackQueryHandler(self.handle_payments_flow, pattern='^payments_'))
        self.application.add_handler(CallbackQueryHandler(self.handle_technical_flow, pattern='^tech_'))
        self.application.add_handler(CallbackQueryHandler(self.handle_app_navigation, pattern='^app_nav_'))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message with main menu"""
        await self.send_welcome_message(update, context)

    async def send_welcome_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send the welcome greeting and main menu"""
        welcome_text = (
            "¡Hola! Gracias por comunicarte con Coach D. method.\n\n"
            "Estamos listos para ayudarte en tu camino hacia el bienestar. "
            "Por favor, selecciona una opción del menú principal para comenzar.\n\n"
            "**Menú Principal**\n\n"
            "1. Información sobre planes y programas\n"
            "2. Ayuda con pagos\n"
            "3. Soporte técnico (Aplicación, cuenta o dispositivos)\n"
            "4. Otros enlaces (Contacto, Ayuda general)"
        )

        keyboard = [
            [InlineKeyboardButton("1. Información sobre planes y programas", callback_data="main_plans")],
            [InlineKeyboardButton("2. Ayuda con pagos", callback_data="main_payments")],
            [InlineKeyboardButton("3. Soporte técnico", callback_data="main_technical")],
            [InlineKeyboardButton("4. Otros enlaces", callback_data="main_links")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        else:
            await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu selections"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "main_plans":
            await self.show_plans_flow(query)
        elif data == "main_payments":
            await self.show_payments_flow(query)
        elif data == "main_technical":
            await self.show_technical_menu(query)
        elif data == "main_links":
            await self.show_other_links(query)

    async def show_plans_flow(self, query):
        """Show plans and programs flow"""
        text = "¡Excelente! Para darte la información correcta, ¿ya has revisado nuestros folletos (brochures) informativos?"
        
        keyboard = [
            [InlineKeyboardButton("1. No, aún no los he visto", callback_data="plans_no_brochures")],
            [InlineKeyboardButton("2. Sí, pero tengo más preguntas", callback_data="plans_human")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def handle_plans_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle plans flow responses"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "plans_no_brochures":
            text = (
                "Entendido. Aquí tienes los detalles de nuestros servicios principales para que puedas revisarlos:\n\n"
                "* Plan On-Demand: [https://drive.google.com/file/d/1eah6l5FGKRSNFqNuTlSNqCdAIjVNsoxQ/view]\n"
                "* Programa Intensivo de Control de Peso: [https://drive.google.com/file/d/1GqjntjQktb6H48nR9JG-2wmjfnVqJs0g/view]\n\n"
                "Tómate tu tiempo para leerlos. Si tienes dudas después, simplemente escribe 'Ayuda'."
            )
            keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]
            
        elif data == "plans_human":
            text = "Perfecto, por favor espera un momento y un asesor te atenderá para resolver todas tus dudas. (Transferencia a humano)"
            keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def show_payments_flow(self, query):
        """Show payments help flow"""
        text = "Entendido. Para ayudarte mejor con el proceso de pago, ¿has podido ver nuestro video tutorial sobre cómo completarlo?"
        
        keyboard = [
            [InlineKeyboardButton("1. No he visto el tutorial", callback_data="payments_no_tutorial")],
            [InlineKeyboardButton("2. Ya vi el tutorial, pero sigo con dudas", callback_data="payments_human")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def handle_payments_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle payments flow responses"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "payments_no_tutorial":
            text = "¡No hay problema! Puedes ver el tutorial completo y realizar tu pago de forma segura en este enlace: [https://www.coachdmethod.com/checkout-on-demand.html]"
            keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]
            
        elif data == "payments_human":
            text = "Comprendo. Por favor espera un momento y un miembro del equipo te asistirá con el pago. (Transferencia a humano)"
            keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def show_technical_menu(self, query):
        """Show technical support menu"""
        text = (
            "Estamos para ayudarte con la parte técnica. Por favor, indícanos qué tipo de asistencia necesitas.\n\n"
            "1. Ayuda conectando dispositivos\n"
            "2. Ayuda sincronizando MyFitnessPal\n"
            "3. Ayuda navegando la aplicación\n"
            "4. Problemas para acceder a mi cuenta\n"
            "5. Reportar un inconveniente / error"
        )
        
        keyboard = [
            [InlineKeyboardButton("1. Ayuda conectando dispositivos", callback_data="tech_devices")],
            [InlineKeyboardButton("2. Ayuda sincronizando MyFitnessPal", callback_data="tech_myfitnesspal")],
            [InlineKeyboardButton("3. Ayuda navegando la aplicación", callback_data="tech_app_nav")],
            [InlineKeyboardButton("4. Problemas para acceder a mi cuenta", callback_data="tech_human")],
            [InlineKeyboardButton("5. Reportar un inconveniente / error", callback_data="tech_report")],
            [InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def handle_technical_flow(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle technical support selections"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "tech_devices":
            text = "Aquí tienes la guía para conectar dispositivos: [https://coachdmethod.helpsite.com/articles/134459-como-conectar-fitbit-a-la-aplicacion]"
            keyboard = [[InlineKeyboardButton("← Volver a Soporte Técnico", callback_data="main_technical")]]
            
        elif data == "tech_myfitnesspal":
            text = "Aquí tienes la guía para sincronizar MyFitnessPal: [https://coachdmethod.helpsite.com/articles/134448-solucion-de-problemas-myfitnesspal-no-se-sincroniza]"
            keyboard = [[InlineKeyboardButton("← Volver a Soporte Técnico", callback_data="main_technical")]]
            
        elif data == "tech_app_nav":
            text = "Perfecto. Tenemos un video de demostración que explica cómo usar todas las funciones de la aplicación. ¿Ya lo has visto?"
            keyboard = [
                [InlineKeyboardButton("1. No he visto el video", callback_data="app_nav_no_video")],
                [InlineKeyboardButton("2. Sí, pero necesito más ayuda", callback_data="app_nav_human")],
                [InlineKeyboardButton("← Volver a Soporte Técnico", callback_data="main_technical")]
            ]
            
        elif data == "tech_human":
            text = "Por favor espera un momento y un asesor te ayudará con los problemas de acceso a tu cuenta. (Transferencia a humano)"
            keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]
            
        elif data == "tech_report":
            text = "Puedes reportar el inconveniente o error aquí: [https://coachdmethod.helpsite.com/contact]"
            keyboard = [[InlineKeyboardButton("← Volver a Soporte Técnico", callback_data="main_technical")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def handle_app_navigation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle app navigation flow"""
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "app_nav_no_video":
            text = "Aquí tienes el video de demostración: [https://coachdmethod.helpsite.com/articles/134447-introduccion-a-la-aplicacion]"
            keyboard = [[InlineKeyboardButton("← Volver a Soporte Técnico", callback_data="main_technical")]]
            
        elif data == "app_nav_human":
            text = "Por favor espera un momento y un asesor te ayudará con la navegación de la aplicación. (Transferencia a humano)"
            keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    async def show_other_links(self, query):
        """Show other links"""
        text = (
            "Aquí tienes nuestros enlaces de interés:\n\n"
            "* Pagina web: [https://www.coachdmethod.com]\n"
            "* Página de Contacto: [https://coachdmethod.helpsite.com/contact]\n"
            "* Centro de Ayuda: [https://coachdmethod.helpsite.com/categories/31935-support]"
        )
        
        keyboard = [[InlineKeyboardButton("← Volver al Menú Principal", callback_data="main_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    def run(self):
        """Start the bot"""
        self.application.run_polling()

def main():
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set")
        return

    # Create and run bot
    bot = CoachDBot(bot_token)
    logger.info("Bot is starting...")
    bot.run()

if __name__ == '__main__':
    main()
