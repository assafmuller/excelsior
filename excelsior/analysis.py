import argparse
import json

import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(prog = 'Excelsior')
parser.add_argument('--start_date', default='2000-01-01')
parser.add_argument('--end_date', default='2023-01-04')
parser.add_argument('--benchmark', default='SPY')
parser.add_argument('--results', type=int, default=30)


def get_stocks():
    with open('stocks.json', 'r') as fp:
        return json.load(fp)


def get_stock_ranges(stocks, start, end):
    result = {}
    for ticker in stocks.keys():
        if not stocks[ticker]:
            continue

        if stocks[ticker][0][0] > start or stocks[ticker][-1][0] < end:
            continue

        result[ticker] = []
        for date, value in stocks[ticker]:
            if start <= date and date <= end:
                result[ticker].append((date, value))
    return result


def transform_data(stocks):
    result = {}
    for ticker in stocks.keys():
        result[ticker] = []

        i = 0
        if not stocks[ticker]:
            continue

        for _, value in stocks[ticker]:
            result[ticker].append((i, value))
            i = i + 1
    return result


def filter_below_benchmark(stocks, benchmark):
    benchmark_performance = 0
    for stock, values in stocks.items():
        if stock == benchmark:
            benchmark_performance = (values[-1][1] / values[0][1])
            print('Determined benchmark %s performance at %s' % (benchmark, benchmark_performance))
    
    result = {}
    for stock, values in stocks.items():
        if (values[-1][1] / values[0][1]) >= benchmark_performance:
            result[stock] = values
    
    return result


def get_polyfit(stock, degree):
    x = [v[0] for v in stock]
    y = [v[1] for v in stock]
    if not x or not y:
        return

    try:
        p = np.polyfit(x, y, degree)
    except Exception as e:
        return

    # Skip companies with negative growth
    if (p[0] < 0):
        return

    # Create the linear (1 degree polynomial) model
    model = np.poly1d(p)
    # Fit the model
    y_model = model(x)

    # Mean
    y_bar = np.mean(y)
    # Coefficient of determination, R²
    R2 = np.sum((y_model - y_bar)**2) / np.sum((y - y_bar)**2)

    if np.isnan(R2) or np.isnan(p[0]):
        return

    return (R2, p[0], y[-1] / y[0])


def get_polyfits(stocks, degree):
    result = {}
    for ticker in stocks.keys():
        fit = get_polyfit(stocks[ticker], degree)
        if not fit:
            continue
        result[ticker] = fit

    return sorted(result.items(), key=lambda v: v[1][0], reverse=True)


def main():
    args = parser.parse_args()
    stocks = get_stocks()
    stocks = get_stock_ranges(stocks, args.start_date, args.end_date)
    stocks = transform_data(stocks)
    stocks = filter_below_benchmark(stocks, args.benchmark)

    linear_fits = get_polyfits(stocks, 1)
    poly_fits = get_polyfits(stocks, 2)

    print('LINEAR FITS...')
    for v in linear_fits[0:args.results]:
        print(v)

    print()
    print('POLY FITS...')
    for v in poly_fits[0:args.results]:
        print(v)


"""
TODO

* Download data for earnings / free cash flow and filter stocks that don't trend upwards
"""


if __name__ == "__main__":
    main()
