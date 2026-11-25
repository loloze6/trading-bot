---
backtest: 054-02.b1_reclaim-rebound-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2117 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3411 | above 0 | no |
| Mean daily return, on days in a position | 0.001027 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1126 | above 0 | yes |
| Calmar | 0.1183 | above 0.75 | no |
| Trades per day | 0.008429 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.256 % |
| Yearly return | +0.9 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-02.b1_reclaim-rebound-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
