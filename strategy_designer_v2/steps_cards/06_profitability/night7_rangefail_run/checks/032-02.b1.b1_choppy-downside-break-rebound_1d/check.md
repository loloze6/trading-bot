---
backtest: 032-02.b1.b1_choppy-downside-break-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4932 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1143 | above 0 | no |
| Mean daily return, on days in a position | 0.0006165 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3546 | above 0 | yes |
| Calmar | 0.2433 | above 0.75 | no |
| Trades per day | 0.002604 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.023 % |
| Yearly return | +0.2 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-02.b1.b1_choppy-downside-break-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
