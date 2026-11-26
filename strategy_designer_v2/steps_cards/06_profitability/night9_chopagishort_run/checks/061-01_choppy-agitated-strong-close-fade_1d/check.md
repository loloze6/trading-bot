---
backtest: 061-01_choppy-agitated-strong-close-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3208 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2488 | above 0 | no |
| Mean daily return, on days in a position | 0.001181 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2107 | above 0 | yes |
| Calmar | 0.1662 | above 0.75 | no |
| Trades per day | 0.01748 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.280 % |
| Yearly return | +1.6 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01_choppy-agitated-strong-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
