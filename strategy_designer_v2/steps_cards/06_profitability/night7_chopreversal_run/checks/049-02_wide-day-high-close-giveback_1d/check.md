---
backtest: 049-02_wide-day-high-close-giveback_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2881 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8422 | above 0 | no |
| Mean daily return, on days in a position | -6.666e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3856 | above 0 | no |
| Calmar | -0.106 | above 0.75 | no |
| Trades per day | 0.5568 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.424 % |
| Yearly return | -2.6 % (over 7.94 years) |
| Days in a position | 96 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/049-02_wide-day-high-close-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
