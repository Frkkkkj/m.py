import stripe
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(King)

# Set your Stripe API Key here
stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'

# Replace with your Telegram Bot token
TELEGRAM_TOKEN = '6893021876:AAEd87lWg7HePmK76fjuM5g53WWv_bTdcDY'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send /pay <amount> to make a payment.")

def pay(update: Update, context: CallbackContext):
    if context.args:
        try:
            amount = int(context.args[0])  # Amount to be paid in cents (e.g., 100 for $1)
            
            # Create a PaymentIntent on Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method_types=["card"],
            )
            
            # Provide user with Stripe's client secret to complete the payment
            client_secret = payment_intent.client_secret
            update.message.reply_text(f"Payment of ${amount / 100} has been initiated. Please complete the payment.\n\nClient Secret: {client_secret}")
        
        except ValueError:
            update.message.reply_text("❌ Please enter a valid amount to pay.")
    else:
        update.message.reply_text("❌ Please provide an amount to pay. Usage: /pay <amount>.")

def handle_payment_confirmation(update: Update, context: CallbackContext):
    """Handles Stripe payment confirmation"""
    try:
        # Assume the user has completed payment using the Stripe client secret
        payment_intent_id = context.args[0]  # This should be the payment intent ID or status
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status == "succeeded":
            update.message.reply_text("✅ Payment successful! Thank you for your purchase.")
        elif payment_intent.status == "requires_payment_method":
            update.message.reply_text("❌ Payment failed: The card was declined.")
        else:
            update.message.reply_text(f"❌ Payment failed: {payment_intent.status}. Please try again.")
    
    except Exception as e:
        update.message.reply_text(f"❌ An error occurred: {str(e)}")

def main():
    # Create the Updater and pass in your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pay", pay))
    dispatcher.add_handler(CommandHandler("confirm_payment", handle_payment_confirmation, pass_args=True))

    # Start the bot
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()