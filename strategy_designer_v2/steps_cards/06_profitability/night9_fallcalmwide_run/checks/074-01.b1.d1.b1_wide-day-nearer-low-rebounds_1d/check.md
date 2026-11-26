---
backtest: 074-01.b1.d1.b1_wide-day-nearer-low-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8049 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2521 | above 0 | yes |
| Mean daily return, on days in a position | 0.003351 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6381 | above 0 | yes |
| Calmar | 0.4936 | above 0.75 | no |
| Trades per day | 0.01893 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.296 % |
| Yearly return | +4.5 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b1.d1.b1_wide-day-nearer-low-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
