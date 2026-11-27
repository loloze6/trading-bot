---
backtest: 067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1443 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7517 | above 0 | no |
| Mean daily return, on days in a position | -0.0002742 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.26 | above 0 | no |
| Calmar | -0.08179 | above 0.75 | no |
| Trades per day | 0.03334 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.016 % |
| Yearly return | -4.6 % (over 7.94 years) |
| Days in a position | 28 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
