---
backtest: 074-01.g1.d1_wide-close-high-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1351 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03703 | above 0 | yes |
| Mean daily return, on days in a position | 0.0003204 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.385 | above 0 | no |
| Calmar | 0.1301 | above 0.75 | no |
| Trades per day | 0.02285 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.195 % |
| Yearly return | +0.4 % (over 0.87 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2026/backtests/074-01.g1.d1_wide-close-high-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
