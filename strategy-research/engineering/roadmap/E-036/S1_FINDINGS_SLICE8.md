# Slice 8 S1 — Exact-match repeat check (E-036) and outside ideas (E-035): characterize-and-stop

Read-only characterization at `94f3a1cc` (master, worktree HEAD). No code, config or
backtest changed; the holdout was not opened. Line numbers are re-grepped directly with
Git Bash `grep -n` against this checkout. No Linear access was available in this session
(checked via tool search — only GitHub tools are wired here), so where a fact lives only
in E-035's/E-036's Linear project and not in this repo, that is stated explicitly rather
than guessed at.

Inputs read: `delivery_plan_v26.md` slice 8 (L447-459), its rules (L17-48), the artifact
table rows for E-036/E-035 (L503-504), `roadmap/E-036/EPIC.md` and `roadmap/E-035/EPIC.md`
(both are Linear pointer stubs — see §0), the pre-pointer E-036/E-035 EPIC.md history (git
log), `E-046a/S1_FINDINGS_5B_II.md`'s REALIGNMENT section (L682-715), `E-059/S1_FINDINGS_6B.md`
(full, esp. §4.1, §5.1, Decision 3), `tools/anti_adjacency_gate.py`, `tools/build_exclusion_digest.py`,
`tools/decide_next.py`, `tools/campaign_memory.py`, `tools/record_schema.py`,
`config/feature_flag_register.yaml`, `workflow_artifacts/schemas/proposal.schema.json`, the
five reader `SKILL.md` files, and `workflow/run_phase1_research.py` at the cited lines.

---

## Guesses for the operator (read this first)

1. **Drop NEIGHBOUR from E-036, don't redefine it.** *(blocks the build)*
   8.1's text carries `NEIGHBOUR (same family/instrument/timeframe)` forward from the design
   that was already rejected once (see §1 below) — reopening S1's hash contract is the chance
   to remove it, not re-home it on `hypothesis_id`. Recommendation: `layer2_digest_check`
   returns binary `REPEAT`/`NOVEL` only, matching `decide_next.py`'s own already-accepted
   contract (no third tier). This is a real change to 8.1's stated text, so it needs your
   nod before S2 codes it.

2. **One hash key, one source of truth — not a second computed store.** *(blocks the build)*
   8.1 asks for a hash "computed at 5a per variant and stored in
   `campaign_record/exclusion_digest.yaml`." Recommendation instead: reuse the 4-field key
   `decide_next.py` already made binding on 2026-09-24 — `(forecast_hash, sorted(symbols),
   timeframe, protocol_ref)`, `forecast_hash` = the existing `_compute_forecast_hash`
   (sha256 of canonical-JSON config) — and look it up directly against
   `campaign_memory.yaml`, which already stores all four fields per variant. Do not compute
   a second, differently-serialized sha256 (`sha256(canonical_json(config)+instrument+
   timeframe+window_set_ref)`) into a separately-maintained file. If a fast on-disk index is
   still wanted for the 5a call site, make it a derived cache of `campaign_memory.yaml`
   (same key, rebuildable, never hand-diverging), not a rewrite of the old family-grain
   `build_exclusion_digest.py`. This changes 8.1's literal wording ("stored in
   `exclusion_digest.yaml` entries"), so it needs sign-off.

3. **`exclusion_digest_input` is already ON and reads the file this slice is about to
   reshape.** *(blocks the build — small, but live)*
   `orchestrator.exclusion_digest_input.enabled` is `on` today (`feature_flag_register.yaml`
   L26-35) and already unions `campaign_record/exclusion_digest.yaml`'s path into
   `hypothesis_generation`/`innovation_expansion`'s LLM prompt as an optional input, with a
   hard-coded "reason" string describing it as "family-scoped (family, instrument,
   timeframe) triples" (`run_phase1_research.py` L2498-2510). If 8.1 changes what that file
   contains (or retires it in favour of `campaign_memory.yaml`, per guess 2), this
   already-live prompt content goes stale or the path stops resolving. This needs an
   explicit decision in the same PR (update the reason string / repoint the optional_input),
   not a silent side effect — it's the one place in this slice where "off by default" doesn't
   cover you, because the consuming flag is already on.

