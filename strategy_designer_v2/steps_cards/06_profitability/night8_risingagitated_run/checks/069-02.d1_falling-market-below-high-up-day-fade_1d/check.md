---
backtest: 069-02.d1_falling-market-below-high-up-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.294 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2601 | above 0 | no |
| Mean daily return, on days in a position | 0.0004261 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1075 | above 0 | yes |
| Calmar | 0.1604 | above 0.75 | no |
| Trades per day | 0.1149 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.696 % |
| Yearly return | +3.1 % (over 7.94 years) |
| Days in a position | 25 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d1_falling-market-below-high-up-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
