from models import BrandInfo, BrandTemplates
import datetime
import typing
import pandas as pd

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
def loading_new_handler_templates():
    pass


# проверка текущего документа на наличие в нём уже сохранённого ранее шаблона
def check_current_document(df: pd.DataFrame) -> typing.Union[bool, str]:
    sp_cols = df.columns.values.tolist()
    brand_name = None
    for elem in BrandTemplates.select():
        flag = True
        for temp in filter(lambda x: x != "null", [elem.article, elem.part_name,
                                                   elem.purchase_price, elem.retail_price,
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


def get_all_handlers_names() -> list[str]:
    result = list(elem.brand for elem in BrandInfo.select())
    return result
