---
backtest: 041-02_agitated-fall-rise-vs-range-giveback_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2951 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2745 | above 0 | no |
| Mean daily return, on days in a position | 0.0005592 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1139 | above 0 | yes |
| Calmar | 0.1233 | above 0.75 | no |
| Trades per day | 0.06409 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.463 % |
| Yearly return | +2.2 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/041-02_agitated-fall-rise-vs-range-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
