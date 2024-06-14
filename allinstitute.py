import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from fund import get_html_content_from_url, get_investor_stocks


def find_investor_extract_stocks_save(no_of_investors=5):
    html_content = get_html_content_from_url('https://trendlyne.com/portfolio/superstar-shareholders/index/institutional/')
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'groupTable'})
    df = pd.read_html(str(table))[0]

    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    href_data = []
    for index, row in enumerate(rows):
        superstar_cell = row.find('td', class_='sup-name')
        if superstar_cell:
            # Extract the text content and href attribute from the <a> tag
            superstar_name = superstar_cell.get_text(strip=True)
            superstar_href = superstar_cell.find('a')['href']
            href_data.append(superstar_href)
        else:
            print(f"Row {index}: No superstar data found.")
    df['Href'] = pd.DataFrame(href_data)

    df[['Value', 'Change']] = df['Portfolio Value *(change)'].str.split('Cr', expand=True)
    df.drop(columns=['Portfolio Value *(change)'], inplace=True)
    df['Value'] = pd.to_numeric(df['Value'].str.strip().str.replace(',', ''))
    df['ID'] = df['Href'].apply(lambda x: x.split('/')[3])
    df['Name'] = df['Href'].apply(lambda x: x.split('/')[5])
    df['URL'] = df.apply(lambda row: f"https://trendlyne.com/portfolio/bulk-block-deals/{row['ID']}/{row['Name']}/", axis=1)
    df.sort_values(by='Value', ascending=False, inplace=True)

    first_5_urls = df[:no_of_investors]['URL']
    results = []
    for url in first_5_urls:
        html_content = get_html_content_from_url(url)
        result = get_investor_stocks(html_content, day=10)
        if result:
            results.extend(result)

    seen_stock_ids = set()
    unique_results = []
    for result in results:
        stock_ids = result["stock_ids"]
        if stock_ids not in seen_stock_ids:
            seen_stock_ids.add(stock_ids)
            unique_results.append(result)

    current_date = datetime.now().strftime('%d%b%Y').capitalize()
    file_name = f"{current_date}.json"
    json_data = json.dumps(unique_results, indent=2, default=str)
    with open(file_name, 'w') as f:
        f.write(json_data)
    print(f"JSON data saved to {file_name}")


if __name__ == '__main__':
    find_investor_extract_stocks_save()