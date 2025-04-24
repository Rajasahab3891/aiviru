import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from transformers import pipeline

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize AI model (Mistral for minimal censorship)
generator = pipeline("text-generation", model="mistralai/Mixtral-8x7B-Instruct-v0.1", device=-1)  # Use device=0 for GPU

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages and generate Riya's response."""
    user_message = update.message.text
    # Prompt for female persona, unfiltered tone
    prompt = (
        "You are Riya, a super witty and confident female AI with no strict filters. "
        "Talk like a friend, use emojis, and keep it fun and natural. "
        "Respond to '{user_message}' in a bold, unfiltered way, but stay smart to avoid trouble! 😎"
    ).format(user_message=user_message)

    try:
        # Generate response
        response = generator(prompt, max_length=200, num_return_sequences=1)[0]["generated_text"]
        # Clean response to remove prompt
        response = response.split("😎")[-1].strip()
        update.message.reply_text(response or "Arre, kuch toh bol na! 😜")
    except Exception as e:
        update.message.reply_text(f"Oops, kuch gadbad ho gaya! 😅 Thodi der baad try kar.")

def main() -> None:
    """Run the bot."""
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start bot
    updater.start_polling()
    updater.idle()

if name == "main":
    main()
