---
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2284 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.8468 | above 0 | no |
| Mean daily return, on days in a position | 0.0002151 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.08157 | above 0 | yes |
| Calmar | 0.0466 | above 0.75 | no |
| Trades per day | 0.3584 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.149 % |
| Yearly return | +2.6 % (over 10.59 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
