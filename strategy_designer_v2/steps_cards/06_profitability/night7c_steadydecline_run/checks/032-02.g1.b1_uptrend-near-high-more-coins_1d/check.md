---
backtest: 032-02.g1.b1_uptrend-near-high-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.213 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6056 | above 0 | yes |
| Mean daily return, on days in a position | 0.001539 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9813 | above 0 | yes |
| Calmar | 1.265 | above 0.75 | yes |
| Trades per day | 0.1865 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.567 % |
| Yearly return | +37.5 % (over 7.94 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.b1_uptrend-near-high-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
