import peewee as pw

# служебная база данных с информацией для обработчиков
help_db = pw.SqliteDatabase("databases/help_db.sqlite3")
# главная база данных, заполняемая из поступающих документов
main_db = pw.SqliteDatabase("databases/main_db.sqlite3")


class BrandInfo(pw.Model):
    id = pw.PrimaryKeyField(unique=True)
    brand = pw.CharField(default="car")  # Бренд
    templates_filled = pw.BooleanField(default=False)  # флаг - заполнены ли шаблоны данного бренда,
    # если нет при первом получении файла от этого бренда необходимо это исправить и make флаг=True

    # названия столбцов - названия необходимых столбцов в главной бд
    # значения - номер столбца в excel необходимый для конкретного параметра (считать от одного)
    article = pw.IntegerField()  # Артикул
    part_name = pw.IntegerField()  # Наименование
    purchase_price = pw.IntegerField()  # Цена закупа
    retail_price = pw.IntegerField()  # Цена розничная
    recommended_retail_price = pw.IntegerField()  # РРЦ

    class Meta:
        database = help_db
        order_by = "id"
        db_table = "Info about every car brand"


class BrandTemplates(pw.Model):
    id = pw.PrimaryKeyField(unique=True)
    brand = pw.CharField(default="car")  # Бренд
    # значение в клетке - строковое представление значение в шапке у конкретного бренда
    article = pw.TextField(default="null")  # Артикул
    part_name = pw.TextField(default="null")  # Наименование
    purchase_price = pw.TextField(default="null")  # Цена закупа
    retail_price = pw.TextField(default="null")  # Цена розничная
    recommended_retail_price = pw.TextField(default="null")  # РРЦ

    class Meta:
        database = help_db
        order_by = "id"
        db_table = "Every car brands template"


class MainTable(pw.Model):
    id = pw.PrimaryKeyField(unique=True)
    brand = pw.CharField(default="car")  # Бренд
    article = pw.TextField(default="null")  # Артикул
    part_name = pw.TextField(default="null")  # Наименование
    purchase_price = pw.TextField(default="null")  # Цена закупа
    retail_price = pw.TextField(default="null")  # Цена розничная
    recommended_retail_price = pw.TextField(default="null")  # РРЦ
    upload_date = pw.TextField()  # Дата загрузки цен

    class Meta:
        database = main_db
        order_by = "id"
        db_table = "Main info"
