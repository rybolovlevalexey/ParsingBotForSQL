from models import BrandInfo, BrandTemplates, MainTable
import datetime
import typing
import pandas as pd
import json

date_now = str(datetime.datetime.now().strftime("%d.%m.%Y"))


# добавление нового обработчика по номерам необходимых столбцов
def loading_new_handler_numbers(brand_info: dict[str, typing.Union[str, int]]):
    for key, value in brand_info.items():
        if value.startswith("-"):
            brand_info[key] = -1
        else:
            brand_info[key] = int(value)
    br_info = BrandInfo(brand=brand_info["brand_name"], article=(brand_info["article_number"]),
                        part_name=(brand_info["part_name_number"]),
                        purchase_price=(brand_info["purchase_price_number"]),
                        retail_price=(brand_info["retail_price_number"]),
                        recommended_retail_price=(brand_info["recommended_retail_price_number"]))
    br_info.save()


# добавление нового обработчика по шаблонам столбцов, после этого можно ещё и наполнить
# таблицу с номерами столбцов, т.к. есть вся необходимая информация
def loading_new_handler_templates(brand_info: dict[str, str], df: pd.DataFrame) -> bool:
    for key, value in brand_info.items():
        if value == "Отсутствует":
            brand_info[key] = "null"
    br_temps = BrandTemplates(brand=brand_info["brand_name"], article=brand_info["article"],
                              part_name=brand_info["part_name"],
                              purchase_price=brand_info["purchase_price"],
                              retail_price=brand_info["retail_price"],
                              recommended_retail_price=brand_info["recommended_retail_price"])
    br_temps.save()
    table_header = list(list(df.iterrows())[0][1].keys())
    br_info = BrandInfo(brand=brand_info["brand_name"], templates_filled=True,
                        article=table_header.index(brand_info["article"]) + 1 if brand_info[
                                "article"] != "null" else -1,
                        part_name=table_header.index(brand_info["part_name"]) + 1 if brand_info[
                                  "part_name"] != "null" else -1,
                        purchase_price=table_header.index(brand_info["purchase_price"]) + 1 if
                        brand_info["purchase_price"] != "null" else -1,
                        retail_price=table_header.index(brand_info["retail_price"]) + 1 if
                        brand_info["retail_price"] != "null" else -1,
                        recommended_retail_price=table_header.index(
                            brand_info["recommended_retail_price"]) + 1 if brand_info[
                            "recommended_retail_price"] != "null" else -1)

    if BrandInfo.select().where(BrandInfo.brand == brand_info["brand_name"]).count == 0 or \
            len(list(elem.templates_filled for elem in BrandInfo.select().where(
                BrandInfo.brand == brand_info["brand_name"]))) == 0 or \
            not list(elem.templates_filled for elem in BrandInfo.select().where(
                BrandInfo.brand == brand_info["brand_name"]))[0]:
        br_info.save()
    return True


# проверка текущего документа на наличие в нём уже сохранённого ранее шаблона
def check_current_document(df: pd.DataFrame) -> typing.Union[bool, str]:
    sp_cols = df.columns.values.tolist()
    brand_name = None
    for elem in BrandTemplates.select():
        flag = True
        for temp in filter(lambda x: x != "null",
                           [elem.article, elem.part_name, elem.purchase_price, elem.retail_price,
                            elem.recommended_retail_price]):
            if temp not in sp_cols:
                flag = False
                break
        if flag:
            brand_name = elem.brand
            break
    if brand_name is not None:
        return brand_name  # f"Данный файл подходит под шаблон компании {brand_name}"
    return False  # "Не найдено шаблонов, под которые мог бы подойти данный файл"


# получение списка всевозможных созданных брендов из двух таблиц
def get_all_handlers_names() -> list[str]:
    result1 = set(elem.brand for elem in BrandInfo.select())
    result2 = set(elem.brand for elem in BrandTemplates.select())
    result = list(result1.union(result2))
    return result


# проверка переданного имени во всех таблицах с информацией для обработчиков
def check_new_brand_name(brand_name: str) -> bool:  # True - такого имени ещё нет в базе данных
    res1 = BrandInfo.select().where(brand_name == BrandInfo.brand)
    res2 = BrandTemplates.select().where(brand_name == BrandTemplates.brand)
    if res1.count() == res2.count() == 0:
        return True
    return False


# получение необходимой информации по названию детали
def get_info_by_part_name(part_name: str) -> dict[str, str]:
    result = MainTable.get(part_name=part_name)
    return result.receive_json()


def get_info_by_by_article_and_brand(article: str, brand: str) -> dict[str, str]:
    result = list(MainTable.select().where((MainTable.article == article) &
                                           (MainTable.brand == brand)))
    last_one = max(result, key=lambda x: x.upload_date)
    res_dict = {'brand': last_one.brand, 'article': last_one.article,
                'part_name': last_one.part_name, 'purchase_price': last_one.purchase_price,
                'retail_price': last_one.article, 'recommended_retail_price': last_one.article}
    return res_dict


# БОЛТ
print(get_info_by_part_name("БОЛТ"))
print(get_info_by_by_article_and_brand("1311338", "jlr"))