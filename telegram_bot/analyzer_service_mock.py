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

TIMEZONE_STR = "GMT+3" # Consistent with signals.py

def generate_mock_signal() -> dict:
    """
    Generates a simulated trading signal with parameters matching signals.py.
    """
    pair = random.choice(CURRENCY_PAIRS)
    direction = random.choice(["بيع 🔴⬇️", "شراء 🟢⬆️"])
    
    # GMT+3 timezone object
    gmt3_tz = timezone(timedelta(hours=3))
    entry_time = datetime.now(gmt3_tz).strftime("%H:%M")
    
    duration = random.choice(["1Min", "2Min", "3Min", "5Min"])
    success_rate = random.randint(70, 95)
    rsi = random.randint(10, 90)
    macd_status = random.choice(["سلبي ❌", "إيجابي ✅"])
    bollinger_bands_status = random.choice(["فوق النطاق العلوي 📈", "ضمن النطاق ↔️", "تحت النطاق السفلي 📉"])

    return {
        "pair": pair,
        "direction": direction,
        "entry_time": entry_time,
        "duration": duration,
        "timezone": TIMEZONE_STR,  # Using the string "GMT+3"
        "success_rate": success_rate,
        "rsi": rsi,
        "macd": macd_status,
        "bollinger_bands": bollinger_bands_status,
    }

if __name__ == "__main__":
    mock_signal = generate_mock_signal()
    print("Generated Mock Signal:")
    print(mock_signal)
    # Example of accessing a specific field
    # print(f"\nMock Signal Pair: {mock_signal['pair']}")
    # print(f"Mock Signal Entry Time (GMT+3): {mock_signal['entry_time']}")