4. **Layer 1 (KB reactivation) stays, but switching `variant_anti_adjacency_gate` on is
   what first gives it live REFUSE power.** *(blocks the build)*
   Both consuming flags (`anti_adjacency_retry`, `variant_anti_adjacency_gate`) are
   `off_incomplete` today, so `layer1_kb_check`'s REFUSE path has never fired in production.
   `S1_FINDINGS_6B.md` §5.1 already flagged that `layer1_kb_check` depends on
   `_lineage_routing_of_run`, which reads `pass_rule_evaluation.yaml.lineage_routing` — a
   retired-routing field per the hard alignment rule. Turning `variant_anti_adjacency_gate`
   on as part of 8.1 activates that dependency for the first time. Recommendation: keep
   Layer 1 in the call order (KB check first, exact-match digest second — unchanged from
   `anti_adjacency_gate.py`'s own module docstring, L11-42) but make it advisory-only
   (never REFUSE) until its `lineage_routing` dependency is separately fixed — the same
   treatment `decide_next.py` already gives it by not calling Layer 1 at all
   (`S1_FINDINGS_6B.md` §5.1, "Never call layer 1"). This is a real behavior choice at the
   moment the flag flips, not a default.

5. **E-035's actual filed S1 (and its "S2 (exists)" per the artifact table) live only in
   Linear.** *(blocks the build, scope-wise)*
   `roadmap/E-035/EPIC.md` was reduced to a Linear-pointer stub (`8a7545fb`); its last local
   content (`9a642a8c`, 2026-08-27) predates E-046a's realignment and E-059's decide_next
   build, both of which change assumptions E-035's original S1 sketch would have made (e.g.
   it assumed E-032's family-grain digest and pre-decide_next queue mechanics). This session
   had no Linear access (confirmed: `ToolSearch` for "linear issue project" surfaces only
   GitHub tools). Recommendation: scope slice 8.2's S2 to what's independently verifiable in
   this repo now — the feed-acquisition lane (§3 below) — and treat re-validating E-035's
   original external-sourcing design (literature/forum/model-knowledge dispatch itself)
   against current code as a prerequisite reopened-S1 task, not something this document can
   certify done from a stub file.

   **RESOLVED 2026-09-27 (orchestrator, Linear read after this document was written):**
   Linear project P-CUL-36 (E-035) holds no filed issues; its description carries the
   story list with **S1 and S2 both unchecked** ("S1 — Characterize and STOP: where the
   grant lives, what triggers exhaustion of internal sources, how a returned mechanism is
   shaped"; "S2 — the external-knowledge dispatch path, with source/date recording"). So
   "S1 as filed" in slice 8.2 means that story text, not a finished characterization, and
   the artifact table's "S2 (exists)" means the story line exists, not a build. The
   2026-09-20 note on the project confirms the manual path (operator writes a brief from
   outside reading) already works and that the feed-acquisition lane is added scope. The
   recommendation above stands: the automated external dispatch needs its own S1 before
   any build; the feed lane can be built now.

6. **`requires_feed` row shape into `data_requests.yaml`.** *(default is safe to build on)*
   No schema conflict exists (the file is an unclosed, flat `{requests: [...]}` list — see
   §3). Recommendation: reuse the existing idempotent appender
   (`_append_data_requests(..., dedupe=True)` → `_crr.append_requests`, already built for
   6c S2c's park/unpark case) with a new row shape
   `{run_id, stage: "specialist_reader", category, reason, requires_feed}`, written from a
   reader's proposal the same way `decide_next.py` already counts the file's rows
   (`decide_next.py` L731, L1522) — additive, no format change to existing rows.

---

## 1. E-036 — history: the design already shipped once, and was rejected

- **E-032** (closed) built the original two-layer gate: Layer 1 = KB reactivation match at
  mechanism grain (`layer1_kb_check`, `anti_adjacency_gate.py` L292); Layer 2 = a
  **family-grain** digest (`build_exclusion_digest.py::classify_family`, L112-160 — derived
  from the hypothesis card via `library_lookup.indicator_id` / `fear_and_greed` / a keyword
  table, never from `hypothesis_family`).
- **E-036 S2** (`16cd31be`/`9a738e49`, 2026-08-27) added `composition_fingerprint()`
  (`build_exclusion_digest.py` L227) — a flat `(regime, component_id, sorted(params),
  weight)` key, deliberately excluding `transforms` — and the three-outcome
  `layer2_digest_check()` (`anti_adjacency_gate.py` L406-501): `REPEAT` only on an identical
  fingerprint under the same family/instrument/timeframe; `NEIGHBOUR` on a family/instrument/
  timeframe match with a *different* fingerprint (`neighbours` list of colliding run ids
  attached); `NOVEL` otherwise. Measured working as designed (2.4-2.8x more distinct
  strategies recognized, `EPIC.md` log 2026-08-27) and merged.
- **Rejected outright, 2026-09-02** (`2ebf7535`, `feature_flag_register.yaml` L71-86,
  L88-98). Not "incomplete" — the operator rejected what it measures: *"the initial design
  of the solution is not convincing me... we need to see how to identify adjacency of two
  strategies with such strategy structure (regime with logic, sub-strategies allocated to
  regime, sub-strategies composed of weighted components)."* The register's own criterion
  text: a flat fingerprint has no representation for regime-detection logic and no
  principled distance threshold for "how different is different" — which is exactly what
  `NEIGHBOUR` was trying to encode. Both flags stayed `off_incomplete`, `blocked_on: E-036`,
  unpark trigger = "E-036 restarted with a reconsidered design, not merely re-reviewed."
- **REALIGNMENT, 2026-09-23** (`E-046a/S1_FINDINGS_5B_II.md` L682-715, PR #198 reverted in
  full same day, `57fcce4e`): *"An idea's identity is its `hypothesis_id`; a same idea on
  another coin is a variant of that idea, not a new family... Repeats are caught by the
  exact-match check (slice 8)."* This closes the family question from a second, independent
  direction: even setting aside the 2026-09-02 rejection, the routing/family machinery
  `NEIGHBOUR` and `classify_family` both lean on is itself retired.
- 8.1's exact-match-only design is consistent with both correction points — it does not
  attempt fuzzy structural adjacency at all, which is what was rejected. The one loose
  thread is that its stated `NEIGHBOUR (same family/instrument/timeframe)` tier is a leftover
  of the rejected design, not a new one — see guess 1.

### Today's exclusion digest, exactly

- **Writer:** `tools/build_exclusion_digest.py::build_digest()` (L447), run manually
  ("Regenerate on demand," `campaign_record/exclusion_digest.yaml`'s own `note:` field).
  Scans `runs/run_*/artifacts/hypothesis_card.yaml` fresh every time — never reads
  `campaign_state.yaml`'s stale `instruments_tried`/`timeframes_tried`. Currently 46/61 run
  dirs parse; keyed by `families.<family>.triples[].{instrument, timeframe, run_ids}`, plus
  a `failed_families_passthrough` block sourced from `campaign_state.failed_families`
  (written by the retired `record_pivot` — used only as a non-refusing "weak prior" flag,
  `anti_adjacency_gate.py` L446-463).
- **Readers:** `anti_adjacency_gate.py::layer2_digest_check()` (L406), called from two
  orchestrator sites: `_route_post_innovation_expansion` (`run_phase1_research.py` L5890,
  flag `anti_adjacency_retry`) and `_route_post_variant_selection` (L6293, flag
  `variant_anti_adjacency_gate`) — the latter is 8.1's real "5a per variant" call site: it
  already runs after variant patches produce each candidate's config and before
  `protocol_execution`, and already reads `backtest_spec.yaml`'s own `config` field as
  `candidate_config` (added 2026-08-27 specifically so this call site could supply a
  fingerprint). **This plumbing is fully built and wired today** — 8.1 only needs to replace
  `layer2_digest_check`'s internals and flip the flag, not build new call sites.
- **`anti_adjacency_retry` / `_route_post_innovation_expansion`:** fires *before*
  `backtest_specification` produces any config, so `candidate_config` is always `None` there
  — REPEAT is structurally unreachable at that call site (confirmed by the 2026-08-27
  regression-test disposition note: every affected test's real subject was the REFUSE-driven
  retry/escalation *policy*, not Layer 2 itself). 8.1's instruction to retire it ("it fired
  before a config existed") is fully supported: it never had a working REPEAT effect, so
  deleting it is a dead-code removal, not a behavior change.
- **`legacy: true`:** does **not exist today** in either `exclusion_digest.yaml` or
  `anti_adjacency_gate.py` (grep empty). The convention exists elsewhere —
  `campaign_memory.py` L492 writes `"legacy": False` on every entry it builds fresh from a
  run's artifacts — but nothing yet marks a pre-hash-scheme run as `legacy: true` in the
  digest/gate path. This is new work for 8.1, not a tightening of an existing marker.
- **Corpus replay, feasibility:** **yes, read-only, with direct precedent.** The 2026-08-27
  S2 build already did exactly this shape of measurement — `scan_run_triples()` over
  `runs/run_*/artifacts` with no backtest, no holdout — and published before/after counts
  (old `(family, instrument, timeframe)` key = 30 distinct / new fingerprint key = 73 across
  46 runs; 13→36 on the 39-run subset with both `hypothesis_card.yaml` and
  `candidate_strategy_config.json`; `EPIC.md` log, `3a838238`). Slice 8.1's replay is the
  same operation with the new key: recompute `(forecast_hash, symbols, timeframe,
  protocol_ref)` over every run's variant configs (`candidate_strategy_config.json` /
  `variants/*/strategy_config.json`), count collisions under the old family-grain key vs the
  new exact-match key, publish refuse/admit before/after. No market data or holdout touched.

## 2. The two repeat checks, mapped precisely

**`tools/decide_next.py` (E-059 S2a, built — 1635 lines, not a sketch).**
`S1_FINDINGS_6B.md` §4.1 (L308-316) and Decision 3 (2026-09-24, accepted, L589-591):
*"The exact-match repeat check (card K: config hash + symbols + timeframe + protocol)
becomes binding now, from campaign memory; the legacy digest stays informational."*
- **When it fires:** candidate-selection time — before a reader-proposed patch/new_block or
  a queued brief-sibling is even registered to the queue. It is the mechanism that decides
  *which one new candidate*, if any, gets written as the next `ready` entry.
- **Key:** `(forecast_hash, sorted(symbols), timeframe, protocol_ref)`. `forecast_hash` is
  the existing `_compute_forecast_hash()` (`run_phase1_research.py` L8439-8463: sha256 of
  `json.dumps(config, sort_keys=True)`) — the same function trial recording has used since
  E-025 (2026-08-16). `symbols`/`n_windows` come from `campaign_memory.py::_variants_block`
  (L240-311, fields at L288-294/304-309); `timeframe`/`protocol_ref` come from the memory
  entry itself (`campaign_memory.py` L457-472, L502-503) — `protocol_ref` is
  `protocol_result.yaml`'s own `protocol_file`, resolved relative to `protocol_root`.
- **Source of truth:** `campaign_memory.yaml`, written post-hoc by `regroup_record` once a
  variant has actually been backtested.
- **Coverage — this is the load-bearing gap.** `decide_next`'s own invariant (§3.1,
  `decide_next.py` L126-127 `_OPERATOR_ORIGINS = (None, "external")`, used at L426, L1382,
  L1466): an operator-registered `ready` entry, or any entry with `origin: external`, is
  always picked **first, with no novelty check at all** — "decide_next then picks nothing."
  So decide_next's binding check only ever runs for reader-proposal/brief-sibling
  candidates. A hand-typed duplicate brief, a re-registered `external` idea, or a
  `queued_card` entry is never checked by it.

**8.1's proposed mechanism (unbuilt).**
Meant to sit at 5a (`_route_post_variant_selection`, already wired — §1), gating **every**
variant regardless of how its run entered the queue: operator, brief, `queued_card`, or
reader-derived. This is the one property decide_next structurally cannot have (it's skipped
for exactly the paths that matter here), so it is not redundant with decide_next — it is the
universal backstop decide_next was never meant to be.

**Where they'd conflict if built as literally written:** two independently-computed hashes
of "the same thing." Decide_next's key is `sha256(canonical_json(config))` combined as a
4-tuple with `symbols`/`timeframe`/`protocol_ref`; 8.1's text proposes a single
`sha256(canonical_json(config) + instrument + timeframe + window_set_ref)` — a different
byte string, with `instrument` (singular) vs `symbols` (sorted list — multi-symbol variants
are real, `campaign_memory.py` L292/308), and `window_set_ref` vs `protocol_ref`.
`window_set_ref` is not a typo or an invented name — it's `pre_registration.yaml`'s own
pre-registered field (`K2`/`K3` design docs; `_lint_machine_constraints_protocol_selection`
hard-rejects a `window_set_ref`/`protocol_ref` mismatch at materialization time,
`test_k3_protocol_pinning.py::test_lint_q1_hard_rejects_window_set_ref_mismatch`) — so the
two are lint-guaranteed equal *when pre-registration exists*, but `campaign_memory.yaml`
only ever stores `protocol_ref` (derived from the actual executed `protocol_result.yaml`,
not the pre-registration promise), and that's the field decide_next already reads. Building
8.1 against `window_set_ref` would mean re-deriving a value memory doesn't carry, from a
file (`pre_registration.yaml`) that doesn't exist for every run shape (e.g. config-direct
authoring, §3.3 of `S1_FINDINGS_6B.md`).

**Resolution (guess 2): one key, one source.** Use decide_next's already-accepted 4-tuple
verbatim (`forecast_hash`, `symbols`, `timeframe`, `protocol_ref`), read from
`campaign_memory.yaml`. Extract the exact-match lookup decide_next already implements into
one small pure function both call sites import (e.g. `tools/novelty.py::exact_match(key,
memory) -> "NOVEL"|"REPEAT"`), so `decide_next.py` and the redesigned
`layer2_digest_check()` can never independently drift on what "the same idea" means. Retire
`composition_fingerprint`/`classify_family` as anything but legacy/informational context (if
kept at all, only inside the `exclusion_digest_input` prompt surfacing — see guess 3 — never
as a refusal signal).

**What's already done, what's still needed, what retires:**

| | |
|---|---|
| Already done | `_compute_forecast_hash` (the hash primitive); decide_next's binding exact-match gate for the reader/brief path (E-059 S2a); `campaign_memory.yaml`'s per-variant `forecast_hash`/`symbols`/`timeframe`/`protocol_ref` fields; the `legacy: False`-on-write convention (needs extending, not inventing); the 5a call site itself (`_route_post_variant_selection`, `variant_anti_adjacency_gate` flag, candidate-config wiring) |
| Still needed | Shared exact-match function importable by both call sites; new `layer2_digest_check` body reading `campaign_memory.yaml` (or a derived cache of it) instead of the family digest; binary REPEAT/NOVEL contract (guess 1); `legacy: true` handling for runs with no memory entry; flip `variant_anti_adjacency_gate` on; update the `exclusion_digest_input` prompt text (guess 3); Layer 1's advisory-only interim treatment (guess 4); the corpus replay itself |
| Retires | `anti_adjacency_retry` (flag + `_route_post_innovation_expansion` call — dead-REPEAT code, §1); `composition_fingerprint`/`classify_family` as a binding signal; the `NEIGHBOUR` outcome and `_describe_fingerprint_diff` (`anti_adjacency_gate.py` L372); a hand-computed, independently-shaped `exclusion_digest.yaml` (replaced by a read of, or a rebuildable cache of, `campaign_memory.yaml`) |

## 3. E-035 — what's locally verifiable vs. what lives only in Linear

`roadmap/E-035/EPIC.md`'s last real content (`9a642a8c`, 2026-08-27, before it was reduced
to a Linear pointer by `8a7545fb`) described: split out of E-032 (S3), goal = dispatch to an
external-knowledge agent (literature/forums/model knowledge) when internal sources are
exhausted, importing *mechanisms not fitted rules*, with source+date recorded (publication
bias control) and every generated idea producing a trial row. S1/S2 status per the delivery
plan's artifact table (L504) is "(exists)" — i.e., filed in Linear since. That content is
not retrievable here (§ guess 5).

