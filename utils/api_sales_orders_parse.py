import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

def write_data_in_json(url, headers, params, keys, model):
    response = requests.get(url, headers=headers, params=params) # получаем данные sales или order в зависимости от переданных аргументов url, headers, params

    my_list = response.json() # функция json() преобразует ответ в список словарей. Далее работаем с my_list как со списком словарей
    for i in range(len(my_list)):
        my_list[i]["date"] = my_list[i]["date"].replace('T', ' ') # исправляем запись даты, чтобы она подходила под требования sqlite3

    database_list = []
    for item in response.json():
        temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in keys}}
        database_list.append(temp_dict)

    if model == "main.OrdersTable":
        with open("../main/fixtures/orders_file.json", 'w', encoding='utf-8') as file: # записываем в файл список словарей с необходимыми ключами, файл будем использовать в команде manage.py loaddata <файл>
            json.dump(database_list, file, ensure_ascii=False, indent=4)
    elif model == "main.SalesTable":
        with open("../main/fixtures/sales_file.json", 'w', encoding='utf-8') as file:
            json.dump(database_list, file, ensure_ascii=False, indent=4)

wb_api_token = os.getenv("wb_api_token_orders_sales")
orders_url = os.getenv("orders_url")
sales_url = os.getenv("sales_url")

headers = {
    'Authorization': wb_api_token
}

params_order = {
    'dateFrom': '2024-12-20',
    'flag': 1, # флаг 1 когда нужна инфа по одному дню
}

params_sales = {
    'dateFrom': '2024-12-25',
    'flag': 0, # флаг 0 когда нужна инфа по промедутку от указанного дня до сегодняшнего
}

needed_keys_orders = ["date", "warehouseName", "oblastOkrugName", "regionName", "supplierArticle", "nmId", "barcode", "incomeID", "finishedPrice", "priceWithDisc", "srid"]
needed_keys_sales = ["date", "supplierArticle", "nmId", "techSize", "priceWithDisc", "saleID"]
orders_model = "main.OrdersTable"
sales_model = "main.SalesTable"

write_data_in_json(orders_url, headers, params_order, needed_keys_orders, orders_model)
write_data_in_json(sales_url, headers, params_sales, needed_keys_sales, sales_model)