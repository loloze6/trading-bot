---
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1719 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4141 | above 0 | no |
| Mean daily return | 8.065e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1951 | above 0 | no |
| Calmar | 0.03054 | above 0.75 | no |
| Trades per day | 0.0295 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
