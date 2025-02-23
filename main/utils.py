import requests
import os
import json
import copy
from dotenv import load_dotenv

load_dotenv()

def orders_parse_in_file():
    wb_api_token_orders_sales = os.getenv("wb_api_token_orders_sales")
    orders_url = os.getenv("orders_url")

    headers = {
        'Authorization': wb_api_token_orders_sales
    }
    params = {
        'dateFrom': '2024-12-20',
        'flag': 1,
    }
    needed_keys = ["date", "warehouseName", "oblastOkrugName", "regionName", "supplierArticle", 
        "nmId", "barcode", "incomeID", "finishedPrice", "priceWithDisc", "srid", "isCancel"]
    model = "main.OrdersTable"
    
    dump_list = []
    response = requests.get(orders_url, headers=headers, params=params)
    
    for item in response.json():
        temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in needed_keys}}
        dump_list.append(temp_dict)

    with open("main/fixtures/orders_file.json", 'w', encoding='utf-8') as file:
        json.dump(dump_list, file, ensure_ascii=False, indent=4)

#############################################################################################################################

def sales_parse_in_file():
    wb_api_token_orders_sales = os.getenv("wb_api_token_orders_sales")
    sales_url = os.getenv("sales_url")

    headers = {
        'Authorization': wb_api_token_orders_sales
    }
    params = {
        'dateFrom': '2024-12-25',
        'flag': 0,
    }
    needed_keys = ["date", "supplierArticle", "nmId", "techSize", "priceWithDisc", "saleID"]
    model = "main.SalesTable"

    dump_list = []
    response = requests.get(sales_url, headers=headers, params=params)

    for item in response.json():
        temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in needed_keys}}
        dump_list.append(temp_dict)

    with open("main/fixtures/sales_file.json", 'w', encoding='utf-8') as file:
        json.dump(dump_list, file, ensure_ascii=False, indent=4)

#############################################################################################################################

def name_img_id_parse_in_file():

    def dump_list_fill(cards, database, keys, model):
        for item in cards:
            temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in keys}}
            temp_dict['fields']['photos'] = temp_dict['fields']['photos'][0]['big']
            database.append(temp_dict)

    wb_api_token_cards = os.getenv('wb_api_token_cards')
    cards_url = os.getenv('cards_url')

    headers = {
        'Authorization': wb_api_token_cards
    }
    data = {
        "settings": {
            "cursor": {
                "limit": 100,
            },
            "filter": {
                "withphoto": -1
            }
        }
    }
    needed_keys = ['nmID', 'vendorCode', 'photos',]
    model = 'main.NameImgIdModel'

    response = requests.post(cards_url, headers=headers, data=json.dumps(data))
    last_card_num = response.json()['cursor']['total']

    with open('main/fixtures/name_img_id_file.json', 'w', encoding='utf-8') as file:
        dump_list = []
        dump_list_fill(response.json()['cards'], dump_list, needed_keys, model)
        while last_card_num == 100:
            data = {
                "settings": {
                    "cursor": {
                        "limit": 100,
                        "updatedAt": response.json()['cursor']['updatedAt'], # передаем последнюю дату как просит wb для загрузки остальных карточек
                        "nmID": response.json()['cursor']["nmID"] # делаем то же, но с номером карточки
                    },
                    "filter": {
                        "withphoto": -1
                    }
                }
            }
            response = requests.post(cards_url, headers=headers, data=json.dumps(data))
            dump_list_fill(response.json()['cards'], dump_list, needed_keys, model)
            last_card_num = response.json()['cursor']['total']
        json.dump(dump_list, file, ensure_ascii=False, indent=4)

#############################################################################################################################

def size_id_parse_in_file():

    def dump_list_fill(cards, database, keys, model):
        for item in cards:
            temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in keys}}
            print(temp_dict)
            for i in range(len(temp_dict['fields']['sizes'])):
                temp_dict['fields']['sizes'][i] = temp_dict['fields']['sizes'][i]['techSize']
            print(temp_dict)
            for item in temp_dict['fields']['sizes']:
                temp_dict_one_size = copy.deepcopy(temp_dict)
                temp_dict_one_size['fields']['sizes'] = item
                database.append(temp_dict_one_size)


    wb_api_token_cards = os.getenv('wb_api_token_cards')
    cards_url = os.getenv('cards_url')

    headers = {
        'Authorization': wb_api_token_cards
    }
    data = {
        "settings": {
            "cursor": {
                "limit": 100,
            },
            "filter": {
                "withphoto": -1
            }
        }
    }
    needed_keys = ['nmID', 'sizes',]
    model = 'main.IdSizeModel'

    response = requests.post(cards_url, headers=headers, data=json.dumps(data))
    last_card_num = response.json()['cursor']['total']

    with open('main/fixtures/id_size.json', 'w', encoding='utf-8') as file:
        dump_list = []
        dump_list_fill(response.json()['cards'], dump_list, needed_keys, model)
        while last_card_num == 100:
            data = {
                "settings": {
                    "cursor": {
                        "limit": 100,
                        "updatedAt": response.json()['cursor']['updatedAt'], # передаем последнюю дату как просит wb для загрузки остальных карточек
                        "nmID": response.json()['cursor']["nmID"] # делаем то же, но с номером карточки
                    },
                    "filter": {
                        "withphoto": -1
                    }
                }
            }
            response = requests.post(cards_url, headers=headers, data=json.dumps(data))
            dump_list_fill(response.json()['cards'], dump_list, needed_keys, model)
            last_card_num = response.json()['cursor']['total']
        json.dump(dump_list, file, ensure_ascii=False, indent=4)