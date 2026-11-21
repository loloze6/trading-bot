---
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3025 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2517 | above 0 | no |
| Mean daily return | 0.0003203 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1051 | above 0 | yes |
| Calmar | 0.06641 | above 0.75 | no |
| Trades per day | 0.1843 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
