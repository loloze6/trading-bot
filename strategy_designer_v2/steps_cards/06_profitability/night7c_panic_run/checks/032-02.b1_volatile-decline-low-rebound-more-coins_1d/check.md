---
backtest: 032-02.b1_volatile-decline-low-rebound-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.202 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4481 | above 0 | no |
| Mean daily return, on days in a position | 0.0003103 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.04322 | above 0 | yes |
| Calmar | 0.1389 | above 0.75 | no |
| Trades per day | 0.002791 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.199 % |
| Yearly return | +0.7 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b1_volatile-decline-low-rebound-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
