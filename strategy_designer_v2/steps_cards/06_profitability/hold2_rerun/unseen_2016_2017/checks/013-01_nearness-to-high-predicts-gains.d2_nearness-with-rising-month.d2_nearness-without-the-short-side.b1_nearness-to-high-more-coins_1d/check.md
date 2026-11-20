---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.22 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03022 | above 0 | yes |
| Mean daily return | 0.003545 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.793 | above 0 | yes |
| Calmar | 12.74 | above 0.75 | yes |
| Trades per day | 0.1533 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold2_rerun/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
