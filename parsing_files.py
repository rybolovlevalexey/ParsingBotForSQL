import pandas as pd
from sqlalchemy import create_engine
# Артикул, Брэнд, Наименование, Цена закупа, Цена розничная, РРЦ, Дата (загрузки цен)
df = pd.read_excel("files with costs/DEALER_PRICE_LIST.xlsb")
for index, row in df.iterrows():
    article = row["PART_NO"]
    name = row["PART_NAME_RUS"]
    purchase_price = row["D_ORDER_DNP"]
    retail_price = row["LIST_PRICE"]
    print(article, name, purchase_price, retail_price, sep="; ")
    break


def parsing(data_frame: pd.DataFrame, handler_id: str):
    # data_frame - получаемые на обработку данные
    # handler_id - id-шник во вспомогательной базе данных, какой обработчик нужно выбирать
    pass