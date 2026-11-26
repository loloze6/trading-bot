---
backtest: 064-01_rising-agitated-volume-shrink-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2915 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2781 | above 0 | no |
| Mean daily return, on days in a position | 0.000482 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.216 | above 0 | no |
| Calmar | 0.07305 | above 0.75 | no |
| Trades per day | 0.02144 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.253 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/064-01_rising-agitated-volume-shrink-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
