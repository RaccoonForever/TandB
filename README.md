# Features implemented

## Connectors

Allow you to connect to the API programmatically

### XTB

- Basic connector (class xAPIConnector)

### Alpha Vantage (deprecated)

- Basic connector (class AlphaVantage)
- When not premium we can only make like 20 calls a day

### FMP (Financial Modeling Preparation)

- Basic connector (class FMPApi)
- When not premium only US and 250 calls a day to the API

Buy this one, seems fine.

## Data Loaders

### XTB

- Retrieve Data with a context manager
    - For the range allowed by the API
        - Need to do loop over it to have all the data
    - Daily, hourly (1h, 4h), 1min, 5min, 15min, 30min
        - Output Format: csv
        - Merge the results

## Indicators

### RSI

Based on TA lib.

## Strategies

### All strategies

- Evaluate with a grid search strategy

### RSI (class RSIStrategy)

- Backtest (class BacktestRSI)
    - Plot with signals and RSI plot under
        - Metrics:
            - Total Trades
            - Buy Signals
            - Sell Signals
            - Hold Signals
            - Final Value (of the capital)
            - Total Profit (without the last buy if no sell on this buy)

TODO:

- FVG: Don't allow a buy signal if we are during bearish FVGs
- Add new metrics like the number of good trades and the mean
  of result of good trades
- Disable debug for matplotlib and PIL logger in tests, set info instead