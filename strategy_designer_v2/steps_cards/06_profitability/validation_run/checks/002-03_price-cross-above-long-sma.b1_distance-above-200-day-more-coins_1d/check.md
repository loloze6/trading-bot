---
backtest: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8416 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2838 | above 0 | yes |
| Mean daily return | 0.0006197 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6038 | above 0 | yes |
| Calmar | 0.5007 | above 0.75 | no |
| Trades per bar | 0.1005 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
