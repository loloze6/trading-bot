---
backtest: 060-02.d2.d2_volume-growth-capitulation-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5684 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01419 | above 0 | yes |
| Mean daily return, on days in a position | 0.001329 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4557 | above 0 | yes |
| Calmar | 0.33 | above 0.75 | no |
| Trades per day | 0.05358 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.658 % |
| Yearly return | +6.6 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d2.d2_volume-growth-capitulation-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
