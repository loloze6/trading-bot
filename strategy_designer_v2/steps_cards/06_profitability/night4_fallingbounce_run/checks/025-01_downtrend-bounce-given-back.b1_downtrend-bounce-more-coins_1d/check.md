---
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3148 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9152 | above 0 | no |
| Mean daily return | -0.0001898 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4388 | above 0 | no |
| Calmar | -0.129 | above 0.75 | no |
| Trades per day | 0.1092 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
