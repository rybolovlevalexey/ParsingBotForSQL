import peewee as pw

db = pw.SqliteDatabase("db.sqlite3")  # служебная база данных с информацией для обработчиков
# main_db = pw.PostgresqlDatabase


class BrandInfo(pw.Model):
    id = pw.PrimaryKeyField(unique=True)
    brand = pw.CharField(default="car")  # Бренд
    # названия столбцов - названия необходимых столбцов в главной бд
    # значения - номер столбца в excel необходимый для конкретного параметра (считать от нуля)
    article = pw.IntegerField()  # Артикул
    part_name = pw.IntegerField()  # Наименование
    purchase_price = pw.IntegerField()  # Цена закупа
    retail_price = pw.IntegerField()  # Цена розничная
    recommended_retail_price = pw.IntegerField()  # РРЦ
    upload_date = pw.TextField()  # Дата загрузки цен

    class Meta:
        database = db
        order_by = "id"
        db_table = "Info about every car brand"
