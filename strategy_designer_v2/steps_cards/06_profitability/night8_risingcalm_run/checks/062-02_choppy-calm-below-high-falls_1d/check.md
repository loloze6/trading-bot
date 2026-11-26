---
backtest: 062-02_choppy-calm-below-high-falls_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.01013 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5797 | above 0 | no |
| Mean daily return, on days in a position | -1.989e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1592 | above 0 | no |
| Calmar | -0.03561 | above 0.75 | no |
| Trades per day | 0.0952 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.822 % |
| Yearly return | -1.4 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/062-02_choppy-calm-below-high-falls_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
