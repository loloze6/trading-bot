# E-078 · Results of the one-time read-only run (2026-10-13)

Fragility condition, stated in README.md before this run: any leave-one-block-out whole-test Sharpe <= 0.

Command (from the operator checkout's `strategy-research/`, code at master `1e52bb1b`):
`../venv/Scripts/python.exe engineering/roadmap/E-078/leave_one_out_and_bh.py run_084 run_088 run_089`

Output, verbatim:

| Run | Whole-test Sharpe | Leave-one-block-out Sharpe (window left out) | Min | Fragile (any <= 0) | Basket buy-and-hold Sharpe |
|---|---|---|---|---|---|
| run_084 | 1.41 | 2018-05: 1.66, 2019-01: 1.31, 2019-09: 1.59, 2020-05: 1.18, 2021-01: 0.76, 2021-09: 1.87 | 0.76 | no | 0.91 |
| run_088 | 1.30 | 2018-05: 1.46, 2019-01: 1.33, 2019-09: 1.56, 2020-05: 0.89, 2021-01: 0.49, 2021-09: 1.94 | 0.49 | no | 0.91 |
| run_089 | 0.99 | 2018-05: 1.22, 2019-01: 0.90, 2019-09: 1.32, 2020-05: 0.71, 2021-01: 0.38, 2021-09: 1.31 | 0.38 | no | 0.91 |

None of the three is fragile under the condition. The weakest block for all three is 2021-01 (left out, the Sharpe drops most). All three whole-test Sharpes are above the basket buy-and-hold Sharpe on the same chain (0.91).
