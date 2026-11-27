---
backtest: 076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6275 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.07469 | above 0 | yes |
| Mean daily return, on days in a position | 0.002334 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4313 | above 0 | yes |
| Calmar | 0.4997 | above 0.75 | no |
| Trades per day | 0.02135 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.296 % |
| Yearly return | +3.4 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
