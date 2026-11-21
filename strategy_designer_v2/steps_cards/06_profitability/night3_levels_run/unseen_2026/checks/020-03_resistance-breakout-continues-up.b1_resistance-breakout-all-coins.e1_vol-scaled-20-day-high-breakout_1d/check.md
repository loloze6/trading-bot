---
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3756 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3092 | above 0 | yes |
| Mean daily return | 0.0001166 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7731 | above 0 | no |
| Calmar | 0.6977 | above 0.75 | no |
| Trades per day | 0.04607 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/unseen_2026/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
