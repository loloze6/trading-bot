---
backtest: 060-02_volume-growth-fall-stalls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4668 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.08733 | above 0 | no |
| Mean daily return, on days in a position | 0.000524 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3063 | above 0 | yes |
| Calmar | 0.2348 | above 0.75 | no |
| Trades per day | 0.1166 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.895 % |
| Yearly return | +6.7 % (over 7.94 years) |
| Days in a position | 42 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02_volume-growth-fall-stalls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
