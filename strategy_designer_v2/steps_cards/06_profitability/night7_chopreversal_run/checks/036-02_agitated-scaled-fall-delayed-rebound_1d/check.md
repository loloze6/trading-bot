---
backtest: 036-02_agitated-scaled-fall-delayed-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3407 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2289 | above 0 | no |
| Mean daily return, on days in a position | 0.0004161 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1241 | above 0 | yes |
| Calmar | 0.1247 | above 0.75 | no |
| Trades per day | 0.2052 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.002 % |
| Yearly return | +4.8 % (over 7.94 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/036-02_agitated-scaled-fall-delayed-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
