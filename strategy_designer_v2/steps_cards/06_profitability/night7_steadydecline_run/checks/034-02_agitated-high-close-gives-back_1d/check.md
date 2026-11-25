---
backtest: 034-02_agitated-high-close-gives-back_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.241 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8106 | above 0 | no |
| Mean daily return, on days in a position | -0.000297 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4015 | above 0 | no |
| Calmar | -0.1245 | above 0.75 | no |
| Trades per day | 0.3471 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.129 % |
| Yearly return | -7.2 % (over 7.94 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/034-02_agitated-high-close-gives-back_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
