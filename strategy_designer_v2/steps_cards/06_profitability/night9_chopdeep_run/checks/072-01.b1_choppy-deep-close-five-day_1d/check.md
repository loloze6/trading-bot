---
backtest: 072-01.b1_choppy-deep-close-five-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1898 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.744 | above 0 | no |
| Mean daily return, on days in a position | -0.0002706 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4111 | above 0 | no |
| Calmar | -0.09816 | above 0.75 | no |
| Trades per day | 0.1309 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.963 % |
| Yearly return | -5.0 % (over 7.94 years) |
| Days in a position | 35 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-01.b1_choppy-deep-close-five-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
