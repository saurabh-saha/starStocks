import json
import os
import datetime
from constants import STOCK_ID
from util import find_unique


def format_data(data, cost_limit):
    results = []
    for i in data:
        if i['Action'] == 'Purchase':
            q = divmod(cost_limit, i['Avg. Price'])
            if q[0] > 0:
                j = {}
                j['Avg. Price'] = i['Avg. Price']
                j[STOCK_ID] = i[STOCK_ID]
                j['quantity'] = q[0]
                j['Exchange'] = i['Exchange']
                results.append(j)
    return results


def find_latest_data_from_file(historic_days):
    datas = []
    directory = os.path.join(os.getcwd(), 'file_cache')
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print('Cache folder not found')
        return datas

    current_date = datetime.datetime.now()
    ten_days_ago = current_date - datetime.timedelta(days=historic_days)
    files_in_directory = os.listdir(directory)
    recent_files = []
    for file_name in files_in_directory:
        file_path = os.path.join(directory, file_name)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        if creation_time >= ten_days_ago and creation_time <= current_date and file_name.endswith('.json'):
            recent_files.append(file_path)


    for file_path in recent_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        datas += json.loads((data))
    return datas


def show(datas, price_limit):
    datas = find_unique(datas, STOCK_ID)
    results = format_data(datas, price_limit)
    print(json.dumps(results, indent=2))


