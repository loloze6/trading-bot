---
backtest: 069-02.d1.d2_swing-graded-low-range-up-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2426 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3147 | above 0 | no |
| Mean daily return, on days in a position | 0.0009775 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.08648 | above 0 | yes |
| Calmar | 0.08966 | above 0.75 | no |
| Trades per day | 0.01768 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.301 % |
| Yearly return | +1.2 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d1.d2_swing-graded-low-range-up-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
