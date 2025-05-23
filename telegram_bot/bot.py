import logging
from functools import wraps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
# Removed ConversationHandler, MessageHandler, filters as they are not used for signal generation
import database
import telegram_bot.signals as signal_formatter # Renamed for clarity
import telegram_bot.analyzer_service_mock as analyzer_service # Added analyzer service
import random # For random result
from datetime import datetime, timezone # For sent_time in signal_info (optional for now)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "7781421237:AAHDK3NtUOMIuaXwFnXUMg0fTxCv7oRTACI"
OWNER_ID = 24770515

# --- Role-Based Access Control Decorators ---
def restricted_access(required_roles: list[str]):
    """Decorator to restrict access to command handlers based on user roles."""
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            user_role = database.get_user_role(user_id)
            if user_role and user_role in required_roles:
                logger.info(f"User {user_id} with role '{user_role}' accessed {func.__name__}")
                return await func(update, context, *args, **kwargs)
            else:
                logger.warning(
                    f"User {user_id} (role: {user_role}) attempted to access restricted command {func.__name__}."
                    f" Required roles: {required_roles}"
                )
                await update.message.reply_text("You are not authorized to use this command.")
                return
        return wrapper
    return decorator

owner_required = restricted_access(["owner"])
developer_required = restricted_access(["owner", "developer"])
member_required = restricted_access(["owner", "developer", "member"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and initializes the owner if it's the first run for the owner."""
    user_id = update.effective_user.id
    name = update.effective_user.first_name

    # Initialize owner
    if user_id == OWNER_ID and database.get_user_role(OWNER_ID) is None:
        database.add_user(OWNER_ID, "owner")
        await update.message.reply_text(
            f"Hello {name}! You have been registered as the bot owner. Welcome!"
        )
        logger.info(f"Owner {OWNER_ID} initialized.")
    elif database.get_user_role(user_id):
        await update.message.reply_text(f"Welcome back, {name}!")
    else:
        # For other users, consider adding them as 'member' by default or having a different flow
        database.add_user(user_id, "member") # Example: add new users as 'member'
        await update.message.reply_text(
            f"Hello {name}! I am your new Telegram bot. You've been added as a member."
        )
        logger.info(f"New user {user_id} added as member.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

# --- Placeholder Commands for User Management ---

@owner_required
async def add_developer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Placeholder: Adds a developer. (Owner only)"""
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Usage: /add_developer <user_id>")
        return
    developer_id_to_add = int(args[0])
    logger.info(f"Owner {user_id} attempting to add developer {developer_id_to_add}.")
    # Actual database.add_user(developer_id_to_add, "developer") will be in control panel
    await update.message.reply_text(f"Placeholder: Attempting to add developer {developer_id_to_add}.")

@owner_required
async def remove_developer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Placeholder: Removes a developer. (Owner only)"""
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Usage: /remove_developer <user_id>")
        return
    developer_id_to_remove = int(args[0])
    logger.info(f"Owner {user_id} attempting to remove developer {developer_id_to_remove}.")
    # Actual database.remove_user(developer_id_to_remove) will be in control panel
    await update.message.reply_text(f"Placeholder: Attempting to remove developer {developer_id_to_remove}.")

@developer_required
async def add_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Placeholder: Adds a member. (Developer/Owner)"""
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Usage: /add_member <user_id>")
        return
    member_id_to_add = int(args[0])
    logger.info(f"User {user_id} attempting to add member {member_id_to_add}.")
    # Actual database.add_user(member_id_to_add, "member") will be in control panel
    await update.message.reply_text(f"Placeholder: Attempting to add member {member_id_to_add}.")

@developer_required
async def remove_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Placeholder: Removes a member. (Developer/Owner)"""
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Usage: /remove_member <user_id>")
        return
    member_id_to_remove = int(args[0])
    logger.info(f"User {user_id} attempting to remove member {member_id_to_remove}.")
    # Actual database.remove_user(member_id_to_remove) will be in control panel
    await update.message.reply_text(f"Placeholder: Attempting to remove member {member_id_to_remove}.")

# --- Channel Management Commands ---
# Note: The bot must be an administrator in the target channel to send messages.
# This is a manual check for the developer when adding a channel. Future enhancements
# could involve trying to fetch bot's status in the channel.

@developer_required
async def add_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Adds a channel to the authorized list. Usage: /add_channel <channel_id> [name]"""
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].startswith('-') or not args[0][1:].isdigit(): # Basic check for channel ID format
        await update.message.reply_text("Usage: /add_channel <channel_id> [optional channel name]\nExample: /add_channel -100123456789 My Channel")
        return

    channel_id = int(args[0])
    channel_name = " ".join(args[1:]) if len(args) > 1 else None

    try:
        database.add_channel(channel_id, channel_name)
        logger.info(f"User {user_id} added channel {channel_id} ('{channel_name}')")
        await update.message.reply_text(f"Channel {channel_id} ('{channel_name or 'N/A'}') has been authorized.")
    except database.sqlite3.IntegrityError:
        logger.warning(f"User {user_id} attempt to add existing channel {channel_id}")
        await update.message.reply_text(f"Channel {channel_id} is already authorized.")
    except Exception as e:
        logger.error(f"Error adding channel {channel_id} by user {user_id}: {e}")
        await update.message.reply_text("An error occurred while adding the channel.")

@developer_required
async def remove_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Removes a channel from the authorized list. Usage: /remove_channel <channel_id>"""
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].startswith('-') or not args[0][1:].isdigit():
        await update.message.reply_text("Usage: /remove_channel <channel_id>\nExample: /remove_channel -100123456789")
        return

    channel_id = int(args[0])
    if database.remove_channel(channel_id):
        logger.info(f"User {user_id} removed channel {channel_id}")
        await update.message.reply_text(f"Channel {channel_id} has been deauthorized.")
    else:
        logger.warning(f"User {user_id} attempt to remove non-existent channel {channel_id}")
        await update.message.reply_text(f"Channel {channel_id} was not found in the authorized list.")

@developer_required
async def list_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all authorized channels."""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} requested channel list.")
    channels = database.list_channels()
    if not channels:
        await update.message.reply_text("No channels are currently authorized.")
        return

    message = "Authorized Channels:\n"
    for ch_id, ch_name in channels:
        message += f"- ID: {ch_id}"
        if ch_name:
            message += f", Name: {ch_name}"
        message += "\n"
    await update.message.reply_text(message)

# --- Test Signal Command ---
@developer_required
async def test_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates and sends a test signal message."""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} triggered /test_signal")

    signal_data = analyzer_service.generate_mock_signal() # Use the analyzer service
    message_text, reply_markup_dict = signal_formatter.format_signal_message(signal_data) # Use the formatter
    
    # Convert the dict to an InlineKeyboardMarkup object
    # The format_signal_message in signals.py should return a dict like:
    # {"inline_keyboard": [[{"text": "Button1", "url": "url1"}]]}
    # This needs to be reconstructed into InlineKeyboardButton and InlineKeyboardMarkup objects
    
    keyboard_buttons = []
    for row in reply_markup_dict["inline_keyboard"]:
        button_row = []
        for button_info in row:
            button_row.append(InlineKeyboardButton(text=button_info["text"], url=button_info["url"]))
        keyboard_buttons.append(button_row)
    
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    await update.message.reply_text(message_text, reply_markup=reply_markup)

# --- Send Signal Command ---
@developer_required
async def send_signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a signal and sends it to all authorized channels."""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} triggered /send_signal")

    # The JobQueue handles pending items. A separate PENDING_SIGNAL_RESULTS list is not strictly necessary
    # for this implementation but could be useful for other management tasks not covered here.
    # For example: if not hasattr(context.application, 'pending_signal_jobs_info'):
    # context.application.pending_signal_jobs_info = [] # Conceptual list

    authorized_channels_tuples = database.list_channels() # List of (channel_id, channel_name)
    if not authorized_channels_tuples:
        await update.message.reply_text(
            "No channels are authorized to receive signals. "
            "Add channels using the control panel or /add_channel command."
        )
        return

    signal_data = analyzer_service.generate_mock_signal() # Use the analyzer service
    message_text, reply_markup_dict = signal_formatter.format_signal_message(signal_data) # Use the formatter
    
    # Parse duration string (e.g., "1Min", "2Min") to seconds
    duration_str = signal_data['duration']
    signal_duration_seconds = 60 # Default
    try:
        if "Min" in duration_str:
            minutes = int(duration_str.replace("Min", ""))
            signal_duration_seconds = minutes * 60
        # Add more parsing if other formats like "Sec" or "Hour" are introduced
    except ValueError:
        logger.error(f"ValueError parsing duration string: {duration_str}. Defaulting to 60s.")
        # Keep default of 60s if parsing fails

    # Convert the dict to an InlineKeyboardMarkup object
    keyboard_buttons = []
    for row in reply_markup_dict["inline_keyboard"]:
        button_row = []
        for button_info in row:
            button_row.append(InlineKeyboardButton(text=button_info["text"], url=button_info["url"]))
        keyboard_buttons.append(button_row)
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    successful_sends = 0
    failed_channels = []

    for channel_id, channel_name in authorized_channels_tuples:
        try:
            sent_message = await context.bot.send_message(
                chat_id=channel_id,
                text=message_text,
                reply_markup=reply_markup
            )
            logger.info(f"Signal sent successfully to channel {channel_id} ('{channel_name or 'N/A'}'). Message ID: {sent_message.message_id}")
            successful_sends += 1

            # Schedule the result message
            job_name = f"result_{sent_message.chat.id}_{sent_message.message_id}"
            context.job_queue.run_once(
                send_signal_result_callback,
                signal_duration_seconds,
                data={
                    'chat_id': sent_message.chat.id,
                    'message_id': sent_message.message_id,
                    'pair': signal_data['pair']
                },
                name=job_name
            )
            logger.info(f"Scheduled result for signal in channel {channel_id} (Pair: {signal_data['pair']}) for {signal_duration_seconds}s. Job: {job_name}")

        except Exception as e:
            logger.error(f"Failed to send signal or schedule result for channel {channel_id} ('{channel_name or 'N/A'}'): {e}")
            failed_channels.append(f"{channel_name or 'Unknown Name'} (ID: {channel_id}) - Error: {type(e).__name__}")

    summary_message = f"Signal sending process initiated for {successful_sends} channel(s)."
    if failed_channels:
        summary_message += "\nFailed to send/schedule for the following channels:\n" + "\n".join(failed_channels)
    
    await update.message.reply_text(summary_message)

async def send_signal_result_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the result of a trading signal after its duration."""
    job_data = context.job.data
    chat_id = job_data['chat_id']
    original_message_id = job_data['message_id']
    pair = job_data['pair']

    # Randomly determine result
    result_status = random.choice(["ربح✅", "خسارة💔"]) # Profit or Loss

    if result_status == "ربح✅":
        result_text = f"نتيجة الصفقة لـ {pair}: {result_status}"
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=result_text,
                reply_to_message_id=original_message_id
            )
            logger.info(f"Successfully sent PROFIT signal result for {pair} to chat {chat_id}, replying to message {original_message_id}.")
        except Exception as e:
            logger.error(
                f"Failed to send PROFIT signal result for {pair} to chat {chat_id}, replying to message {original_message_id}. Error: {e}"
            )
            # Attempt to send as a new message if replying failed
            try:
                await context.bot.send_message(chat_id=chat_id, text=f"(الرسالة الأصلية قد تكون حذفت) {result_text}")
                logger.info(f"Sent PROFIT signal result for {pair} to chat {chat_id} as new message (original likely deleted).")
            except Exception as e_alt:
                logger.error(f"Failed to send PROFIT signal result for {pair} to chat {chat_id} even as a new message. Error: {e_alt}")
    
    elif result_status == "خسارة💔":
        logger.info(f"Signal for {pair} in chat {chat_id} (msg: {original_message_id}) resulted in a LOSS. Scheduling delayed notification.")
        # Schedule a new job to send the loss message after 2 minutes (120 seconds)
        delayed_job_name = f"delayed_loss_{chat_id}_{original_message_id}"
        context.job_queue.run_once(
            send_delayed_loss_result_callback,
            120, # 2 minutes in seconds
            data={
                'chat_id': chat_id,
                'message_id': original_message_id,
                'pair': pair,
                'status': result_status # Pass the "خسارة💔" status
            },
            name=delayed_job_name
        )
        logger.info(f"Scheduled delayed loss notification for {pair} in chat {chat_id} (msg: {original_message_id}). Job: {delayed_job_name}")

