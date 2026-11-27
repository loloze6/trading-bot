# Portfolio versions (every version tried stays listed)

| Version | Commit | Books | In-sample | Unseen coins |
|---|---|---|---|---|
| v1 | 438b097e9d | 9 books | in-sample Sharpe 1.973 | unseen coins Sharpe 0.989 ((a) 0.986, P4 0.134); 7 of 8 books hold alone |
| v2 | 150ce85532 | 10 books | in-sample Sharpe 2.055 | unseen coins Sharpe 1.008 ((a) 0.998, P4 0.134); 8 of 9 books hold alone |
| v2b | b30c67e224 | 10 books | in-sample Sharpe 2.055 | unseen coins Sharpe 1.008 ((a) 0.998, P4 0.134); 8 of 9 books hold alone |

## Versions by rule, on the common records (common/data_use.md, steps 10 to 12)

Correction of 2026-11-27 (next steps A10, `runs/BUILD_A8_A10.md`): holding's Sharpe for v3 and v4 was listed as 1.075.
That figure moved with the order of the strategies (0.945 in the order of `portfolio.json`) and was read from the
chart files' closes, which are rounded. It is now read from the coins' data files on the version's coin-days: **1.058**,
in every order. Both versions stay ready; their own Sharpe (1.914) is unchanged. The column "Yearly at a 20 % worst
fall" is new (A11): informative, before any cost of leverage, in no rule. Each version's `measures.json` is as built;
the figures measured again are in its `measured_again.json`.

| Version | Commit | Candidates | Books | Portfolio coins: Sharpe (holding) | Yearly at a 20 % worst fall (scale) | Ready | Final test |
|---|---|---|---|---|---|---|---|
| v3 | 0f2ce199b1 | 129 | 11 | 1.914 (1.058) | +47.9% (x 2.12) | ready | not made |
| v4 | 210187f965 | 131 | 11 | 1.914 (1.058) | +47.9% (x 2.12) | ready | not made |
