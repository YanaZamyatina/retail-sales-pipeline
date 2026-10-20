import configparser
from datetime import datetime, time, timedelta
import json
from pathlib import Path
from random import randint, choice, uniform, random

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

config = configparser.ConfigParser()
config.read(BASE_DIR / 'config.ini')

SALES_DIR = (BASE_DIR / config["Files"]["SALES_DIR"]).resolve()
SALES_DIR.mkdir(parents=True, exist_ok=True)

MIN_SHOPS = int(config["Shops"]["MIN_SHOPS"])
MAX_SHOPS = int(config["Shops"]["MAX_SHOPS"])
MIN_CASH_DESKS = int(config["Cash_desks"]["MIN_CASH_DESKS"])
MAX_CASH_DESKS = int(config["Cash_desks"]["MAX_CASH_DESKS"])

MIN_SALES_PER_CASH_DESK = int(config["Sales_per_cash_desk"]["MIN_SALES_PER_CASH_DESK"])
MAX_SALES_PER_CASH_DESK = int(config["Sales_per_cash_desk"]["MAX_SALES_PER_CASH_DESK"])
MIN_ITEM_PER_DOC = int(config["Item_per_doc"]["MIN_ITEM_PER_DOC"])
MAX_ITEM_PER_DOC = int(config["Item_per_doc"]["MAX_ITEM_PER_DOC"])

MIN_PRICE = float(config["Prices"]["MIN_PRICE"])
MAX_PRICE = float(config["Prices"]["MAX_PRICE"])
DISCOUNT_CHANCE = float(config["Discounts"]["DISCOUNT_CHANCE"])
DISCOUNT_VALUES = json.loads(config["Discounts"]["DISCOUNT_VALUES"])

START_HOUR = int(config["Opening_hours"]["START_HOUR"])
END_HOUR = int(config["Opening_hours"]["END_HOUR"])

CATEGORY = json.loads(config["Category"]["Category"])
ITEM = json.loads(config["Item"]["ITEM"])

for shop_id in list(range(1, randint(MIN_SHOPS, MAX_SHOPS) + 1)):
    for cash_desk_id in list(range(1, randint(MIN_CASH_DESKS, MAX_CASH_DESKS) + 1)):
        doc_id = 1
        sales_data = []

        doc_times = [
            (datetime.combine(datetime.now().date(), time(START_HOUR,0)) + timedelta(seconds=randint(0, (END_HOUR - START_HOUR ) * 60 * 60))).strftime("%Y-%m-%d %H:%M:%S")
            for _ in range(1, randint(MIN_SALES_PER_CASH_DESK, MAX_SALES_PER_CASH_DESK) + 1)
        ]
        doc_times.sort()

        for created_at in doc_times:
            for _ in range(1, randint(MIN_ITEM_PER_DOC, MAX_ITEM_PER_DOC) + 1):
                sales_data.append({
                    'created_at': created_at,
                    'doc_id': doc_id,
                    'category': (category := choice(CATEGORY)),
                    'item': choice(ITEM[category]),
                    'amount': randint(1, 5),
                    'price': (price := round(uniform(MIN_PRICE, MAX_PRICE), 2)),
                    'discount': round(price * choice(DISCOUNT_VALUES), 2) if random() < DISCOUNT_CHANCE else 0.00
                })
            doc_id += 1

        df = pd.DataFrame(sales_data)
        
        file_name = f"{shop_id}_{cash_desk_id}.csv"
        full_path = (BASE_DIR / SALES_DIR).resolve() / file_name
        df.to_csv(full_path, index=False)