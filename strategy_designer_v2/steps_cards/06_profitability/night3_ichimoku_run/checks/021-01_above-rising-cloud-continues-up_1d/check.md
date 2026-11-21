---
backtest: 021-01_above-rising-cloud-continues-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4543 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.09989 | above 0 | no |
| Mean daily return | 0.0003633 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2268 | above 0 | yes |
| Calmar | 0.1551 | above 0.75 | no |
| Trades per day | 0.03892 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
