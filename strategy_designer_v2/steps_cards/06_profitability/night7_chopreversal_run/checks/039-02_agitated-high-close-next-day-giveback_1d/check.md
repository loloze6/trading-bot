---
backtest: 039-02_agitated-high-close-next-day-giveback_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5853 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01574 | above 0 | yes |
| Mean daily return, on days in a position | 0.0001429 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4708 | above 0 | yes |
| Calmar | 0.3003 | above 0.75 | no |
| Trades per day | 0.2946 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.276 % |
| Yearly return | +3.0 % (over 7.94 years) |
| Days in a position | 59 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-02_agitated-high-close-next-day-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
