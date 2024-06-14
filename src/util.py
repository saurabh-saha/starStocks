import json
from datetime import datetime
from constants import FILE_CACHE_DIR
import os


def save_to_file_curr_date(unique_results):
    current_date = datetime.now().strftime('%d%b%Y').capitalize()
    file_name = f"{current_date}.json"
    file_path = os.path.join(FILE_CACHE_DIR, file_name)
    json_data = json.dumps(unique_results, indent=2, default=str)
    with open(file_path, 'w') as f:
        f.write(json_data)
    print(f"JSON data saved to {file_name}")


def find_unique(list_of_dict, key):
    seen_stock_ids = set()
    unique_results = []
    for result in list_of_dict:
        stock_ids = result[key]
        if stock_ids not in seen_stock_ids:
            seen_stock_ids.add(stock_ids)
            unique_results.append(result)
    return unique_results
