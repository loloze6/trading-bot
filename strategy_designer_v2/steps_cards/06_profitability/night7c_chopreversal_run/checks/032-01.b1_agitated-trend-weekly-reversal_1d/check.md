---
backtest: 032-01.b1_agitated-trend-weekly-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7937 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.348 | above 0 | no |
| Mean daily return, on days in a position | -0.001504 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9288 | above 0 | no |
| Calmar | -0.1841 | above 0.75 | no |
| Trades per day | 0.03761 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.815 % |
| Yearly return | -12.7 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1_agitated-trend-weekly-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
