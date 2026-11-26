---
backtest: 033-01_rising-market-sharp-drop-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8402 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.286 | above 0 | yes |
| Mean daily return, on days in a position | 0.001205 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6217 | above 0 | yes |
| Calmar | 0.5572 | above 0.75 | no |
| Trades per day | 0.1819 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.110 % |
| Yearly return | +16.8 % (over 7.94 years) |
| Days in a position | 40 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/033-01_rising-market-sharp-drop-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
