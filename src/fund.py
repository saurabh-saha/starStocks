import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
from constants import STOCK_ID

def get_html_content_from_file(file='sbi.html'):
    with open(file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content


def get_html_content_from_url(url='https://trendlyne.com/portfolio/bulk-block-deals/superstar-shareholders/sbi-group-portfolio/'):
    html_content = None
    headers = {
        'User-Agent': ''
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
    return html_content


def get_investor_stocks(html_content, historic_no_of_day):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'bbdealTable'})
    df = pd.read_html(str(table))[0]
    if df.empty:
        return []

    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    stock_ids = []
    for index, row in enumerate(rows):
        stock_cell = row.find('td', class_='stockrow')
        if stock_cell:
            stock_id = stock_cell.find('a')['href'].split('/')[3]
            stock_ids.append(stock_id)
        else:
            print(f"Row {index}: No superstar data found.")
    df[STOCK_ID] = pd.DataFrame(stock_ids)
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')
    current_date = pd.to_datetime(datetime.now().date())
    one_month_ago = current_date - pd.DateOffset(days=historic_no_of_day)
    df = df[df['Date'] > one_month_ago]
    if df.empty:
        return []

    data = df[['Client Name', 'Exchange', 'Action', 'Date', 'Avg. Price', 'stock_ids']].to_dict(orient='records')
    return data

if __name__ == '__main__':
    html_content = get_html_content_from_file()
    data = get_investor_stocks(html_content)
    print(json.dumps(json.loads(data), indent=2))