---
backtest: 032-02.b1_choppy-weekly-falls-keep-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4497 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.004 | above 0 | no |
| Mean daily return, on days in a position | -0.0001517 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6006 | above 0 | no |
| Calmar | -0.102 | above 0.75 | no |
| Trades per day | 0.03521 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.245 % |
| Yearly return | -2.2 % (over 7.94 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-02.b1_choppy-weekly-falls-keep-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
