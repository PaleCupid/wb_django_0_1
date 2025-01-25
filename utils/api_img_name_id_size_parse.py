import requests
import os
import json
import copy
from dotenv import load_dotenv

load_dotenv()
wb_api_token_cards = os.getenv('wb_api_token_cards')
url_cards = os.getenv('url_cards')
needed_keys_first = [
    'nmID', 'vendorCode', 'photos',
]
needed_keys_second = [
    'nmID', 'sizes',
]

def img_name_id_parse(cards, database, keys, model):
    for item in cards:
        temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in keys}}
        temp_dict['fields']['photos'] = temp_dict['fields']['photos'][0]['big']
        database.append(temp_dict)

def size_id_parse(cards, database, keys, model):
    for item in cards:
        temp_dict = {'model': model, 'fields': {key: value for key, value in item.items() if key in keys}}
        for i in range(len(temp_dict['fields']['sizes'])):
            temp_dict['fields']['sizes'][i] = temp_dict['fields']['sizes'][i]['techSize']
        my_list = temp_dict['fields']['sizes']
        for item in my_list:
            temp_dict_one_size = copy.deepcopy(temp_dict)
            temp_dict_one_size['fields']['sizes'] = item
            database.append(temp_dict_one_size)


model_name_img_id = 'main.NameImgIdModel'
model_id_size = 'main.IdSizeModel'

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

res = requests.post(url_cards, headers=headers, data=json.dumps(data))

last_card_num = res.json()['cursor']['total'] # присваиваем число загруженных карточек
    
with open('../main/fixtures/img_name_id.json', 'w', encoding='utf-8') as file:
    with open('../main/fixtures/id_size.json', 'w', encoding='utf-8') as file_sizes:
        database_list = []
        database_list_sizes = []
        img_name_id_parse(res.json()["cards"], database_list, needed_keys_first, model_name_img_id)
        size_id_parse(res.json()["cards"], database_list_sizes, needed_keys_second, model_id_size)
        while last_card_num == 100: # если карточек больше 100, то заходим в цикл
            data = {
                "settings": {
                    "cursor": {
                        "limit": 100,
                        "updatedAt": res.json()['cursor']['updatedAt'], # передаем последнюю дату как просит wb для загрузки остальных карточек
                        "nmID": res.json()['cursor']["nmID"] # делаем то же, но с номером карточки
                    },
                    "filter": {
                        "withphoto": -1
                    }
                }
            }
            res = requests.post(url_cards, headers=headers, data=json.dumps(data))
            img_name_id_parse(res.json()["cards"], database_list, needed_keys_first, model_name_img_id)
            size_id_parse(res.json()["cards"], database_list_sizes, needed_keys_second, model_id_size)
            last_card_num = res.json()['cursor']['total']
        json.dump(database_list, file, ensure_ascii=False, indent=4)
        json.dump(database_list_sizes, file_sizes, ensure_ascii=False, indent=4)
        





