---
backtest: 068-02_falling-agitated-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7413 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1717 | above 0 | yes |
| Mean daily return, on days in a position | 0.002202 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5508 | above 0 | yes |
| Calmar | 0.3572 | above 0.75 | no |
| Trades per day | 0.043 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.492 % |
| Yearly return | +6.7 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/068-02_falling-agitated-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
