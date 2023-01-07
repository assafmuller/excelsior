import argparse
import json

import pandas as pd
from yahoo_fin import stock_info as si


parser = argparse.ArgumentParser(prog = 'Excelsior')
parser.add_argument('--tickers', choices=['sp500', 'nasdaq', 'dow', 'other', 'all'], default='all', nargs='+')


def download_tickers(tickers):
    print("Getting tickers %s" % tickers)

    tickers_to_symbols = {
        'sp500': si.tickers_sp500(),
        'nasdaq': si.tickers_nasdaq(),
        'dow': si.tickers_dow(),
        'other': si.tickers_other()
    }

    if 'all' in tickers:
        tickers = tickers_to_symbols.keys()

    symbols = set()
    for group in tickers:
        df = pd.DataFrame(tickers_to_symbols[group])
        l = df[0].values.tolist()
        symbols = symbols.union(symbols, set(l))

    # Some stocks are 5 characters. Those stocks with the suffixes listed below are not of interest.
    exclude_list = ['W', 'R', 'P', 'Q']
    result = set()

    for symbol in symbols:
        if not (len(symbol) > 4 and symbol[-1] in exclude_list):
            result.add(symbol)

    return result


def download_stocks(tickers):
    print('Downloading data for %s tickers' % len(tickers))
    stocks = {}

    i = 0
    for ticker in tickers:
        i = i + 1
        if not ticker:
            continue
        print("Getting data for (%s/%s): %s" % (i, len(tickers), ticker))
        try:
            stock = si.get_data(ticker)['close']
            stock_output = []
            for k, v in stock.items():
                stock_output.append((str(k).split()[0], v))
            
            stocks[ticker] = stock_output
        except Exception as e:
            print('Error getting data for %s' % ticker)

    return stocks


def cache_stocks(stocks):
    with open('stocks.json', 'w') as fp:
        json.dump(stocks, fp)


def main():
    args = parser.parse_args()
    tickers = download_tickers(args.tickers)
    stocks = download_stocks(tickers)
    cache_stocks(stocks)


if __name__ == "__main__":
    main()
