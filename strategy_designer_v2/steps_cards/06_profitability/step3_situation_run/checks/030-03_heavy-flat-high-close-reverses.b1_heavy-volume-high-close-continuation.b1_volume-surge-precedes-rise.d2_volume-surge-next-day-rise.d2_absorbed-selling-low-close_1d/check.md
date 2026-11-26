---
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8922 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.338 | above 0 | yes |
| Mean daily return, on days in a position | 0.001956 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7545 | above 0 | yes |
| Calmar | 0.5808 | above 0.75 | no |
| Trades per day | 0.1477 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.180 % |
| Yearly return | +19.2 % (over 7.94 years) |
| Days in a position | 28 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/steps/bt/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
