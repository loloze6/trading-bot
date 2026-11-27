---
backtest: 077-03_choppy-agitated-close-position-reversal_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6988 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.146 | above 0 | yes |
| Mean daily return, on days in a position | 0.001098 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5724 | above 0 | yes |
| Calmar | 0.4147 | above 0.75 | no |
| Trades per day | 0.06148 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.260 % |
| Yearly return | +3.4 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03_choppy-agitated-close-position-reversal_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
