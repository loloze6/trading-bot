---
backtest: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.222 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6145 | above 0 | yes |
| Mean daily return, on days in a position | 0.001776 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.078 | above 0 | yes |
| Calmar | 1.01 | above 0.75 | yes |
| Trades per day | 0.1027 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.733 % |
| Yearly return | +17.5 % (over 7.94 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
