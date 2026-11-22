---
backtest: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.373 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4649 | above 0 | no |
| Mean daily return | 0.002778 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.933 | above 0 | yes |
| Calmar | 7.741 | above 0.75 | yes |
| Trades per day | 0.2808 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
