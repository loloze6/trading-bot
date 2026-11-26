---
backtest: 058-02_rising-calm-below-recent-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6324 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.06278 | above 0 | yes |
| Mean daily return, on days in a position | 0.001609 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4338 | above 0 | yes |
| Calmar | 0.4184 | above 0.75 | no |
| Trades per day | 0.08268 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.984 % |
| Yearly return | +10.7 % (over 7.94 years) |
| Days in a position | 20 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02_rising-calm-below-recent-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
