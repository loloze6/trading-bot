# E-062 signing checklist (for the operator)

What this is: every number the operator has agreed to but not yet signed, in one
place, with what it means in one line. Nothing here changes any file by itself.
It is deliberately NOT a comment block at the top of `config/profitability_bars.yaml`,
because any byte change to that file changes its sha256 (see "The sha" below).

Everything below is read only when `orchestrator.profit_bars_v2.enabled` is on,
except where noted. The values were agreed in D-039, D-046 and D-047; the
definitions they apply to are D-034..D-038, D-041, D-046 and D-047
(`engineering/DECISION_LOG.md`).

## 1. `config/profitability_bars.yaml` (ten values, then the signature)

| Key | Value | What it means, in one line |
|---|---|---|
| `sharpe_min` | 1.0 | Floor on the whole-test Sharpe (mean / stdev of the chained daily returns of the equal-weight portfolio, times sqrt(365), risk-free 0). D-036, D-039. |
| `avg_daily_return_min` | 0.0005 | Floor on the mean daily return of that same chained curve: 0.05 % per day. Kept from before. D-039. |
| `deflated_sharpe_threshold` | 0.95 | Floor on the luck-corrected (deflated) Sharpe. **The number is unchanged but its meaning changed with D-046:** it is now the Bailey and Lopez de Prado 2014 formula on the whole-test daily Sharpe, so signing it re-signs the new meaning (measured hurdle at N = 12 trials: about 1.2 annualised Sharpe over roughly 2700 days, about 1.7 over roughly 1400 days). |
| `max_drawdown_pct_max` | 20.0 | Ceiling, in percent, on the largest peak-to-trough fall of the chained bar-level curve over the WHOLE test period (stricter than the old worst-single-window meaning). D-034, D-039. |
| `trade_count_min` | 100 | Floor on trades per coin over the whole test, not counting the forced close at each window end. D-035. |
| `buy_and_hold_excess_return_min` | 0.0 | The strategy's total return must be strictly above equal-weight buy-and-hold over the same days, after one round trip of costs. D-037. |
| `cost_edge_ratio_min` | 2.2 | Pooled realised gross edge over cost must be strictly above 2.2, i.e. it survives doubled costs including doubled slippage. D-038, D-039. |
| `cost_edge_min_trades` | 100 | Below this many non-forced trades the cost-ratio bar is NOT_EVALUABLE rather than PASS or FAIL. D-038, D-039. |
| `dsr_min_same_basis_trials` | 10 | With fewer than this many trials scored on the same whole-test basis, the deflated Sharpe compares against the pure-luck spread; from this many on, against the spread of those trials themselves. D-046. |
| `trade_count_min_floor` | 60 | Absolute lower limit on the scaled trade minimum (and the cost-ratio trade floor) of a partial-coverage variant: `max(ceil(100 * f), 60)`. Inert while the D-042 coverage minimum is 60 %, so it acts only as a guard. D-047. |

Not a bar, nothing to decide: `target_instrument_set` (BTCUSDT, ETHUSDT) is metadata.
The drawdown scaling for partial coverage (`limit * sqrt(f)`) is in code, not in the
file, and needs no signature (D-047).

**Where the signature goes.** The two keys `ratified_by:` (a name, currently
`null`) and `ratified_at:` (an ISO date; an unquoted YAML date is accepted), which
sit after `target_instrument_set` in the same file. The loader does not check them: signing is a human
review, not a schema check.

## 2. `config/criterion_menu.yaml` (a different file, a different sha)

| Entry | Value | What it means, in one line |
|---|---|---|
| `realized_edge_to_cost_ratio` | threshold 2.2, `min_trades` 100 | The idea-level twin of the two cost rows above (same numbers, slightly different definition, still optional at step 1a). D-038, D-039. |
| `code_added_criteria.residual_ic` | threshold 0.02, `max_p_value` 0.05, `min_n_eff` 30 | A candidate block's residual IC (after fitting on the current composite's forecast) must exceed 0.02, one-sided p below 0.05, on at least 30 effective independent observations. Composition runs only. D-039. |

Where the signature goes: flip `ratified: false` to `ratified: true` on the
`residual_ic` entry. There is no `ratified_by` field in this file.

## 3. The sha, and why to sign before the first real run

- Every evaluation records the sha256 of the bars file it was graded under
  (`bars_file_sha256`). A holdout `spend` refuses (`bars_changed`) if the file's
  sha256 now differs. So an evaluation graded BEFORE the signature cannot be spent
  AFTER it, and signing must come before the first real run (C4).
- Current sha256 of `config/profitability_bars.yaml`, unsigned, as committed (LF line
  endings, what git stores): `29aa264251c1c95c30227302ab08e59954a0e521b6922c73a8d1e3d303373fb6`.
  It is a fact about this commit, not a permanent value: signing changes it.
- **CUL-348 caveat.** The sha depends on line endings. The same file read from a
  Windows checkout with CRLF conversion hashes to
  `08aea0ca336962b6507d7b8d723cb57963fc04c101eaf30724c9de6aca03989f`. A grading on
  one checkout and a spend on the other would disagree. Until CUL-348 is resolved,
  grade and spend from one checkout with one line-ending setting, and write down
  which one.
- After signing, commit the file and record the new sha256 of the LF blob
  (`git show HEAD:strategy-research/config/profitability_bars.yaml | sha256sum`)
  next to the signature, so a later `bars_changed` can be told apart from an
  accidental edit.

## 4. Order of work

1. Read sections 1 and 2; change any value the operator wants different BEFORE
   signing (a change after is another signature).
2. Write `ratified_by` / `ratified_at` in the bars file and flip `ratified` in the
   menu. Commit both. Record the new LF sha256.
3. Only then switch the flag set on for the first real run.

## 5. Signed (2026-09-29)

- The operator agreed every value above unchanged ("I agree with the bars, can you ratify it for me"); Claude
  recorded the signature at that explicit instruction in commit `cdb1d577`: `ratified_by` / `ratified_at: 2026-09-29`
  in `config/profitability_bars.yaml`, and `ratified: true` on `residual_ic` in `config/criterion_menu.yaml`.
- sha256 of the signed bars file:
  - committed LF blob (what git stores; a Mac or Linux checkout): `43de386832865bb5367db32a33f485b838528d995f39c31117b9fa657682cbaa`
  - this Windows checkout (`core.autocrlf=true`, CRLF on disk -- what the runtime hashes here): `a752a2ebb60bb4ed7e6577fcd9449db1be28dd8767bc571ca3ba86e0f1bcad71`
- Until CUL-348 lands, grade and spend on the same checkout; C4 on this Windows machine records the CRLF value.
