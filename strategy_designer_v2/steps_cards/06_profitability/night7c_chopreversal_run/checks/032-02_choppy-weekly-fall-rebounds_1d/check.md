---
backtest: 032-02_choppy-weekly-fall-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4073 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1623 | above 0 | no |
| Mean daily return, on days in a position | 0.0004567 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2717 | above 0 | yes |
| Calmar | 0.2271 | above 0.75 | no |
| Trades per day | 0.1006 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.964 % |
| Yearly return | +5.9 % (over 7.94 years) |
| Days in a position | 45 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-02_choppy-weekly-fall-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
