---
backtest: 031-02.b1.b2_flat-day-after-strong-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.044 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4895 | above 0 | yes |
| Mean daily return, on days in a position | 0.002361 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9301 | above 0 | yes |
| Calmar | 0.9058 | above 0.75 | yes |
| Trades per day | 0.02106 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.675 % |
| Yearly return | +13.5 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b2_flat-day-after-strong-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
