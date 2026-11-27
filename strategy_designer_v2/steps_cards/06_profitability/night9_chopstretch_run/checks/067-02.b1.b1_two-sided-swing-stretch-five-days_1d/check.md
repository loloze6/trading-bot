---
backtest: 067-02.b1.b1_two-sided-swing-stretch-five-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2332 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.321 | above 0 | no |
| Mean daily return, on days in a position | 0.0003064 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.06006 | above 0 | yes |
| Calmar | 0.0748 | above 0.75 | no |
| Trades per day | 0.1468 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.899 % |
| Yearly return | +2.6 % (over 7.94 years) |
| Days in a position | 36 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1_two-sided-swing-stretch-five-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
