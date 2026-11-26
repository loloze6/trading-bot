---
backtest: 031-02.b1.b1_strong-failed-rally-near-low_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3485 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9464 | above 0 | no |
| Mean daily return, on days in a position | -0.0005719 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5186 | above 0 | no |
| Calmar | -0.125 | above 0.75 | no |
| Trades per day | 0.03121 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.984 % |
| Yearly return | -8.0 % (over 7.94 years) |
| Days in a position | 31 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b1_strong-failed-rally-near-low_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
