---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.562 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.487 | above 0 | yes |
| Mean daily return, on days in a position | 0.003025 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.415 | above 0 | yes |
| Calmar | 1.706 | above 0.75 | yes |
| Trades per day | 0.1922 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.350 % |
| Yearly return | +44.8 % (over 10.59 years) |
| Days in a position | 37 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_learned_run/common/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
