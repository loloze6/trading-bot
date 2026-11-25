---
backtest: 035-02_swing-wide-low-close-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.771 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2169 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008434 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6209 | above 0 | yes |
| Calmar | 0.5799 | above 0.75 | no |
| Trades per day | 0.7435 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.081 % |
| Yearly return | +25.4 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/035-02_swing-wide-low-close-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
