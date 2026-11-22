---
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.047 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.7347 | above 0 | no |
| Mean daily return | 0.003892 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.639 | above 0 | yes |
| Calmar | 11.11 | above 0.75 | yes |
| Trades per day | 0.2108 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_range_run/unseen_2016_2017/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
