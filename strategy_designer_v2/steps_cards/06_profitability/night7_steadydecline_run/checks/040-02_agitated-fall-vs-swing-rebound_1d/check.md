---
backtest: 040-02_agitated-fall-vs-swing-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.852 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2824 | above 0 | yes |
| Mean daily return, on days in a position | 0.001129 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7315 | above 0 | yes |
| Calmar | 0.6858 | above 0.75 | no |
| Trades per day | 0.1727 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.853 % |
| Yearly return | +13.4 % (over 7.94 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/040-02_agitated-fall-vs-swing-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
