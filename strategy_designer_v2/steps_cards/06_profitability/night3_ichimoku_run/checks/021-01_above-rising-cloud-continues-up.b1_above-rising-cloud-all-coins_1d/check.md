---
backtest: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5578 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02815 | above 0 | no |
| Mean daily return | 0.0003861 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.211 | above 0 | yes |
| Calmar | 0.2085 | above 0.75 | no |
| Trades per day | 0.03178 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
