---
backtest: 058-01.g2.d1_volume-dry-up-at-the-lows_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1312 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4384 | above 0 | no |
| Mean daily return, on days in a position | 0.0002624 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.03461 | above 0 | no |
| Calmar | 0.02054 | above 0.75 | no |
| Trades per day | 0.07807 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.886 % |
| Yearly return | +0.8 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.g2.d1_volume-dry-up-at-the-lows_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
