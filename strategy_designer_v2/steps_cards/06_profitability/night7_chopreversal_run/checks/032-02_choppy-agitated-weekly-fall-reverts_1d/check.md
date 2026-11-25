---
backtest: 032-02_choppy-agitated-weekly-fall-reverts_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3599 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2097 | above 0 | no |
| Mean daily return, on days in a position | 0.0005909 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2882 | above 0 | yes |
| Calmar | 0.1494 | above 0.75 | no |
| Trades per day | 0.02441 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.577 % |
| Yearly return | +3.4 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/032-02_choppy-agitated-weekly-fall-reverts_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
