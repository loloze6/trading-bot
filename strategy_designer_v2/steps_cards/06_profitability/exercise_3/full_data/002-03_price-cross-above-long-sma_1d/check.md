---
backtest: 002-03_price-cross-above-long-sma_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5051 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06455 | above 0 | no |
| Mean daily return | 0.0009085 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1867 | above 0 | yes |
| Calmar | 0.1399 | above 0.75 | no |
| Trades per bar | 0.1105 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
- The book: BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, equal weight; 24 windows, 2898 days (7.94 years); 1897 trades on 17163 bars
- Holding's Sharpe: 0.5696; yearly return: 0.1163; deepest fall: 0.8312; window whose removal lowers the Sharpe most: w11
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
