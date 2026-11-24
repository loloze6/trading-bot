---
backtest: 031-03.b1_wide-day-extends-up-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.359 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.393 | above 0 | no |
| Mean daily return, on days in a position | 0.005419 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.927 | above 0 | yes |
| Calmar | 4.504 | above 0.75 | yes |
| Trades per day | 0.1173 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.588 % |
| Yearly return | +95.5 % (over 1.99 years) |
| Days in a position | 36 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-03.b1_wide-day-extends-up-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
