---
backtest: 072-02_choppy-deep-up-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02118 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.533 | above 0 | no |
| Mean daily return, on days in a position | 3.132e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1518 | above 0 | no |
| Calmar | -0.007249 | above 0.75 | no |
| Trades per day | 0.07253 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.418 % |
| Yearly return | -0.1 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-02_choppy-deep-up-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
