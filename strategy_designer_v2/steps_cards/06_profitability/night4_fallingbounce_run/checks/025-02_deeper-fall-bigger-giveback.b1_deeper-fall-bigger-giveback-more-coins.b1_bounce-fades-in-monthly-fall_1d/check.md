---
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5945 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.005899 | above 0 | no |
| Mean daily return | 4.004e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4769 | above 0 | yes |
| Calmar | 0.5123 | above 0.75 | no |
| Trades per day | 0.005358 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
