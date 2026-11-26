---
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.121 | above 0 | no |
| Sharpe minus holding's Sharpe | -5.356 | above 0 | no |
| Mean daily return, on days in a position | -0.00191 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.689 | above 0 | no |
| Calmar | -0.5387 | above 0.75 | no |
| Trades per day | 0.05649 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.492 % |
| Yearly return | -18.4 % (over 1.99 years) |
| Days in a position | 29 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2016_2017/backtests/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
