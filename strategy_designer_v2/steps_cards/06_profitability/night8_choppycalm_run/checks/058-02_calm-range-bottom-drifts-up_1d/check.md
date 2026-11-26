---
backtest: 058-02_calm-range-bottom-drifts-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2031 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7727 | above 0 | no |
| Mean daily return, on days in a position | -0.0003918 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3964 | above 0 | no |
| Calmar | -0.08517 | above 0.75 | no |
| Trades per day | 0.05663 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.504 % |
| Yearly return | -2.4 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02_calm-range-bottom-drifts-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
