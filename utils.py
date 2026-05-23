    import math
import re
from typing import Dict, Any

def analyze_password(password: str) -> Dict[str, Any]:
    """
    Parolni tahlil qiladi va uni brute-force orqali buzish vaqtini hisoblaydi.
    Sekundiga 10 milliard kombinatsiya tekshira oladigan tizim asos qilingan.
    """
    length = len(password)
    if length == 0:
        return {"pool_size": 0, "entropy": 0, "seconds": 0, "time_formatted": "0 sekund", "rating": "Juda yomon"}

    # Belgilar jamlanmasini aniqlash
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digits = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digits: pool_size += 10
    if has_special: pool_size += 32

    if pool_size == 0:
        pool_size = 26 

    # Entropiya va kombinatsiyalar soni
    entropy = length * math.log2(pool_size)
    combinations = math.pow(pool_size, length)

    # Sekundiga 10,000,000,000 urinish tezligi
    guesses_per_second = 10_000_000_000
    seconds = (combinations / 2) / guesses_per_second

    # Vaqtni yil, oy, kunlarga formatlash
    time_formatted = format_time(seconds)

    if entropy < 28:
        rating = "🔴 Juda zaif (Lahzalarda buziladi)"
    elif entropy < 36:
        rating = "🟠 Zaif (Bir necha daqiqa yoki soat)"
    elif entropy < 60:
        rating = "🟡 O'rtacha (Yaxshi xavfsizlik)"
    elif entropy < 128:
        rating = "🟢 Kuchli (Xavfsiz va ishonchli)"
    else:
        rating = "⚡️ O'ta kuchli (Buzib bo'lmas darajada)"

    return {
        "length": length,
        "pool_size": pool_size,
        "entropy": round(entropy, 2),
        "combinations": combinations,
        "time_formatted": time_formatted,
        "rating": rating,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digits": has_digits,
        "has_special": has_special
    }

def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return "0.001 sekunddan kam"
    if seconds < 1:
        return f"{seconds:.3f} sekund"
    
    minute = 60
    hour = minute * 60
    day = hour * 24
    month = day * 30.44
    year = day * 365.25

    if seconds < minute:
        return f"{round(seconds, 2)} sekund"
    elif seconds < hour:
        return f"{round(seconds / minute, 1)} daqiqa"
    elif seconds < day:
        return f"{round(seconds / hour, 1)} soat"
    elif seconds < month:
        return f"{round(seconds / day, 1)} kun"
    elif seconds < year:
        return f"{round(seconds / month, 1)} oy"
    
    years = seconds / year
    if years > 1_000_000_000:
        return f"{round(years / 1_000_000_000, 2)} milliard yil"
    elif years > 1_000_000:
        return f"{round(years / 1_000_000, 2)} million yil"
    elif years > 1000:
        return f"{round(years / 1000, 2)} ming yil"
    else:
        return f"{round(years, 1)} yil"