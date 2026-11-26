---
backtest: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2863 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3561 | above 0 | yes |
| Mean daily return, on days in a position | 0.0003123 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1811 | above 0 | no |
| Calmar | 0.2152 | above 0.75 | no |
| Trades per day | 0.06231 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.733 % |
| Yearly return | +3.1 % (over 0.87 years) |
| Days in a position | 35 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/validation_run/unseen_2026/backtests/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
