---
backtest: 039-02.d1_wide-range-low-close-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2335 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.3316 | above 0 | no |
| Mean daily return, on days in a position | -0.0002886 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5253 | above 0 | no |
| Calmar | -0.3924 | above 0.75 | no |
| Trades per day | 0.2747 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.244 % |
| Yearly return | -8.0 % (over 0.87 years) |
| Days in a position | 53 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
