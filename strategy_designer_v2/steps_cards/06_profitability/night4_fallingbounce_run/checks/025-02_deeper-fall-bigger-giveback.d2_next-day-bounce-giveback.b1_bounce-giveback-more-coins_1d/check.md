---
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1505 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7509 | above 0 | no |
| Mean daily return | -4.034e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3126 | above 0 | no |
| Calmar | -0.07414 | above 0.75 | no |
| Trades per day | 0.1098 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
