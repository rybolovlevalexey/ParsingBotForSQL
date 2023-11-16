from models import BrandInfo
import datetime
import typing

date_now = str(datetime.datetime.now().strftime("%d.%m.%Y"))


def loading_new_handler(brand_info: dict[str, typing.Union[str, int]]):
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
