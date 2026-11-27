---
backtest: 074-01.g1_falling-agitated-wide-up-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7553 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1857 | above 0 | yes |
| Mean daily return, on days in a position | 0.002823 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5246 | above 0 | yes |
| Calmar | 0.5458 | above 0.75 | no |
| Trades per day | 0.01975 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.280 % |
| Yearly return | +4.0 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.g1_falling-agitated-wide-up-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
