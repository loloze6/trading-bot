---
backtest: 060-02.d1.d3_shrinkage-short-in-moderate-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3651 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.189 | above 0 | no |
| Mean daily return, on days in a position | 0.0006054 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1541 | above 0 | yes |
| Calmar | 0.1325 | above 0.75 | no |
| Trades per day | 0.04902 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.536 % |
| Yearly return | +3.3 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d3_shrinkage-short-in-moderate-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
