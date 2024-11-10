from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ChatMemberHandler
import random
import string

# Dictionary to store unique invite codes for each user
user_invite_codes = {}
invite_referrals = {}  # Store who invited whom

# Generate a unique invite code for each user
def generate_invite_code(user_id: int):
    # Generate a random code of length 6 (you can increase the length if you want)
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    user_invite_codes[user_id] = code
    return code

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Before you start using the bot, first subscribe to the channel:\n\n"
        "https://t.me/+zNppIA2Gk_4xODVh\n\n"
        "To see a list of all commands, use /commands."
    )

# /commands command - Lists all available commands
async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = (
        "Here are the available commands:\n\n"
        "/start - Start the bot and get instructions.\n"
        "/pay - Show payment options for hacks.\n"
        "/redeem - Redeem your payment using a gift card or crypto.\n"
        "/faq - Frequently asked questions.\n"
        "/invite - Get your personal invite link to earn rewards.\n"
        "/commands - List all available commands."
    )
    await update.message.reply_text(commands_text)

# /pay command with inline buttons for different payment methods
async def pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the inline buttons including the new "Pay without Crypto" button
    keyboard = [
        [InlineKeyboardButton("BTC", callback_data="BTC"),
         InlineKeyboardButton("ETH", callback_data="ETH")],
        [InlineKeyboardButton("SOL", callback_data="SOL"),
         InlineKeyboardButton("LTC", callback_data="LTC")],
        [InlineKeyboardButton("Pay without Crypto", callback_data="NON_CRYPTO")]  # New button
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline buttons
    await update.message.reply_text(
        "Purchase your own hack for $50 each or $100 for three hacks!\n\n"
        "To buy access, select a payment method below",
        reply_markup=reply_markup
    )

# /redeem command response
async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please DM me on Telegram: https://t.me/DM_SnapCracker\n\n"
        "Or join my Discord server: https://discord.gg/snapcracker"
    )

# /faq command response
async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send FAQ page response
    faq_text = (
        "Welcome to our FAQ page!\n"
        "Feel free to look at some of our frequently asked questions down below.\n\n"
        "Question 1: How does this work?\n"
        "Answer: To start a hack enter /hack + the username of the person.\n\n"
        "Question 2: How long does a hack take?\n"
        "Answer: Hacking usually takes about 3-5 minutes.\n\n"
        "Question 3: Will the person know I've hacked their account?\n"
        "Answer: No, our bot is completely anonymous.\n\n"
        "Question 4: How do I pay for a hack?\n"
        "Answer: The bot will prompt you to choose a payment option after a successful hack."
    )
    await update.message.reply_text(faq_text)

# Handle payment choice based on user selection (inline button handler)
async def handle_payment_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.callback_query.data  # Get the payment choice

    # Acknowledge the callback query
    await update.callback_query.answer()

    # Prepare the payment instructions based on the selected payment method
    if choice == "LTC":
        payment_message = "Pay to this crypto address: ltc1q4rgt70j0xvv6zvdp4jg66rzeu3yx9xe2rrxjpg\n\nAfter you’ve sent the payment, please use /redeem"
    elif choice == "BTC":
        payment_message = "Pay to this crypto address: bc1qwwhc0z6mfwrptefxjw33f9n4puqtwzwnxlty4r\n\nAfter you’ve sent the payment, please use /redeem"
    elif choice == "ETH":
        payment_message = "Pay to this crypto address: 0xDe44D94573661c5f5FC99e6F56bA4Ab2D8Fc9533\n\nAfter you’ve sent the payment, please use /redeem"
    elif choice == "SOL":
        payment_message = "Pay to this crypto address: F4aPW5dJbnscfo7LwFmRhLQnTp4VWemXTZa5GRFK49A4\n\nAfter you’ve sent the payment, please use /redeem"
    elif choice == "NON_CRYPTO":
        # New response for "Pay without Crypto" button
        payment_message = (
            "You can pay with cryptovoucher.io gift cards. Just use /redeem. "
            "We'll manually verify the code's validity. Current waiting time: 20-30 min."
        )
    else:
        payment_message = "Please select a valid payment method by clicking one of the buttons."

    # Send the payment instructions in a new message
    await update.callback_query.message.reply_text(payment_message)

# Handle when users join the group and capture their unique invite code
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for new_member in update.message.new_chat_members:
        if new_member.is_bot:
            continue

        # Check if the user joined using an invite link with a start parameter
        start_param = update.message.text.split("start=")  # This will capture the start parameter from the URL
        
        if len(start_param) > 1:
            invite_code = start_param[1]  # Get the invite code from the URL
            # Store who invited the user
            invite_referrals[new_member.id] = invite_code

            # Log the referral (you can store this in a database or file for persistence)
            print(f"User {new_member.id} joined using invite code {invite_code}")
            
            # Respond to the new member with a thank-you message and info
            await update.message.reply_text(
                f"Welcome {new_member.first_name}! You joined using the invite link with code {invite_code}. "
                "Thank you for joining! You can now start using the bot."
            )

# /invite command - Sends the personal invite link
async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # Generate a unique invite code for the user if they don't have one
    if user_id not in user_invite_codes:
        generate_invite_code(user_id)
    
    # Generate the unique invite link with the invite code
    invite_code = user_invite_codes[user_id]
    personal_invite_link = f"https://t.me/SnapchatCracker_bot?start={invite_code}"  # Replace with your bot's username
    
    # Send the invite message with the link
    await update.message.reply_text(
        f"Earn a hack free of charge if you invite 10 new people to our bot via your link.\n\n"
        f"Here is your personal invitation link: {personal_invite_link}"
    )

# Main function to start the bot
def main():
    # Create the application with your bot's token
    application = Application.builder().token("7599242956:AAFvbHrq7F16JwEYukrbI9OTX0KZcQLeu_4").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("pay", pay_command))
    application.add_handler(CommandHandler("redeem", redeem_command))
    application.add_handler(CommandHandler("faq", faq_command))  # Added /faq command handler
    application.add_handler(CommandHandler("invite", invite_command))  # Added /invite command handler
    application.add_handler(CommandHandler("commands", commands_command))  # Added /commands command handler

    # Add a callback handler for inline button presses
    application.add_handler(CallbackQueryHandler(handle_payment_choice))

    # Add a handler for when users join the group
    application.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.MY_CHAT_MEMBER))

    # Start the bot
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
