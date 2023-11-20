import datetime
import pandas as pd
from models import BrandInfo, BrandTemplates, MainTable


# получен dataFrame скачанного файла и название бренда
# необходимо определить названия столбцов с нужной информацией загрузить её в основную базу данных
def parsing(data_frame: pd.DataFrame, brand_name: str):
    date_now = str(datetime.datetime.now().strftime("%d.%m.%Y"))
    table_header = data_frame.keys().tolist()

    # data_frame - получаемые на обработку данные
    # brand_name - название бренда
    print("Начата загрузка информации в главную базу данных")
    # название поля в main_db: название столбца в файле
    column_names = {"article": None, "part_name": None, "purchase_price": None,
                    "retail_price": None, "recommended_retail_price": None}

    # заполнение какой-то из таблиц, в случае если в ней не хватает информации
    if len(list(BrandInfo.select().where(BrandInfo.brand == brand_name))) == 0:
        print("here1")
        # в таблице BrandInfo нет информации об указанном бренде
        handler_templates = BrandTemplates.get(BrandTemplates.brand == brand_name)
        # наполнение BrandInfo
        new_br_info = BrandInfo(brand=brand_name, templates_filled=True,
                                article=table_header.index(
                                    handler_templates.article) + 1 if
                                handler_templates.article != "null" else -1,
                                part_name=table_header.index(
                                    handler_templates.part_name) + 1 if
                                handler_templates.part_name != "null" else -1,
                                purchase_price=table_header.index(
                                    handler_templates.purchase_price) + 1 if
                                handler_templates.purchase_price != "null" else -1,
                                retail_price=table_header.index(
                                    handler_templates.retail_price) + 1 if
                                handler_templates.retail_price != "null" else -1,
                                recommended_retail_price=table_header.index(
                                    handler_templates.recommended_retail_price) + 1 if
                                handler_templates.recommended_retail_price != "null" else -1)
        new_br_info.save()
    elif len(list(BrandTemplates.select().where(BrandTemplates.brand == brand_name))) == 0:
        print("here2")
        # в таблице BrandTemplates нет информации об указанном бренде
        handler_numbers = BrandInfo.get(BrandInfo.brand == brand_name)
        new_br_temp = BrandTemplates(brand=brand_name,
                                     article=table_header[
                                         handler_numbers.article - 1] if
                                     handler_numbers.article != -1 else "null",
                                     part_name=table_header[
                                         handler_numbers.part_name - 1] if
                                     handler_numbers.part_name != -1 else "null",
                                     purchase_price=table_header[
                                         handler_numbers.purchase_price - 1] if
                                     handler_numbers.purchase_price != -1 else "null",
                                     retail_price=table_header[
                                         handler_numbers.retail_price - 1] if
                                     handler_numbers.retail_price != -1 else "null",
                                     recommended_retail_price=table_header[
                                         handler_numbers.recommended_retail_price - 1] if
                                     handler_numbers.recommended_retail_price != -1 else "null")
        new_br_temp.save()

    # наполнение словаря column_names названиями столбцов в файле
    data_for_dict = BrandTemplates.get(BrandTemplates.brand == brand_name)
    column_names["article"] = data_for_dict.article
    column_names["part_name"] = data_for_dict.part_name
    column_names["purchase_price"] = data_for_dict.purchase_price
    column_names["retail_price"] = data_for_dict.retail_price
    column_names["recommended_retail_price"] = data_for_dict.recommended_retail_price

    for data_line in data_frame.iterrows():
        data_series = data_line[1]
        data = MainTable(brand=brand_name, upload_date=date_now)
        if column_names["article"] != "null":
            data.article = data_series.loc[column_names["article"]]
        if column_names["part_name"] != "null":
            data.part_name = data_series.loc[column_names["part_name"]]
        if column_names["purchase_price"] != "null":
            data.purchase_price = data_series.loc[column_names["purchase_price"]]
        if column_names["retail_price"] != "null":
            data.retail_price = data_series.loc[column_names["retail_price"]]
        if column_names["recommended_retail_price"] != "null":
            data.recommended_retail_price = data_series.loc[column_names[
            "recommended_retail_price"]]

        data.save()

    print("Загрузка информации в главную базу данных окончена")
