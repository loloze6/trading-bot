---
backtest: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8284 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2756 | above 0 | yes |
| Mean daily return, on days in a position | 0.001069 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6829 | above 0 | yes |
| Calmar | 0.6702 | above 0.75 | no |
| Trades per day | 0.1889 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.390 % |
| Yearly return | +20.3 % (over 7.94 years) |
| Days in a position | 56 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
