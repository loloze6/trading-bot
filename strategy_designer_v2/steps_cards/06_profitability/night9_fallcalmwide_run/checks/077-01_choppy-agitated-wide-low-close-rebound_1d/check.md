---
backtest: 077-01_choppy-agitated-wide-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7858 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.233 | above 0 | yes |
| Mean daily return, on days in a position | 0.003333 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6804 | above 0 | yes |
| Calmar | 0.3247 | above 0.75 | no |
| Trades per day | 0.006229 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.102 % |
| Yearly return | +1.5 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-01_choppy-agitated-wide-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
