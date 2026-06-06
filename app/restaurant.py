# app/restaurant.py

import re

def make_restaurant_id(
    name: str,
    location: str
) -> str:

    s = f"{name}_{location}".lower()

    s = re.sub(r"[^a-z0-9]+", "_", s)

    return s.strip("_")