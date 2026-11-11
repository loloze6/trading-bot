---
backtest: 002-04_price-cross-below-long-sma_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5224 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.092 | above 0 | no |
| Mean daily return | -0.0007663 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7523 | above 0 | no |
| Calmar | -0.3547 | above 0.75 | no |
| Trades per bar | 0.1226 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
- The book: BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, equal weight; 24 windows, 2898 days (7.94 years); 2105 trades on 17163 bars
- Holding's Sharpe: 0.5696; yearly return: -0.3473; deepest fall: 0.9792; window whose removal lowers the Sharpe most: w2
Record: `steps_cards/04_backtest/full_data_run/backtests/002-04_price-cross-below-long-sma_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
