---
backtest: 002-06_down-cross-to-reverse-cross-loss_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.407 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9766 | above 0 | no |
| Mean daily return | -0.000513 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5856 | above 0 | no |
| Calmar | -0.2719 | above 0.75 | no |
| Trades per bar | 0.05564 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
- The book: BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, equal weight; 24 windows, 2898 days (7.94 years); 955 trades on 17163 bars
- Holding's Sharpe: 0.5696; yearly return: -0.2551; deepest fall: 0.9383; window whose removal lowers the Sharpe most: w14
Record: `steps_cards/04_backtest/full_data_run/backtests/002-06_down-cross-to-reverse-cross-loss_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
