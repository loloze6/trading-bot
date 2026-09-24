# E-059 S2a — open question from the code review (fix 4)

## Question: should the legacy B11 and CUL-267 lints run on the 1a pass_rule?

Review fix 4 asked for the full registration lint chain on the pass_rule built
from the 1a card: B11 `_lint_pass_rule_total_mapping`, CUL-267
`verdict_criteria_evaluator.lint_pass_rule_structure`, and the K3
`window_set_ref` check.

**What was built:**
- the K3 check (`_lint_machine_constraints_protocol_selection`);
- card criteria limited to `id` plus the menu entry's new `card_overridable`
  list (`config/criterion_menu.yaml`: `[]` for `realized_edge_to_cost_ratio`,
  `[metric]` for `sign_consistent_by_era`, following that entry's own comment),
  with stray keys refused;
- the merge reused from the grid (`resolve_criteria_against_menu`, split out of
  `_resolve_grid_criteria`).

**Why B11 and CUL-267 were not wired in:** both lints were written for the
legacy pass_rule shape (`metric` / `comparator` / `threshold`, `outcomes`,
`metric_basis`, `null_handling`). They refuse both live menu entries exactly as
the menu defines them.

This was measured with system python against `config/criterion_menu.yaml`, with
each entry resolved and `basis` removed:

| entry | B11 violations | CUL-267 violations |
|---|---|---|
| `realized_edge_to_cost_ratio` | no `outcomes`; no `metric_basis` | `null_handling` is None |
| `sign_consistent_by_era` | no `outcomes`; invalid `comparator`; no `metric_basis` | `comparator` is None; `null_handling` is None |

Wiring them in would therefore refuse every decide-next candidate. The grid
(`evaluate_grid`) needs none of these fields: `sign_consistent_by_era` has no
comparator by design (see the menu comment).

**Decision needed (pick one):**
- (a) Add menu-aware branches to B11 and CUL-267, so menu-shaped criteria are
  checked only for what `evaluate_grid` reads.
- (b) Add the missing fields to the menu entries. This would change the grid's
  resolved criteria and needs its own byte-identity review.
- (c) Accept the current scope: menu-only ids, the `card_overridable`
  allowlist and K3.

This also affects any hand-registered menu-shaped brief that goes through
`_materialize_run`, which runs the same two lints today (no such brief exists on
disk).

---

## Decision (operator, 2026-09-24): option (c)

Keep the current checks on the 1a pass_rule: criteria must be menu ids, overrides
only from the menu entry's `card_overridable` list (stray keys refused), and the K3
window_set_ref lint. The legacy B11 / CUL-267 lints stay off for menu-shaped
criteria; the menu is the source of truth. Revisit (a) menu-aware lints only if a
real malformed menu-shaped rule is ever observed.
