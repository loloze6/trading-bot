---
backtest: 039-02.d1_wide-range-low-close-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.26 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.93 | above 0 | no |
| Mean daily return, on days in a position | 0.00198 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7769 | above 0 | yes |
| Calmar | 1.743 | above 0.75 | yes |
| Trades per day | 0.3209 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.562 % |
| Yearly return | +39.3 % (over 1.99 years) |
| Days in a position | 52 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
