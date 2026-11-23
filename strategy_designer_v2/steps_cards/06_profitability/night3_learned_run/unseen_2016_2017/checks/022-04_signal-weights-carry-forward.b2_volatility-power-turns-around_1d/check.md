---
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8578 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.64 | above 0 | no |
| Mean daily return, on days in a position | -0.0008881 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.583 | above 0 | no |
| Calmar | -0.4425 | above 0.75 | no |
| Trades per day | 0.109 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.277 % |
| Yearly return | -21.3 % (over 1.99 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
