import json
import os
import datetime
from allinstitute import find_investor_extract_stocks_save

LIMIT = 2500
DAYS = 10
NO_OF_INVESTORS=5

if __name__ == '__main__':
    find_investor_extract_stocks_save(NO_OF_INVESTORS)

    directory = os.getcwd()
    current_date = datetime.datetime.now()
    ten_days_ago = current_date - datetime.timedelta(days=DAYS)
    files_in_directory = os.listdir(directory)
    recent_files = []
    for file_name in files_in_directory:
        file_path = os.path.join(directory, file_name)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        if creation_time >= ten_days_ago and creation_time <= current_date and file_name.endswith('.json'):
            recent_files.append(file_path)

    results = []
    for file_path in recent_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        data = json.loads((data))
        for i in data:
            if i['Action'] == 'Purchase':
                q = divmod(LIMIT, i['Avg. Price'])
                if q[0] > 0:
                    j = {}
                    j['Avg. Price'] = i['Avg. Price']
                    j['stock_ids'] = i['stock_ids']
                    j['quantity'] = q[0]
                    j['Exchange'] = i['Exchange']
                    results.append(j)
    print(json.dumps(results, indent=2))


