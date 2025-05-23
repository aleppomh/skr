from telegram import InlineKeyboardButton # Only InlineKeyboardButton is needed from telegram for formatting

# TIMEZONE_STR is not needed here anymore as it's part of the signal_data
# CURRENCY_PAIRS list is removed
# generate_signal function is removed

def format_signal_message(signal_data: dict) -> tuple[str, dict]:
    """
    Formats the signal data (received from an external source like analyzer_service_mock.py)
    into a message string and creates an inline keyboard.
    """
    # Ensure all expected keys are present in signal_data, with defaults if necessary
    # This makes the function more robust if signal_data might be incomplete.
    pair = signal_data.get('pair', 'N/A')
    direction = signal_data.get('direction', 'N/A')
    entry_time = signal_data.get('entry_time', 'N/A')
    duration = signal_data.get('duration', 'N/A')
    timezone_str = signal_data.get('timezone', 'N/A') # Renamed from 'timezone' in dict to avoid conflict if we used datetime.timezone
    success_rate = signal_data.get('success_rate', 'N/A')
    rsi = signal_data.get('rsi', 'N/A')
    macd = signal_data.get('macd', 'N/A')
    bollinger_bands = signal_data.get('bollinger_bands', 'N/A')

    message_text = f"""🔔 إشارة جديدة 🔔
▪️ الزوج: {pair}
▪️ الاتجاه: {direction}
▪️ وقت الدخول: {entry_time}
▪️ المدة: {duration}
▪️ المنطقة الزمنية: {timezone_str}
▪️ النجاح: {success_rate}%

📊 تحليل فني سريع:
▪️ مؤشر RSI: {rsi}
▪️ مؤشر MACD: {macd}
▪️ البولنجر باند: {bollinger_bands}

⚠️تحذير؛ اتبع إدارة رأس مال صارمة"""

    keyboard = [
        [
            InlineKeyboardButton("تسجيل حساب", url="https://pocket.click/register?utm_source=affiliate&a=k1EstfG8TSRtg2&ac=mosto&code=50START"),
            InlineKeyboardButton("قناتنا", url="https://t.me/Trading3litepro")
        ]
    ]
    reply_markup = {"inline_keyboard": keyboard}

    return message_text, reply_markup

if __name__ == '__main__':
    # Example usage with mock data similar to what analyzer_service_mock.py would provide
    mock_signal_from_analyzer = {
        "pair": "EUR/USD OTC",
        "direction": "شراء 🟢⬆️",
        "entry_time": "10:45",
        "duration": "5Min",
        "timezone": "GMT+3",
        "success_rate": 88,
        "rsi": 65,
        "macd": "إيجابي ✅",
        "bollinger_bands": "ضمن النطاق ↔️",
    }
    
    message, keyboard_markup_dict = format_signal_message(mock_signal_from_analyzer)
    print("\nFormatted Message:")
    print(message)
    print("\nKeyboard Markup Dictionary:")
    print(keyboard_markup_dict)

    # To test how it would be used with InlineKeyboardMarkup directly (as in bot.py)
    # from telegram import InlineKeyboardMarkup
    # ikm_buttons = []
    # for row in keyboard_markup_dict["inline_keyboard"]:
    #     button_row = []
    #     for button_info in row:
    #         button_row.append(InlineKeyboardButton(text=button_info["text"], url=button_info["url"]))
    #     ikm_buttons.append(button_row)
    # ikm = InlineKeyboardMarkup(ikm_buttons)
    # print("\nActual InlineKeyboardMarkup object (example for bot.py):")
    # print(ikm)
