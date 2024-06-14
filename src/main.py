import argparse
from reco import find_latest_data_from_file, show
from allinstitute import find_investor_extract_stocks_save


def run(num_investors, price_limit, no_of_historic_days, env):
    print(f"Number of investors: {num_investors}")
    print(f"Price limit: {price_limit}")
    print(f"Number of historic days: {no_of_historic_days}")
    print(f"Environment: {env}")
    if env == 'prod':
        datas = find_investor_extract_stocks_save(num_investors, no_of_historic_days)
    else:
        datas = find_latest_data_from_file(no_of_historic_days)
    show(datas, price_limit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process number of investors.')
    parser.add_argument('--i', dest='num_investors', type=int, default=5, help='Number of investors (default: 10)')
    parser.add_argument('--p', dest='price_limit', type=float, default=1000.0, help='Price limit (default: 2500.0)')
    parser.add_argument('--d', dest='no_of_historic_days', type=int, default=10, help='Number of historic days (default: 30)')
    parser.add_argument('--env', dest='env', type=str, default='dev', choices=['prod', 'dev'], help='Environment (prod/dev) (default: prod)')
    args = parser.parse_args()
    run(args.num_investors, args.price_limit, args.no_of_historic_days, args.env)