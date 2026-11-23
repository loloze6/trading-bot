---
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.03796 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.1043 | above 0 | no |
| Mean daily return, on days in a position | -3.495e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.352 | above 0 | no |
| Calmar | -0.1414 | above 0.75 | no |
| Trades per day | 0.05001 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.946 % |
| Yearly return | -2.3 % (over 0.87 years) |
| Days in a position | 54 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/unseen_2026/backtests/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
