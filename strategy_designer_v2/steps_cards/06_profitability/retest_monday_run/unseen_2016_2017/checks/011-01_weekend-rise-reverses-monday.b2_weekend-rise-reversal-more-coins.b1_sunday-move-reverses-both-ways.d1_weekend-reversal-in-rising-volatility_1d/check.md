---
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5262 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.277 | above 0 | no |
| Mean daily return, on days in a position | -0.000893 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.318 | above 0 | no |
| Calmar | -0.2968 | above 0.75 | no |
| Trades per day | 0.09234 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.923 % |
| Yearly return | -10.3 % (over 1.99 years) |
| Days in a position | 28 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_monday_run/unseen_2016_2017/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
