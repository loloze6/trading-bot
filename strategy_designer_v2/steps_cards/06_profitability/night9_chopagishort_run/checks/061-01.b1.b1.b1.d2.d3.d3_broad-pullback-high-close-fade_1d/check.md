---
backtest: 061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3537 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9611 | above 0 | no |
| Mean daily return, on days in a position | -0.0001841 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5802 | above 0 | no |
| Calmar | -0.09262 | above 0.75 | no |
| Trades per day | 0.05913 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.214 % |
| Yearly return | -1.5 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
