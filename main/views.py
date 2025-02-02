from django.shortcuts import render
from .models import NameImgIdModel, IdSizeModel, SalesTable, OrdersTable
from datetime import date, timedelta

def items_sales(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    first_date = date(2024, 12, 30)
    today_date = date.today()

    if start_date:
        start_date = date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[-2:]))
        if start_date >= first_date:
            first_date = start_date
    if end_date:
        end_date = date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[-2:]))
        if end_date <= today_date:
            today_date = end_date

    days_between_dates = today_date - first_date

    sales_dict = {} # словарь который будет отправляться в шаблон, цикл ниже наполняет словарь ключами в виде дат
    dates_list=[] # список будет содержать в себе даты и отправится в шаблон для создания дат в шапке таблицы
    for i in range(days_between_dates.days + 1):
        current_day = str(first_date + timedelta(1) * i)
        dates_list.append(current_day)
        sales_dict[current_day] = sales_dict.get(current_day, {})
        if ((first_date + timedelta(1) * i).isocalendar().weekday) == 7:
            dates_list.append('Неделя ' + str((first_date + timedelta(1) * i).isocalendar().week)) # добавляем номер недели в таблицу чтобы суммировать в столбце недели количество продаж за неделю

    sales_data_list = list(SalesTable.objects.values()) # забираем данные из таблицы SalesTable

    for item in sales_data_list:
        operation = 0 # если произошла продажа (S) то присваиваем переменной +1, если возврат то -1
        string_date = str(item['date'].date())
        if item['saleID'][0] == 'S':
            operation = 1
        elif item['saleID'][0] == 'R':
            operation = -1
        if string_date in dates_list:
            sales_dict[string_date][item['nmId']] = sales_dict[string_date].get(item['nmId'], 0) + operation # считаем для каждого nmID кол-во продаж/возвратов за каждую дату

    data_cards = list(NameImgIdModel.objects.values()) # получаем данные карточек
    data_sizes = list(IdSizeModel.objects.values()) # получаем размеры каждого предмета
    for item_cards in data_cards:
        for item_sizes in data_sizes:
            if (item_cards['nmID'] == item_sizes['nmID_id']) and (item_sizes['sizes'] != 'ONE SIZE') and ('sizes' in item_sizes.keys()):
                item_cards['sizes'] = item_cards.get('sizes', []) # добавляем для каждого предмета и размеров пару предмет - размеры
                item_cards['sizes'].append(item_sizes['sizes'])

    menus_n_refs = {'Продажи': '/items_sales', 'Список заказов': '/orders_table'}

    return render(request, 'items_sales.html', {'data': data_cards, 'dates': dates_list, 'sales': sales_dict, 
                                                "menu_items": menus_n_refs, 'start_date': first_date, 'end_date': today_date})

def orders_table(request):
    data = OrdersTable.objects.all()
    menus_n_refs = {'Продажи': '/items_sales', 'Список заказов': '/orders_table'}
    return render(request, 'orders_table.html', {"data": data, "menu_items": menus_n_refs})