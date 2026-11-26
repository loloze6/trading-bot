---
backtest: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.119 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7264 | above 0 | no |
| Mean daily return, on days in a position | -0.0003998 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2442 | above 0 | no |
| Calmar | -0.04905 | above 0.75 | no |
| Trades per day | 0.02725 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.457 % |
| Yearly return | -1.4 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
