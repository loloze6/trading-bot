---
backtest: 032-02.b2.g3_stretched-breakout-next-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2796 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8338 | above 0 | no |
| Mean daily return, on days in a position | -0.0002953 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4181 | above 0 | no |
| Calmar | -0.09126 | above 0.75 | no |
| Trades per day | 0.02203 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.180 % |
| Yearly return | -1.0 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g3_stretched-breakout-next-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
