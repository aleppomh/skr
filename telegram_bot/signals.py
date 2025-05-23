import random
from datetime import datetime, timezone, timedelta

# Full list of currency pairs, duplicates removed and sorted.
CURRENCY_PAIRS = sorted(list(set([
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/USD OTC", "EUR/CHF OTC", "EUR/GBP OTC", 
    "GBP/USD OTC", "NZD/JPY OTC", "USD/CAD OTC", "USD/RUB OTC", "USD/THB OTC", 
    "USD/VND OTC", "USD/PHP OTC", "USD/MXN OTC", "USD/IDR OTC", "LBP/USD OTC", 
    "TND/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "NGN/USD OTC", 
    "UAH/USD OTC", "GBP/JPY OTC", "USD/INR OTC", "AUD/CHF OTC", "NZD/USD OTC", 
    "USD/PKR OTC", "AUD/CHF", "CHF/JPY", "EUR/CHF", "EUR/GBP", "GBP/CAD", 
    "EUR/USD", "GBP/AUD", "EUR/RUB OTC", "AUD/JPY OTC", "GBP/AUD OTC", 
    "JOD/CNY OTC", "AUD/NZD OTC", "EUR/NZD OTC", "CAD/JPY", "AUD/JPY", 
    "CAD/CHF OTC", "USD/CNH OTC", "EUR/AUD", "CHF/JPY OTC", "AUD/CAD", 
    "USD/CAD", "USD/JPY OTC", "USD/MYR OTC", "EUR/CAD", "CAD/JPY OTC", 
    "USD/BDT OTC", "YER/USD OTC", "EUR/JPY", "USD/JPY", "ZAR/USD OTC", 
    "USD/EGP OTC", "EUR/TRY OTC", "GBP/JPY", "OMR/CNY OTC", "USD/BRL OTC", 
    "CHF/NOK OTC", "USD/COP OTC", "USD/SGD OTC", "USD/DZD OTC", "QAR/CNY OTC", 
    "AUD/USD", "KES/USD OTC", "GBP/USD", "USD/CHF", "EUR/HUF OTC", 
    "USD/ARS OTC", "CAD/CHF", "MAD/USD OTC", "EUR/JPY OTC", "USD/CLP OTC", 
    "GBP/CHF", "GOLD-OTC", "GOLD"
])))

TIMEZONE_STR = "GMT+3"

def generate_signal(pair: str = None) -> dict:
    """
    Generates a simulated trading signal.
    If 'pair' is not provided, a random one is chosen from CURRENCY_PAIRS.
    """
    if pair is None:
        pair = random.choice(CURRENCY_PAIRS)

    # Adjust current time to GMT+3
    gmt3_offset = timedelta(hours=3)
    now_gmt3 = datetime.now(timezone.utc) + gmt3_offset

    signal_data = {
        "pair": pair,
        "direction": random.choice(["بيع 🔴⬇️", "شراء 🟢⬆️"]),
        "entry_time": now_gmt3.strftime("%H:%M"),
        "duration": random.choice(["1Min", "2Min", "3Min", "5Min"]),
        "timezone": TIMEZONE_STR,
        "success_rate": random.randint(70, 95),
        "rsi": random.randint(10, 90),
        "macd": random.choice(["سلبي ❌", "إيجابي ✅"]),
        "bollinger_bands": random.choice(["فوق النطاق العلوي 📈", "ضمن النطاق ↔️", "تحت النطاق السفلي 📉"]),
    }
    return signal_data

def format_signal_message(signal_data: dict) -> tuple[str, dict]:
    """
    Formats the signal data into a message string and creates an inline keyboard.
    """
    message_text = f"""🔔 إشارة جديدة 🔔
▪️ الزوج: {signal_data['pair']}
▪️ الاتجاه: {signal_data['direction']}
▪️ وقت الدخول: {signal_data['entry_time']}
▪️ المدة: {signal_data['duration']}
▪️ المنطقة الزمنية: {signal_data['timezone']}
▪️ النجاح: {signal_data['success_rate']}%

📊 تحليل فني سريع:
▪️ مؤشر RSI: {signal_data['rsi']}
▪️ مؤشر MACD: {signal_data['macd']}
▪️ البولنجر باند: {signal_data['bollinger_bands']}

⚠️تحذير؛ اتبع إدارة رأس مال صارمة"""

    # Inline Keyboard
    # Note: InlineKeyboardButton uses 'url' parameter for links
    keyboard = [
        [
            InlineKeyboardButton("تسجيل حساب", url="https://pocket.click/register?utm_source=affiliate&a=k1EstfG8TSRtg2&ac=mosto&code=50START"),
            InlineKeyboardButton("قناتنا", url="https://t.me/Trading3litepro")
        ]
    ]
    reply_markup = {"inline_keyboard": keyboard} # Changed to pass as a dict

    return message_text, reply_markup

if __name__ == '__main__':
    # Test the functions
    test_signal_data = generate_signal()
    print("Generated Signal Data:")
    print(test_signal_data)
    
    message, keyboard_markup = format_signal_message(test_signal_data)
    print("\nFormatted Message:")
    print(message)
    print("\nKeyboard Markup:")
    print(keyboard_markup)

    # Example of how InlineKeyboardMarkup is typically created in python-telegram-bot
    # from telegram import InlineKeyboardMarkup
    # ikm = InlineKeyboardMarkup.from_row(
    #     [
    #         InlineKeyboardButton("تسجيل حساب", url="https://pocket.click/register?utm_source=affiliate&a=k1EstfG8TSRtg2&ac=mosto&code=50START"),
    #         InlineKeyboardButton("قناتنا", url="https://t.me/Trading3litepro")
    #     ]
    # )
    # print("\nActual InlineKeyboardMarkup object (example):")
    # print(ikm)
