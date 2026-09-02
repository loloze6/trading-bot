# E-041 — Every feature flag gets an owner and a switch-on criterion

**State:** in-progress — S1 and S3 done, S2 (the register) remains
**Owner:** Jérémy
**Updated:** 2026-09-02

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

- [x] **S1 — Characterise and stop.** Done 2026-09-02. All eight checked
      against commit history and config comments: none had a stated switch-on
      criterion — the blanket ship-off-by-default rule was the entire
      explanation. Two (`anti_adjacency_retry`, `variant_anti_adjacency_gate`)
      turned out not to be simple activations at all: E-036's fix is built
      and verified working as designed, but Jérémy **rejected the design
      itself** on review (2026-09-02) — see [E-036](../E-036/EPIC.md)'s
      rejection entry. These two are **incomplete, out of radar** until
      E-036 restarts, same footing as `model_funding` and E-014.
- [ ] **S2 — (blocked on S1) The register.** One file, plus a test that every
      default-`False` flag in the engine and `campaign_config.yaml` appears in
      it with an owner and a criterion. **Not yet built** — the per-flag
      decisions below are its input.
- [x] **S3 — (blocked on S1) Act on the decisions.** Done 2026-09-02, one flag
      per commit: `bar_equity` (PR #95), `exclusion_digest_input` (PR #96),
      `stale_input_path_fix` (PR #97), `variant_selection_record` +
      `schedulability_block` (PR #98). Final state, all eight:

      | Flag | State | Reason |
      |---|---|---|
      | `bar_equity` | **ON** | Proven since 2026-07-31, no criterion unmet |
      | `exclusion_digest_input` | **ON** | Digest file exists on disk, fires immediately |
      | `stale_input_path_fix` | **ON** | Both target files verified present |
      | `variant_selection_record` | **ON** | Compliance checked before flipping (see PR #98) |
      | `schedulability_block` | **ON** | Purely additive, no consumer yet |
      | `model_funding` | **incomplete** | Unavailable below daily bars — a real gap, not a caution. Out of radar until E-014 restarts |
      | `anti_adjacency_retry` | **incomplete** | E-036's fix is built and works as designed, but Jérémy rejected the design itself. Out of radar until E-036 restarts |
      | `variant_anti_adjacency_gate` | **incomplete** | Same E-036 rejection, same mechanism |

      None of the three "incomplete" rows is a flag decision at all — each
      names a piece of work that has to happen in its own epic first.
      Guard tests for all eight now live in
      `tests/test_campaign_config_e041_flags.py`, including two asserting the
      incomplete pair stay off until E-036 restarts.

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

---

## Decision (Jérémy, 2026-09-01): switch them on

> *"then lets turn it on. i do not see reasons to be extra careful. we would
> develop and continue developing new features. if we spend time and time being
> cautious about activating a feature we would not progress."*

**Recorded as a standing principle, not a one-off call: the default for a
finished, tested feature is ON. Staying off is the exception and needs a stated
reason.** The off-by-default rule protects the moment a feature *lands* — it was
never meant to be where features permanently live. An off flag with no
switch-on plan is an abandoned feature with a test suite.

**The "it invalidates baselines" objection is weak here and must not be used to
delay.** Zero strategies have ever been promoted, so the existing corpus is a
pile of kills, not a baseline worth protecting. The one discipline worth
keeping costs nothing: **turn them on one at a time**, so a behaviour change
stays attributable to a specific flag.

**Verified 2026-09-01, answering "was there a reason each was switched off?" —
no.** Every commit message and config comment says only "off by default" and
cites its epic; **not one states a condition for turning on.** There is no
per-flag rationale to recover. The blanket ship-off-by-default rule is the
entire explanation, which is precisely this epic's finding.

**Two exceptions, both with reasons:**

- **`model_funding` — STAYS OFF.** Jérémy: *"a partially working feature
  (funding) is a delayed bomb until a bug is found."* It raises on anything
  below daily bars, so it is not a finished feature and the principle above
  does not apply to it. Unblocking it belongs to [E-014](../E-014/EPIC.md).
  **This is the shape of a legitimate exception: not "we are being careful",
  but "the feature is incomplete."**
- **`variant_selection_record`** — tied to [E-033](../E-033/EPIC.md) D1's
  variant-count work, but Jérémy's call is that this does **not** block turning
  it on now.

**A third exception surfaced only once S3 actually checked each flag
individually (2026-09-02), not visible from this decision alone:**
`anti_adjacency_retry` and `variant_anti_adjacency_gate` looked ready — their
underlying fix (E-036) was built and verified working. But reviewing that
fix on its own merits, Jérémy **rejected the design**, not merely its
completeness — see [E-036](../E-036/EPIC.md)'s rejection entry. Same shape of
exception as `model_funding`: **incomplete, not a caution.**

So: **5 of 8 on. Three incomplete, each with its own epic to finish first:**
`model_funding` (E-014), `anti_adjacency_retry` + `variant_anti_adjacency_gate`
(E-036).
