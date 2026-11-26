---
backtest: 058-01_calm-downtrend-depth-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2006 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.369 | above 0 | no |
| Mean daily return, on days in a position | 0.0004573 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.04207 | above 0 | yes |
| Calmar | 0.09899 | above 0.75 | no |
| Trades per day | 0.0624 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.786 % |
| Yearly return | +1.9 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01_calm-downtrend-depth-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