**What is independently verifiable in this repo, and answers the dispatch's specific
questions:**

- **`register_hypothesis` + `origin: external` — already plumbed, ahead of E-035's own
  build.** `record_schema.py` L133: `_ORIGIN_VALUES = {"brief", "reader", "composition",
  "campaign_review", "external"}` — `external` is a first-class, already-valid value.
  `decide_next.py` L126-127 treats `origin` in `(None, "external")` identically to a
  hand-registered operator entry: always considered first, before any agent-ranked
  candidate, with **no scoring and no novelty gate** (§3.1 of `S1_FINDINGS_6B.md`). So "queue
  entry via `register_hypothesis` with `origin: external`, with criteria set at 1a as for
  every idea" is already mechanically true today for the queue side — an externally-sourced
  brief registered this way enters exactly like any operator `ready` entry and goes through
  1a like every idea (per the hard alignment rule: "the next run is chosen only by
  decide_next" / "idea status comes only from the grid" — nothing here contradicts that).
  What's missing is the thing that *produces* such a brief, not the queue plumbing to accept
  it.
- **`campaign_record/data_requests.yaml` as the feed lane's intake.** Writer:
  `_append_data_requests()` (`run_phase1_research.py` L3999-4016) — flat, append-only
  `{requests: [...]}`, each row stamped `{run_id, stage: "data_availability_gate", ...}`.
  Its only current caller is the per-variant data-availability gate's feasibility rejections
  (L1323-1339); no reader-proposal path writes to it today. Its `dedupe=True` branch
  (`_crr.append_requests(requests_path, rows, key=_crr.request_key)`, added for slice 6c
  S2c's park/unpark re-run case) is the "locked, idempotent appender" the dispatch refers to
  — it is real, already built, and directly reusable by a new writer with a different row
  shape (the file has no closed schema to fight). `decide_next.py` already reads the file's
  row count into the decision record as information (`decide_next.py` L731, L1522) — so
  routing a `requires_feed` proposal there is additive to a path that already tolerates
  arbitrary new rows.
- **`requires_feed` — does not exist anywhere.** Not in
  `workflow_artifacts/schemas/proposal.schema.json` (its `kind` enum is only
  `["patch", "new_block"]`, L16), not in any of the five reader `SKILL.md` files (grep
  empty). This is genuinely unbuilt, exactly as 8.2 implies — a new optional field on a
  proposal (likely orthogonal to `kind`, since a reader might flag "this idea needs a feed we
  don't have" regardless of whether it's proposing a patch or a new block) plus the reader
  SKILL.md wording to produce it, plus the router in `decide_next.py`'s feasibility gate
  (§4.2 of `S1_FINDINGS_6B.md` already treats `component_requests.yaml`/`data_requests.yaml`
  as "information; the binding check is re-resolving the candidate itself" — a
  `requires_feed` candidate should land the same way: `infeasible` until the feed exists,
  never silently dropped).
- **Run budget — "1 externally-sourced idea reaching a grid verdict" needs a real run and an
  `ANTHROPIC_API_KEY`; neither exists in this environment.** Everything else is provable with
  fixtures alone, following the exact precedent E-059 S2a/S2b already set (build + pure-function
  tests now; the real "2 consecutive runs" proof was a separate, later step). For 8.2: the
  schema change, the appender reuse, and `decide_next`'s already-built `origin: external`
  priority path are all testable today with synthetic proposals/queue fixtures and system
  Python, no API key, no backtest. Only the external-sourcing agent's own dispatch and the
  final grid-verdict run need the key and a live run.

## 4. Proposed S2 split

**S2a — E-036 core (no new call sites, redesign the existing one):**
1. `tools/novelty.py` (new, pure): the shared exact-match key/lookup, imported by both
   `decide_next.py` and the redesigned `layer2_digest_check`.
2. Redesign `layer2_digest_check()`: binary `REPEAT`/`NOVEL` (guess 1), reads
   `campaign_memory.yaml` (or a rebuildable cache of it) via `tools/novelty.py`, `legacy`
   handling for runs with no memory entry.
3. Retire `composition_fingerprint`/`classify_family` as a refusal signal; retire
   `anti_adjacency_retry` (flag + `_route_post_innovation_expansion` call, dead-REPEAT code).
4. Flip `variant_anti_adjacency_gate` on; update its `feature_flag_register.yaml` entry
   (state, criterion, unpark evidence).
5. Layer 1 advisory-only interim (guess 4) — one-line change, same treatment decide_next
   already gives it.
6. Update `exclusion_digest_input`'s prompt text/optional_input path (guess 3) in the same
   PR, since it's already live.
7. Docs: `USER_GUIDE.md`, `E-036/EPIC.md`'s Linear-mirrored summary, flag register.

**S2b — E-036 corpus replay:** read-only script over the 61 run dirs, publishing
refuse/admit counts under the old family-grain key vs the new exact-match key (same shape as
the 2026-08-27 measurement). No code dependency on S2a beyond the shared key function.

**S2c — E-035 feed lane (the locally-verifiable slice of 8.2):**
8. `proposal.schema.json`: add `requires_feed` (optional string/object), independent of
   `kind`.
9. Reader `SKILL.md` wording (all five) for when/how to emit it.
10. A router from a `requires_feed` proposal into `_append_data_requests(..., dedupe=True)`
    with the new row shape.
11. `decide_next.py`: mark a `requires_feed` candidate `infeasible` until resolved (mirrors
    the existing feasibility treatment of `component_requests.yaml`/`data_requests.yaml`,
    §4.2 of `S1_FINDINGS_6B.md`).

**Deferred, outside this S2 (per guess 5):** re-validating E-035's external-sourcing design
itself (the literature/forum/model-knowledge dispatch mechanism) against current code — its
last local characterization predates E-046a's realignment and E-059's decide_next build.
This needs its own read of the actual Linear-filed S1/S2 before a build dispatch, which this
session could not perform.

## 5. Flag design

- `orchestrator.variant_anti_adjacency_gate.enabled` — **existing** flag, reused as-is (no
  new flag). Redefine its `feature_flag_register.yaml` criterion once S2a ships; flip
  `off_incomplete` → `on` only after the corpus replay (S2b) is published, per rule 0.2's
  "before/after artifact diff" requirement for a declared-adjacent change.
- `anti_adjacency_retry` — **removed**, not flipped. It never had a working REPEAT effect
  (§1), so deleting the flag, its reader function, and its call site is bit-identity-safe by
  construction; its register entry is removed in the same PR with a note citing this
  document.
- E-035 feed lane — **no new flag needed for the schema/appender additions** (they're
  additive to files nothing yet gates on); if the external-sourcing dispatch itself (deferred
  per §4) needs one later, it follows the standard
  `orchestrator.<name>.enabled` pattern.

## 6. Tests (all runnable here: system Python, no API key, no backtest)

- **`tools/novelty.py`:** exact-match REPEAT/NOVEL on synthetic memory; a legacy run (no
  memory entry) never matches; multi-symbol `sorted(symbols)` equality; determinism.
- **`layer2_digest_check` (redesigned):** identical config/symbols/timeframe/protocol_ref →
  REPEAT; any single field different → NOVEL (no NEIGHBOUR path exists to test); a
  transform-only diff is no longer collapsed to REPEAT (this was the old design's own
  documented weakness, `anti_adjacency_gate.py` L377-380 — becomes a NOVEL case here, add a
  regression test asserting so).
- **Flag-off bit-identity:** `variant_anti_adjacency_gate` off ⇒ `_route_post_variant_selection`
  byte-identical (existing `test_flag_off_*` pattern extended); `anti_adjacency_retry`'s
  removal ⇒ existing byte-identity tests for that call site either retired with a note or
  repointed to prove the code path is gone.
- **`exclusion_digest_input`:** the optional_input's `reason` text matches the new schema
  (no stale "family-scoped triples" wording once the source changes).
- **Corpus replay:** a fixture asserting the replay script runs read-only (no writes under
  `runs/`), and a golden count on a small synthetic corpus.
- **`requires_feed`:** schema accepts/rejects; router writes the correct row shape via the
  existing dedupe appender (idempotent on re-run, per its own contract); `decide_next`
  marks the candidate `infeasible: requires_feed` until a matching resolved entry exists.
- **Register:** `test_feature_flag_register.py` updated for the `anti_adjacency_retry`
  removal and `variant_anti_adjacency_gate`'s new criterion text.
- **Docs gate:** `test_guide_covers_the_code.py`, `test_doc_anchors.py`.

---

## Decision (operator, 2026-09-27)

All five recommendations accepted ("Go"):

1. **No NEIGHBOUR.** `layer2_digest_check` returns binary `REPEAT`/`NOVEL` only; no family
   or similarity tier.
2. **One key, one source.** The exact-match key is decide_next's
   `(forecast_hash, sorted(symbols), timeframe, protocol_ref)`, read from
   `campaign_memory.yaml`, through one shared pure function imported by both
   `decide_next.py` and the 5a gate. No second hash formula, no hand-maintained digest.
   The 5a gate is the backstop for operator/`external`/`queued_card` entries that
   decide_next never checks.
3. **Idea-writing prompt input.** The live `exclusion_digest_input` surfacing is repointed
   to the same information from the campaign record (idea, coins, timeframe, grid status),
   with no family grouping; the prompt reason text is updated in the same PR. Declared
   as a live prompt-text change.
4. **Layer 1 (KB reactivation) is advisory only** — it warns, never refuses.
5. **Scope.** Build the exact-match check and the E-035 feed-acquisition lane now. The
   automated external-knowledge dispatch gets its own S1 later (Linear P-CUL-36 S1/S2 are
   unchecked stories); the manual path (operator brief from outside reading) already works.

Sequencing (orchestrator): the default switch-on of `variant_anti_adjacency_gate` happens
only after the read-only corpus replay (S2b) has published refuse/admit counts and they
have been reported to the operator — S2a ships the redesigned gate with the flag still
off. Guess 6 (`requires_feed` row shape via the existing dedupe appender) taken as the
default.
