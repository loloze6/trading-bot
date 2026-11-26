---
backtest: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4713 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4049 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006683 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.9406 | above 0 | no |
| Calmar | 0.8137 | above 0.75 | yes |
| Trades per day | 0.05181 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.626 % |
| Yearly return | +5.0 % (over 0.87 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2026/backtests/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
