import pandas as pd
from bs4 import BeautifulSoup
from fund import get_html_content_from_url, get_investor_stocks
from util import save_to_file_curr_date, find_unique
from constants import HOME_URL, FUND_URL_PRE, STOCK_ID


def find_investor_extract_stocks_save(no_of_investors=5, historic_no_of_day=10):
    html_content = get_html_content_from_url(HOME_URL)
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'groupTable'})
    df = pd.read_html(str(table))[0]

    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    href_data = []
    for index, row in enumerate(rows):
        superstar_cell = row.find('td', class_='sup-name')
        if superstar_cell:
            href_data.append(superstar_cell.find('a')['href'])
        else:
            print(f"Row {index}: No superstar data found.")
    df['Href'] = pd.DataFrame(href_data)

    df[['Value', 'Change']] = df['Portfolio Value *(change)'].str.split('Cr', expand=True)
    df.drop(columns=['Portfolio Value *(change)'], inplace=True)
    df['Value'] = pd.to_numeric(df['Value'].str.strip().str.replace(',', ''))
    df['ID'] = df['Href'].apply(lambda x: x.split('/')[3])
    df['Name'] = df['Href'].apply(lambda x: x.split('/')[5])
    df['URL'] = df.apply(lambda row: f"{FUND_URL_PRE}/{row['ID']}/{row['Name']}/", axis=1)
    df.sort_values(by='Value', ascending=False, inplace=True)

    results = []
    for url in df[:no_of_investors]['URL']:
        html_content = get_html_content_from_url(url)
        result = get_investor_stocks(html_content, historic_no_of_day=historic_no_of_day)
        if result:
            results.extend(result)

    unique_results = find_unique(results, STOCK_ID)
    save_to_file_curr_date(unique_results)
    return unique_results


if __name__ == '__main__':
    find_investor_extract_stocks_save()