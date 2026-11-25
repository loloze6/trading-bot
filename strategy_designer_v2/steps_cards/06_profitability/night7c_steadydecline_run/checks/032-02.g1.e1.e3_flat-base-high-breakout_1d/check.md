---
backtest: 032-02.g1.e1.e3_flat-base-high-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8843 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3301 | above 0 | yes |
| Mean daily return, on days in a position | 0.001279 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5963 | above 0 | yes |
| Calmar | 0.7331 | above 0.75 | no |
| Trades per day | 0.04628 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.627 % |
| Yearly return | +10.4 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e3_flat-base-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
