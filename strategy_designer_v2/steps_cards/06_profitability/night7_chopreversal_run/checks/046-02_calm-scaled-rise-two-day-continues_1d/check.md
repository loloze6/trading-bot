---
backtest: 046-02_calm-scaled-rise-two-day-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3667 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2029 | above 0 | no |
| Mean daily return, on days in a position | 0.0004996 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2383 | above 0 | yes |
| Calmar | 0.153 | above 0.75 | no |
| Trades per day | 0.2567 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.213 % |
| Yearly return | +6.0 % (over 7.94 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/046-02_calm-scaled-rise-two-day-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
