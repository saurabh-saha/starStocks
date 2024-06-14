# starStocks

Read stocks from Big Portfoliois of India.

run src/main.py

use the -- options parser.add_argument('--i', dest='num_investors', type=int, default=5, help='Number of investors (default: 10)')

    '--p', type=float, default=1000.0, help='Price limit (default: 2500.0)'
    '--d', type=int, default=10, help='Number of historic days (default: 30)'
    '--env', type=str, default='dev', choices=['prod', 'dev'], help='Environment (prod/dev) (default: prod)'


Sample Buy Response:

[
  {
    "Avg. Price": 280.0,
    "stock_ids": "ZAGGLE",
    "quantity": 3.0,
    "Exchange": "BSE"
  },
]
