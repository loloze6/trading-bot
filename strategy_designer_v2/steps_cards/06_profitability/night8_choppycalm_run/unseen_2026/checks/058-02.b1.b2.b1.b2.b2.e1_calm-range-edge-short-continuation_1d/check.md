---
backtest: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.108 | above 0 | yes |
| Sharpe minus holding's Sharpe | 2.042 | above 0 | yes |
| Mean daily return, on days in a position | 0.0023 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.467 | above 0 | yes |
| Calmar | 4.694 | above 0.75 | yes |
| Trades per day | 0.3996 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.363 % |
| Yearly return | +67.5 % (over 0.87 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2026/backtests/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
