---
backtest: 059-02.b1_falling-calm-declines-extend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2817 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2879 | above 0 | no |
| Mean daily return, on days in a position | 0.0006136 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1103 | above 0 | yes |
| Calmar | 0.1093 | above 0.75 | no |
| Trades per day | 0.09701 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.985 % |
| Yearly return | +3.6 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-02.b1_falling-calm-declines-extend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
