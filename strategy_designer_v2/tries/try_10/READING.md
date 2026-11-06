# try 10: branch 1 from the engine's outputs (fold A, BTCUSD 1h, claim range_break_strength, horizon 12, min_effect 0.03)
One engine run (six windows, two sizes) wrote both `engine_verdict.yaml` (branch 3) and `judge_verdict.yaml` (branch 1) in `tries/try_09/engine_fold_A/`.

| window | event bars | event-bar correlation | all-bars correlation |
|---|---|---|---|
| W1 | 29 | +0.2861 | -0.0253 |
| W2 | 30 | +0.2731 | -0.0058 |
| W3 | 32 | +0.1015 | -0.0214 |
| W4 | 39 | -0.0346 | -0.0029 |
| W5 | 31 | +0.1023 | -0.0169 |
| W6 | 29 | +0.0461 | -0.0389 |

Fold (pooled event bars): n = 190, correlation +0.1639, t-statistic 2.28 (information only). All-bars correlation, pooled: -0.0170.
Verdict: **pass**. Checks: fold correlation >= 0.03 yes; same sign as the fold in >= 5 of 6 windows yes (5); pooled event bars >= 30 yes.
Engine branch 3 on the same run: fail (full size and vol target both lose 90%+ per window), as in try 09.

Reading: on event bars the engine's graded forecast ranks the next 12h return (+0.16); on all bars it has no relation (-0.02). The idea is right where it fires; the book that trades every bar loses to churn.

One-window folder (`tries/try_09/engine`, CLI): W1 n=29, correlation +0.2861, fold +0.2861, t 1.55, verdict fail (pooled events 29 < 30). Output says "only 1 window(s): same-sign check needs 1".
