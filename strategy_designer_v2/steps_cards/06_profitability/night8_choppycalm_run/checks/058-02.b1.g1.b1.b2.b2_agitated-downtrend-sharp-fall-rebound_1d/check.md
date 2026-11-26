---
backtest: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9347 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3819 | above 0 | yes |
| Mean daily return, on days in a position | 0.001877 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7564 | above 0 | yes |
| Calmar | 0.7979 | above 0.75 | yes |
| Trades per day | 0.07258 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.491 % |
| Yearly return | +8.7 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
