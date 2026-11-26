---
backtest: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6354 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7018 | above 0 | no |
| Mean daily return, on days in a position | -0.001635 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9873 | above 0 | no |
| Calmar | -0.7203 | above 0.75 | no |
| Trades per day | 0.02033 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.321 % |
| Yearly return | -4.0 % (over 0.87 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
