---
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8109 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2105 | above 0 | yes |
| Mean daily return | 0.0006375 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5239 | above 0 | yes |
| Calmar | 0.358 | above 0.75 | no |
| Trades per day | 0.2319 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
