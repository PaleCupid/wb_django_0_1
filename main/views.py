from django.shortcuts import render
from .models import NameImgIdModel, IdSizeModel

def items_sales(request):
    data_1 = list(NameImgIdModel.objects.values())
    data_2 = list(IdSizeModel.objects.values())
    for item_1 in data_1:
        for item_2 in data_2:
            if (item_1['nmID'] == item_2['nmID_id']) and (item_2['sizes'] != 'ONE SIZE') and ('sizes' in item_2.keys()):
                item_1['sizes'] = item_1.get('sizes', [])
                item_1['sizes'].append(item_2['sizes'])
    # print(data_1)
    return render(request, 'items_sales.html', {'data': data_1})
