---
backtest: 061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2274 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3801 | above 0 | no |
| Mean daily return, on days in a position | 0.0004667 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1132 | above 0 | no |
| Calmar | 0.09642 | above 0.75 | no |
| Trades per day | 0.04816 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.666 % |
| Yearly return | +2.1 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
