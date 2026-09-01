# E-041 — Every feature flag gets an owner and a switch-on criterion

**State:** new
**Owner:** Jérémy
**Updated:** 2026-08-31

## Why

**Eight feature flags. All `False`. None has ever been switched on.**

Measured 2026-08-31 across the engine and the orchestrator:

| Flag | What it buys | Runs using it |
|---|---|---|
| `model_funding` | Perp funding accrual — the cost side of every held position | **0** |
| `bar_equity` | Bar-level max-drawdown and Sharpe, plus textbook Sortino | **0** |
| `orchestrator.variant_selection_record.enabled` | Which variant was chosen, and the discards | **0** |
| `orchestrator.variant_anti_adjacency_gate.enabled` | Is this candidate a repeat? | **0** |
| `orchestrator.exclusion_digest_input.enabled` | What the campaign has already excluded | **0** |
| `orchestrator.schedulability_block.enabled` | Can this actually be run today? | **0** |
| `orchestrator.anti_adjacency_retry.enabled` | Retry routing | **0** |
| `orchestrator.stale_input_path_fix.enabled` | Input-path correctness | **0** |

`tools/run_protocol.py` — the only caller that matters — passes
`warmup_prefetch=True` explicitly and passes **neither** `bar_equity` nor
`model_funding`. Zero artifacts anywhere contain a `bar_equity` block.

Recorded as [E037-42](../E-037/FINDINGS.md#e037-42) and
[E037-21](../E-037/FINDINGS.md#e037-21).

### This is a process defect, not eight coding defects

The project's rule is sound and should not change:

> *New features ship off-by-default with a test proving byte-identical default
> behaviour.*

That protects every prior baseline from silent invalidation, and it is why this
codebase can be trusted at all. **What is missing is the other half: nothing in
the process ever flips one on.**

So the discipline that was built to make change safe has become the reason no
change lands. An off-by-default flag with no switch-on plan is not a safe
default — it is **an abandoned feature with a test suite**.

### The measured cost of one of them

For `bar_equity`, the fork's own reference figures on the same run:

```
bar-level Sharpe   -5.12      trade-exit Sharpe   -5.65
bar-level maxDD   -24.77%     trade-exit maxDD   -24.59%
```

Every research verdict to date was decided on the trade-exit numbers, because
the bar-level block has never been produced. The gap is not large here, but
**which of the two is correct is not a matter of taste** — the bar-level one
is, which is why it was built.

For `model_funding` it is worse: not merely off, but unavailable below daily
bars. See [E-014](../E-014/EPIC.md)'s "Blocker found by E-037" section (E-042
was drafted for this, then deleted as a duplicate once E-014 was found to
already own the question — see [E037-43](../E-037/FINDINGS.md#e037-43)).

---

## Scope

### In

- A **switch-on criterion recorded at creation**: every new off-by-default flag
  states, in its own docstring or config comment, *"on once X is true"* and who
  owns that call.
- A **register** of current flags with owner, criterion and status — one place,
  mechanically checkable against the code so it cannot drift.
- A **decision on each of the eight**: turn on, delete, or record the criterion
  that is still unmet. "Leave it off with no reason" stops being an option.
- A test that a new default-`False` flag cannot land without a criterion.

### Out

- Turning any specific flag on. That is each flag's own decision, and two of
  them have owners elsewhere — [E-033](../E-033/EPIC.md) D1 for
  `variant_selection_record`, [E-014](../E-014/EPIC.md) for `model_funding`.
- Changing the off-by-default rule itself. It is correct.

---

## Stages

- [ ] **S1 — Characterise and stop.** For each of the eight: who added it, what
      it was waiting for, and whether that condition is now met. Several may
      simply be ready. Report, then stop for Jérémy's per-flag calls.
- [ ] **S2 — (blocked on S1) The register.** One file, plus a test that every
      default-`False` flag in the engine and `campaign_config.yaml` appears in
      it with an owner and a criterion.
- [ ] **S3 — (blocked on S1) Act on the decisions.** Each flag turned on,
      deleted, or documented as blocked with its criterion stated.

## Risks

- **Turning several on at once invalidates baselines simultaneously**, and you
  lose the ability to attribute a behaviour change to a specific flag. One at a
  time, each with its bit-identity proof.
- **The register drifts** — which is the same failure this epic is about, one
  level up. It must be generated or tested against the code, never hand-
  maintained. E-037 has three ratchet tests that are the model for this.

## Log

- 2026-08-31 — `new`. Found by the flag sweep that
  [E037-38](../E-037/FINDINGS.md#e037-38) implied: orchestrator flags had been
  swept during E-037, engine flags never had, and `model_funding` surfaced by
  accident while answering Jérémy's question about the funding epic. The sweep
  then found `bar_equity` and made it a class.