async def send_delayed_loss_result_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the delayed result of a trading signal that resulted in a loss."""
    job_data = context.job.data
    chat_id = job_data['chat_id']
    original_message_id = job_data['message_id']
    pair = job_data['pair']
    # status = job_data['status'] # This will be "خسارة💔"

    result_text = f"نتيجة الصفقة لـ {pair}: خسارة💔 (بعد انتظار المضاعفة)"

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=result_text,
            reply_to_message_id=original_message_id
        )
        logger.info(f"Successfully sent DELAYED LOSS signal result for {pair} to chat {chat_id}, replying to message {original_message_id}.")
    except Exception as e:
        logger.error(
            f"Failed to send DELAYED LOSS signal result for {pair} to chat {chat_id}, replying to message {original_message_id}. Error: {e}"
        )
        # Attempt to send as a new message if replying failed
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"(الرسالة الأصلية قد تكون حذفت) {result_text}")
            logger.info(f"Sent DELAYED LOSS signal result for {pair} to chat {chat_id} as new message (original likely deleted).")
        except Exception as e_alt:
            logger.error(f"Failed to send DELAYED LOSS signal result for {pair} to chat {chat_id} even as a new message. Error: {e_alt}")

def main() -> None:
    """Start the bot."""
    # Initialize database
    database.initialize_database()
    logger.info("Database initialized.")

    # Add owner if not exists (can also be part of start or a specific init command)
    if database.get_user_role(OWNER_ID) is None:
        database.add_user(OWNER_ID, "owner")
        logger.info(f"Bot owner {OWNER_ID} ensured in database with 'owner' role.")


    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # User management commands
    application.add_handler(CommandHandler("add_developer", add_developer))
    application.add_handler(CommandHandler("remove_developer", remove_developer))
    application.add_handler(CommandHandler("add_member", add_member))
    application.add_handler(CommandHandler("remove_member", remove_member))

    # Channel management commands
    application.add_handler(CommandHandler("add_channel", add_channel_command))
    application.add_handler(CommandHandler("remove_channel", remove_channel_command))
    application.add_handler(CommandHandler("list_channels", list_channels_command))

    # Control Panel
    # Control Panel (Commented out if not part of this subtask's file version)
    # application.add_handler(CommandHandler("control_panel", control_panel_command))
    # application.add_handler(CallbackQueryHandler(control_panel_callback_handler))

    # Test signal command
    application.add_handler(CommandHandler("test_signal", test_signal_command))
    application.add_handler(CommandHandler("send_signal", send_signal_command))

    # log all errors
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
