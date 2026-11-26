---
backtest: 047-02_falling-agitated-daily-rise-giveback_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3486 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.221 | above 0 | no |
| Mean daily return, on days in a position | 0.0004518 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1838 | above 0 | yes |
| Calmar | 0.1963 | above 0.75 | no |
| Trades per day | 0.06036 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.364 % |
| Yearly return | +2.2 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/047-02_falling-agitated-daily-rise-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
