---
backtest: 074-01_falling-wide-up-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0506 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5036 | above 0 | no |
| Mean daily return, on days in a position | 4.318e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1588 | above 0 | no |
| Calmar | 0.01417 | above 0.75 | no |
| Trades per day | 0.02368 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.078 % |
| Yearly return | +0.1 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01_falling-wide-up-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
