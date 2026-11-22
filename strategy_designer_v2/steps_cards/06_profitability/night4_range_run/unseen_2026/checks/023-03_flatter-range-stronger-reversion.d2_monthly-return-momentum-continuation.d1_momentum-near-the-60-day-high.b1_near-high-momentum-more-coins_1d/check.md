---
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2349 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1685 | above 0 | yes |
| Mean daily return | 0.0001494 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4207 | above 0 | no |
| Calmar | 0.2195 | above 0.75 | no |
| Trades per day | 0.2532 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
