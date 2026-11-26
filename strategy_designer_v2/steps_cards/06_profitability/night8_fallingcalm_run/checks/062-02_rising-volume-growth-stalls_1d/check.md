---
backtest: 062-02_rising-volume-growth-stalls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.49 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.044 | above 0 | no |
| Mean daily return, on days in a position | -0.0006719 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6284 | above 0 | no |
| Calmar | -0.1869 | above 0.75 | no |
| Trades per day | 0.124 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.139 % |
| Yearly return | -12.2 % (over 7.94 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/062-02_rising-volume-growth-stalls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
