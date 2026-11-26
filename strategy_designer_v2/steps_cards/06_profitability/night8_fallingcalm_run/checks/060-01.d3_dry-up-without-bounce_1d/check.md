---
backtest: 060-01.d3_dry-up-without-bounce_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4286 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1256 | above 0 | no |
| Mean daily return, on days in a position | 0.0006793 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.277 | above 0 | yes |
| Calmar | 0.1886 | above 0.75 | no |
| Trades per day | 0.08508 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.641 % |
| Yearly return | +4.6 % (over 7.94 years) |
| Days in a position | 21 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-01.d3_dry-up-without-bounce_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
