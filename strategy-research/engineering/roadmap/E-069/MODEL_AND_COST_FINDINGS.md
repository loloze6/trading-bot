# E-069: model and cost findings (read before changing any stage's model)

E-069 ("Each AI step can use its own model", Linear P-CUL-77) is parked. This file keeps
what the analyst smokes of 2026-10-09/10 taught about models and costs, so that whoever builds
E-069, or changes the model of any stage, starts from it. Every fact has its source; line
numbers are those of master `52bb0fa3` (2026-10-10).

## 1. Which model each stage uses

- Every Claude stage runs on one model: `_CLAUDE_WORKER_MODEL = "claude-haiku-4-5"`
  (`workflow/run_phase1_research.py:1113`, passed at `:1179` by `_stage_agent_options`).
- A stage runs on Gemini instead only when its handoff says `assigned_engine: gemini`
  (`:10580-10587`); the default is Claude.
- The analyst (E-075) is the only stage with its own model setting:
  `orchestrator.analyst.model` in `config/campaign_config.yaml`, read by `_analyst_caps`
  (`:5000`, default `_CLAUDE_WORKER_MODEL`). Its caps: 40 turns, $3, 15 minutes
  (`_ANALYST_DEFAULT_CAPS`, `:4973`; $1.50 until D-097's PR, #371).

## 2. `cost_usd` is the CLI's estimate, not the bill

- Every Claude stage runs through `claude-agent-sdk` 0.2.82 (pinned,
  `config/requirements-mac.txt:29`), which runs its bundled Claude Code CLI, version 2.1.142.
  `cost_usd` in the audit log is that CLI's own estimate.
- The CLI 2.1.142 binary does not contain the strings `claude-haiku-5-5` or
  `claude-sonnet-5-5` (byte search, 2026-10-09). It still runs them, but prices them with a
  fallback.
- Measured (smoke 5, `claude-haiku-5-5`): a least-squares fit of the four audit entries'
  tokens against their `cost_usd` gives about $24.6 per million output tokens, $0.48 per
  million cache reads and $7.05 per million cache writes, i.e. about Opus list rates, fitting
  all four within $0.001. At the Haiku 5.5 list price the same tokens cost about $0.06
  instead of the $3.11 reported (estimate: cache prices assumed at 1.25x / 0.1x input).
- The token counts in the audit log are exact (`_usage_token_record`); the real bill is in
  the Console.
- The caps are enforced on that estimate: `max_budget_usd` reaches the CLI as
  `--max-budget-usd` (`run_phase1_research.py:1194`; `claude_agent_sdk/_internal/transport/
  subprocess_cli.py:262-263`). With a model the CLI does not know, a session can be stopped
  far below its real cost.
- Upgrading the SDK/CLI fixes the price list but changes every stage at once (the
  result-misclassification workaround at `run_phase1_research.py:776-791` is written against
  this install): treat it as its own change, with a smoke.

## 3. The run's token budget ignores the model's price

- The budget gate sums weighted token units with fixed ratios: input 1, output 5, cache read
  0.1, cache write 1.25 (`_TOKEN_WEIGHT_*`, `run_phase1_research.py:918-921`).
- So moving a stage from Haiku to Sonnet uses the same budget units for many times the
  dollars. Per-stage models need a per-model price, or a dollar budget, beside this one.

## 4. Which model answered is not always recorded

- The analyst records it in each attempt and audit entry (`models`, `:5196`, `:5228`;
  since #371).
- The other stages record it only under the score-provenance flag
  (`_score_provenance_enabled`, `:4007`; read at `:1408`, `:4940`, `:5742`).
- Smoke 5's served model was established from the CLI's own transcripts, not from the run's
  records. Record the served model in every stage before comparing models.

## 5. A retry is a fresh, full-price session

- Each retry starts a new session: its whole prompt is written to the cache again (smokes 5
  and 6: 63,272 to 68,394 cache-write tokens for a one-turn retry, against 1,321 cache-read
  tokens). In smoke 5 the one-turn retries were about 35% of each lens's estimated real
  cost (forecast $0.011 of $0.032, trade_efficiency $0.010 of $0.027, at list price). A rule
  that refuses often is paid in fresh sessions.

## 6. The smoke results (copies of run_074, outside the repository)

| Smoke | Model | Reported `cost_usd` (both lenses) | What was accepted |
|---|---|---|---|
| 2-4 | `claude-haiku-4-5` (known to the CLI: real price) | $0.89-0.92 each | 2 of 6 lens sessions, neither usable |
| 5 | `claude-haiku-5-5` | $3.11 (estimate at list price: about $0.06) | 2 of 2: a weak claim (after a no_claim to claim flip), an honest no_claim |
| 6 | `claude-sonnet-5-5` | $2.83 (estimate at list price: about $1.05) | 1 of 2: a plausible claim (lots opened at a forecast of -15 or lower earn less, 5 of 6 windows) |

Tokens per attempt (input / output / cache read / cache write):

| Smoke, lens, attempt | Tokens |
|---|---|
| 5 forecast, 1st (17 turns) | 40 / 11,933 / 569,000 / 74,775 |
| 5 forecast, retry (1 turn) | 4 / 6,084 / 1,321 / 63,982 |
| 5 trade_efficiency, 1st (11 turns) | 32 / 7,973 / 430,677 / 67,770 |
| 5 trade_efficiency, retry | 4 / 3,624 / 1,321 / 63,272 |
| 6 forecast, 1st (17 turns) | - / 6,698 / 578,554 / 73,748 |
| 6 forecast, retry | - / 1,417 / 1,321 / 68,394 |
| 6 trade_efficiency, 1st (16 turns) | - / 4,166 / 620,621 / 65,604 |
| 6 trade_efficiency, retry | - / 1,250 / 1,321 / 64,045 |

Sonnet 5.5 wrote fewer output tokens than Haiku 5.5 on the same lens (6,698 against 11,933).
Two sessions per model cannot choose a model: the pilot (E-075 PR5_RUNBOOK section 2a) is
the comparison, on the same runs for each model.

## 7. Where the prices come from

The list prices used above ($0.10 / $0.50 per million tokens for Haiku 5.5, $2 / $10 for
Sonnet 5.5, cache reads $0.20 for Sonnet 5.5) come from Claude Code's API reference price
table (cached 2026-10-06), not from the live price page; the Haiku 5.5 price holds for
prompts up to 100K tokens. The Console usage page is the only proof of a bill.

## 8. Checklist before changing a stage's model

1. The SDK's bundled CLI knows the model (search its binary for the id), or the stage's cost
   and caps are understood to be a fallback estimate.
2. The caps: a dollar cap is enforced on the CLI's estimate; a turn or time cap is not.
3. The run's weighted token budget (section 3) still means what you want.
4. The stage records the model that answered (section 4).
5. One smoke on a copy of a run first, its tokens and records read, before any campaign run.
