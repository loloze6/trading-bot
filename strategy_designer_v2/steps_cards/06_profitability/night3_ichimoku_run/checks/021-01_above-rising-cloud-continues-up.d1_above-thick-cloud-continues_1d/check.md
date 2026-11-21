---
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5081 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04603 | above 0 | no |
| Mean daily return | 0.0003325 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2902 | above 0 | yes |
| Calmar | 0.2038 | above 0.75 | no |
| Trades per day | 0.03464 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
