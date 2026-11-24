---
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08741 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.1854 | above 0 | no |
| Mean daily return, on days in a position | -0.000155 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6193 | above 0 | no |
| Calmar | -0.09721 | above 0.75 | no |
| Trades per day | 0.04621 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.394 % |
| Yearly return | -0.9 % (over 0.87 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_2026/backtests/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
