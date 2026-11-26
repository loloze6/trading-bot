---
backtest: 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3586 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1955 | above 0 | no |
| Mean daily return, on days in a position | 0.0002344 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.04027 | above 0 | yes |
| Calmar | 0.2158 | above 0.75 | no |
| Trades per day | 0.007076 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.230 % |
| Yearly return | +1.5 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
