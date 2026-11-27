---
backtest: 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5722 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01938 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006951 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4771 | above 0 | yes |
| Calmar | 0.5951 | above 0.75 | no |
| Trades per day | 0.00595 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.051 % |
| Yearly return | +0.6 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
