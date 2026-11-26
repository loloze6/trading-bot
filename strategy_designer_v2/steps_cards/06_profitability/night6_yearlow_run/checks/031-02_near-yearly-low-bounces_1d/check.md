---
backtest: 031-02_near-yearly-low-bounces_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2552 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3265 | above 0 | no |
| Mean daily return, on days in a position | 0.0003083 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1054 | above 0 | yes |
| Calmar | 0.03265 | above 0.75 | no |
| Trades per day | 0.04981 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.994 % |
| Yearly return | +2.4 % (over 7.94 years) |
| Days in a position | 86 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02_near-yearly-low-bounces_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
