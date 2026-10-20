import configparser
from pathlib import Path

import pandas as pd

from pgdb import PGDatabase

BASE_DIR = Path(__file__).resolve().parent

config = configparser.ConfigParser()
config.read(BASE_DIR / 'config.ini')

DATABASE_CREDS = config["Database"]

SALES_DIR = (BASE_DIR / config["Files"]["SALES_DIR"]).resolve()
FILE_MASK = config["Files"]["FILE_MASK"]

database = PGDatabase(
    host = DATABASE_CREDS["HOST"],
    database = DATABASE_CREDS["DATABASE"],
    user = DATABASE_CREDS["USER"],
    password = DATABASE_CREDS["PASSWORD"]
)

file_list = SALES_DIR.glob(FILE_MASK)

for file in file_list:
    file_name = file.stem
    shop_id, cash_desk_id = map(int, file_name.split('_'))

    sales_df = pd.read_csv(file)

    for i, row in sales_df.iterrows():
        row_dict = row.to_dict()
        row_dict['shop_id'] = shop_id
        row_dict['cash_desk_id'] = cash_desk_id
        
        query="""insert into sales (
            created_at, doc_id, shop_id, cash_desk_id, category, item, amount, price, discount)
            values (%(created_at)s, %(doc_id)s, %(shop_id)s, %(cash_desk_id)s, %(category)s, %(item)s, %(amount)s, %(price)s, %(discount)s)
        """
        database.post(query, row_dict)
    
    file.unlink(missing_ok=True)