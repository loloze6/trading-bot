# config/ — what each file is for

Lookup table for an operator who has forgotten what a file does. One entry per
tracked file in `strategy-research/config/` (11 files).

"PROD referrer" below means a non-test `.py`/`.sh`, a `config/*.yaml`, a
`workflow/*.yaml`, or the git hook. Every `file:line` cited was opened and read.

---

## Quick answers

### a) When is each file read?

| Read at | Files | What that means for you |
|---|---|---|
| **Campaign start** (orchestrator startup / queue selection) | `campaign_queue.yaml`, `campaign_baseline_runs.yaml`, `venue_tradability.yaml`, `detector_wishlist.yaml` | Edit before launching a campaign. `run_campaign.py` resolves these while choosing and materializing the next run. |
| **Per run** (once per run, at the stage that needs it) | `campaign_data_policy.yaml`, `campaign_config.yaml`, `available_feeds.yaml`, `indicator_library.yaml` | Read fresh each run. An edit lands on the next run, not the current one. |
| **Per stage / per call** (re-read at every call site, no caching) | `cost_model.yaml`, `regime_retune_winner.json` | `prescreen_signal.py:613` and `run_protocol.py:85` each call `_load_cost_model()` independently. An edit mid-campaign changes some stages and not others — avoid. |
| **Per commit** (git hook) | `holdout_gate_exemptions.txt` | Read by `holdout_date_gate.sh:57` on every `git commit`. |

One caching exception: `venue_tradability.yaml` is cached per resolved path inside
`run_campaign.py` (`_venue_tradability_cache`, `:187`), so a mid-process edit will
not be picked up.

### b) Who writes each file — you, or the tooling?

| Hand-edited by the operator | Written by tooling — **do not hand-edit** |
|---|---|
| `cost_model.yaml` | `detector_wishlist.yaml` — *the `trigger_condition` fields only*: `status`, `last_evaluated_at`, `last_evaluated_against`, `kb_state_hash`, `evaluation_note` are written **only** by `run_campaign.py::evaluate_and_persist_wishlist_predicate()` (`:707`). The rest of an entry is hand-authored. |
| `campaign_config.yaml` | `campaign_queue.yaml` — written by `run_campaign._save_queue` (`:74`, `:105-126`) via atomic temp-file replace, and schema-validated on every write. |
| `campaign_data_policy.yaml` | `regime_retune_winner.json` — output of `retune_regime_detector.py:72`. |
| `available_feeds.yaml` | |
| `indicator_library.yaml` | |
| `venue_tradability.yaml` | |
| `campaign_baseline_runs.yaml` — human-added only, after manually confirming provenance | |
| `holdout_gate_exemptions.txt` — see the warning below | |

⚠️ Two traps, both learned the hard way:

- **`detector_wishlist.yaml` has been corrupted by hand-editing before.** A
  `status: triggered` value was found in it that no evaluator run had ever
  produced (`:16-27`). Before trusting any persisted status, check that its
  `kb_state_hash` still matches a fresh sha256 of the knowledge base's current
  bytes — a stale hash means a stale status.
- **PyYAML does not preserve `#` comments.** Anything written back by a
  `yaml.safe_dump` round-trip silently deletes every comment in the file. That is
  exactly how this file's original header block was lost, and why it now lives as
  a real YAML field (`file_documentation`) instead of a comment.

### c) `holdout_gate_exemptions.txt` — read this before touching it

The registry is **path-keyed with pinned line counts**. Format is
`<repo-relative-path><TAB><max allowed holdout-date lines>` (`:3`).

Three consequences:

1. **Renaming or moving ANY registered file invalidates its entry.** The key is
   the literal repo-relative path. Move `strategy-research/tools/panel_backtester.py`
   and its exemption stops matching — the file blocks the next commit until you
   update the path here. The same applies to every one of the registered paths.
2. **The count is part of the exemption.** A listed file that gains an N+1'th
   holdout-date line is blocked again (`:9-11`). The exemption is pinned to
   *audited content*, not to a filename. This is deliberate: it means a file can't
   be registered once and then quietly filled with sealed data.
3. **Adding an entry to silence a gate block is forbidden.** If the gate blocks,
   the answer is to look at the lines it found. If they are market data, the file
   is quarantined or excluded — **never registered** (`:33-35`). Registering it
   converts a working seal into a decorative one. The correct workflow is:

   ```
   sh strategy-research/tools/holdout_date_gate.sh --report-residual
   ```

   then, for each new path, **read the matching lines** and confirm they are prose,
   plans, config or code before pasting path/count. The original audit
   (2026-07-26, dispatch W5) confirmed 0 data files in the residual across 7,770
   text files examined; two run directories that *did* carry holdout bars were
   quarantined, not exempted.

---

## available_feeds.yaml

**PURPOSE** — Enumerates which data feeds are wired into the engine today, and
therefore which `evidence_type` values a hypothesis may claim.
*In plain terms: what data we actually have. An idea that needs something not on
this list goes to a wishlist, not the run queue.*

**WHO READS IT (PROD, measured)**
- `workflow/stages.yaml [ARCHIVED 2026-08-24 -> E-033/artifacts/; never drove the pipeline]:14` — a `required_input` of the `hypothesis_generation` stage
- `config/cost_model.yaml:212` — cites it for why `order_book` cannot be calibrated

**HOW IT IS CONSUMED** — Stage-level input to hypothesis generation.

**KEY PARAMETERS**
- `available:` — currently OHLCV, Binance 8h funding rate, and daily Fear & Greed. Each entry warns about its own catch (funding is not open interest; F&G is daily-resolution only and must be aligned or forward-filled).
- `unavailable:` — `order_book`, `liquidation_data`, `cross_exchange`, on-chain. Anything here routes to `feed_wishlist` instead of the queue.
- Update this file when a new feed is wired into the engine (`:7`) — not before.

**STATUS** — live. Hand-edited.

---

## campaign_baseline_runs.yaml

**PURPOSE** — Frozen list of run directories that predate this campaign's
registration convention, or were manually resolved.
*In plain terms: old runs that nothing points at, which are known-OK rather than
lost. Stops the orphan checker crying wolf about them forever.*

**WHO READS IT (PROD, measured)**
- `workflow/run_campaign.py:80` — `BASELINE_PATH`; `:1173` reports any orphan *not* listed here as unexpected

**HOW IT IS CONSUMED** — Read at campaign start by `reconcile_orphans()`.

**KEY PARAMETERS**
- `grandfathered_runs:` — each entry is `id` + `reason`.
- The important property (`:5-8`): `reconcile_orphans()` **never auto-populates** this file. A newly discovered unlisted orphan is always reported, never silently grandfathered. A human adds an entry only after manually confirming provenance.

**STATUS** — live. Hand-edited, append-only in practice.

---

## campaign_config.yaml

**PURPOSE** — Campaign-wide statistical constants: block sizes, significance
thresholds, episode-bootstrap settings, regime-detector bands.
*In plain terms: the dials that decide how strict the maths is.*

**WHO READS IT (PROD, measured)**
- `tools/power_check.py:40` — `_DEFAULT_CONFIG`; `:44` loads `rho_bar` from it
- `workflow/run_phase1_research.py:621`, `:3289` — loads the measured symbol correlation
- `workflow/run_campaign.py:1096` — `orchestrator.token_budget_per_run_weighted_units`

**HOW IT IS CONSUMED** — Read per run by the orchestrator and by `power_check.py`.

**KEY PARAMETERS**
- `prescreen.block_size_1h: 24` — how many bars count as one independent observation at 1h (a day's worth). Drives the effective sample size.
- `prescreen.block_size_1d: 1` — a daily bar *is* already a day; nothing to divide out.
- `prescreen.significance_threshold: 0.10` — the p-value below which an IC counts as real.
- `episode_significance.*` — gap length, minimum episode count, resample count for the sparse-signal bootstrap.
- `regime_detector.activation_band_min/max: 0.10 / 0.40` — how often "trending" is allowed to fire before the grade is capped.

⚠️ `:7-12`: this file is **not yet load-bearing at runtime**. Code still reads its
own module-level constants (e.g. `_BLOCK_SIZE_1H = 24` in `prescreen_signal.py`).
`test_campaign_config_sync.py` enforces that the two stay identical — a divergence
is a hard regression failure. Editing a value here without editing the code
constant will fail the suite, not change behaviour.

**STATUS** — live. Hand-edited.

---

## campaign_data_policy.yaml

**PURPOSE** — Which date ranges may be searched over, and which are sealed.
*In plain terms: the single answer to "am I allowed to look at this data?" It is
the most consequential file in this directory.*

**WHO READS IT (PROD, measured)**
- `tools/prescreen_signal.py:625` — `_load_campaign_data_policy()`; `:1081` applies it
- `tools/check_data.py:36` — `_DEFAULT_POLICY`, the holdout-overlap check
- `tools/validate_regime_detector.py:426`; `tools/measure_bar_sigma.py:105,125` — refuses to read sealed candles
- `workflow/run_phase1_research.py:3894` — `_DATA_POLICY_PATH`; `:4076,4105` — refuses a second holdout evaluation
- `workflow/stages.yaml [ARCHIVED 2026-08-24 -> E-033/artifacts/; never drove the pipeline]:81,130,162` — required input of three stages
- `tools/holdout_date_gate.sh:5`, `tools/hooks/pre-commit:12` — the window the commit gate enforces

**HOW IT IS CONSUMED** — Read per run, and per commit via the gate.

**KEY PARAMETERS**
- `holdout_range` (`:18`) — a sealed six-month window, **frozen**. No stage, tool, prescreen or diagnostic may read candles inside it, except a holdout evaluation (`:8-9`). Read the literal dates from `:18`; they are deliberately not repeated here, because publishing them is exactly what `holdout_date_gate.sh` blocks.
- `burned_ranges` — already used in past walk-forward windows; still usable for comparative search, not for unbiased estimation.
- `walk_forward_extension` — the range you may search over now.
- `backward_extension` — the 2018–2023 backfill, with per-feed true start dates (funding did not exist before perpetuals launched).
- `eras` — era boundaries for episode-blocked significance; every prescreen over backfilled data must report per-era, not only pooled.
- `holdout_consumed_by` — hypothesis ids that have spent their **single** holdout evaluation. There is no second attempt.
- `holdout_contaminated_runs` — quarantined runs that crossed the boundary.

**STATUS** — live. Hand-edited, rarely, and never casually.

---

## campaign_queue.yaml

**PURPOSE** — The work queue: which hypotheses are pending, in progress, blocked or
done, with the reasoning behind each disposition.
*In plain terms: what the campaign is doing next, and why it isn't doing the others.*

**WHO READS IT (PROD, measured)**
- `workflow/run_campaign.py:74` — `QUEUE_PATH`; `:123` validates each entry against `record_schema.QUEUE_ENTRY_SCHEMA` on save; `:628,656` evaluate wishlist predicates against it; `:1118` counts registered run ids
- `config/cost_model.yaml` and `config/campaign_data_policy.yaml` reference queue entries by id

**HOW IT IS CONSUMED** — Read at campaign start to select the next entry;
rewritten by `_save_queue` via atomic temp-file replace (`:126`) — it is the
clearest concurrent-writer risk in the repo (`:105`).

**KEY PARAMETERS**
- Per entry: `id`, `brief_path`, `status`, `priority`, `source`, `relation`, `notes`.
- `status` — the selector is **exact equality** on `ready` / `in_progress`
  (`campaign_queue.yaml:38`). Any other token, including any `blocked_on_*`
  variant, is inert: it records a disposition without reopening anything. There is
  no suffix whitelist to satisfy.
- `notes` — carries the measured basis for the status. These are long on purpose; a status without a reason is how a blocker gets misattributed.
- E-059 S2a (decide-next, `orchestrator.decide_next.enabled`, off by default):
  status `queued` (a waiting agent candidate — inert to the selector, like any
  other non-`ready`/`in_progress` token), and the closed-schema fields `origin`
  (`brief|reader|composition|campaign_review|external`), `proposal_ref`,
  `decision_ref`, `card_ref`, `brief_status` (`open|exhausted`) and
  `parked_reason` (`tools/record_schema.py`). Agent entries written by
  decide-next carry `source: agent`, `origin: reader`, `priority: 999` and no
  `relation`.
- E-059 S2b (same flag): a brief's extra cards (`<entry>__h<n>`) and R2
  requests (`<owner>__more_<n>`) carry `source: agent`, `origin: brief`,
  `priority: 999`, no `relation` (cards also `card_ref`); the owner of a brief
  carries `brief_status`. `title` (closed-schema, TEXT) is written once, in
  code, as `[obsolete] <heading or id>` on legacy briefs only.

**STATUS** — live. **Tooling-written** — prefer changing it through the orchestrator.

---

## cost_model.yaml

**PURPOSE** — Single source of truth for all fee/spread/slippage constants; the
top-of-file HARD RULE forbids any fee constant being hardcoded elsewhere.
*In plain terms: this file answers "what does it cost us to get in and out of a
trade once?" Every gate that kills a strategy for being too expensive gets its
numbers from here, so changing a value here changes which strategies survive.*

**WHO READS IT (PROD, measured)**
- `tools/prescreen_signal.py:613` — `_load_cost_model()`, feeds `_round_trip_cost()` (`:644`) and the Layer 2 `_cost_check` (`:665-666`)
- `tools/run_protocol.py:85` — `_load_cost_model()`, consumed by `_cost_paid_bps()` (`:296`) and `_commission_rate_for_symbol()` (`:96`)
- `workflow/stages.yaml [ARCHIVED 2026-08-24 -> E-033/artifacts/; never drove the pipeline]:80` — declared `required_inputs` of the `signal_prescreen` stage
- `workflow/run_phase1_research.py:1369` — same requirement, emitted into the stage dispatch as `"../../config/cost_model.yaml"`
- `config/campaign_data_policy.yaml:130` — cites it to explain why no maker/spread bps figure is derivable from available feeds

**HOW IT IS CONSUMED** — Never on a command line; read at call time by both tools
via `Path(_SR)/"config"/"cost_model.yaml"`. No caching, so an edit takes effect on
the next stage run.

**KEY PARAMETERS**
- `safety_factor: 2.0` — margin of safety: a strategy must earn **twice** its trading cost to pass, not merely beat it.
- `fee_rate_bps` — what the exchange charges you per side, per symbol.
- `spread_estimate_bps` — what you lose crossing the bid-ask gap to get filled now.
- `slippage_estimate_bps` — how far the price moves against you while your order fills.
- `round_trip_cost_bps` — the bottom line: total cost of one in-and-out trade (`2×fee + spread + slippage`).
- `perp:` — the same cost picture for perpetual futures (5 bps/side, Kraken). Used **only** with `--cost-product=perp`. Excludes funding, so it under-prices any funding-carry strategy (`:147-157`).
- `execution_style.maker` — hypothetical "rest an order instead of crossing" costs. **No code reads it** (`:188`); reference only.
- `verdict_execution_style: taker` — every pass/fail decision must use the pessimistic (taker) costs. Maker numbers may illustrate, never decide (`:45-57`).

**STATUS** — live. Hand-edited.

---

## detector_wishlist.yaml

**PURPOSE** — Candidate regime-detector families noted for later, each with a
machine-checkable trigger condition.
*In plain terms: a wishlist, not a work queue. Nothing here gets built until its
trigger fires — and the trigger is evaluated by code, not by someone reading prose
and deciding it feels true.*

**WHO READS IT (PROD, measured)**
- `workflow/run_campaign.py:500`, `:549`, `:707` — `dw_path`; `:674-689` document the single-authority contract and the `kb_state_hash` it persists

**HOW IT IS CONSUMED** — Read at campaign start when evaluating wishlist predicates.

**KEY PARAMETERS**
- `trigger_condition.predicate` — structured, not prose: `source`, `all_of[]` with `field` / `op` / `value` (`:6-12`).
- Evaluation outcomes (`:13-16`): `true` → build it; `false` → rejected, campaign review must produce a non-wishlist question; `missing_field` → **pause**, the knowledge base doesn't yet record what the predicate needs.
- ⚠️ `status`, `last_evaluated_at`, `last_evaluated_against`, `kb_state_hash`, `evaluation_note` are written **only** by the evaluator. As of the note at `:24-27`, `adx_threshold` and `hidden_markov_model` still carry the original hand-authored, unverified status and must not be trusted until re-evaluated.

**STATUS** — live. Partly tooling-written — see the warning above and §b.

---

## holdout_gate_exemptions.txt

**PURPOSE** — Audited allow-list of files permitted to contain dates inside the
sealed holdout window, each pinned to a maximum line count.
*In plain terms: the list of files where a 2026-H1 date is known to be harmless
prose, not market data.*

**WHO READS IT (PROD, measured)**
- `tools/holdout_date_gate.sh:57` — `REGISTRY`. A missing or unreadable registry **fails the commit** (deny by default, `:17-21` of that script)

**HOW IT IS CONSUMED** — Read on every `git commit`, via the pre-commit hook.

**KEY PARAMETERS**
- Format: `<repo-relative-path><TAB><max holdout-date lines>` (`:3`). `#` comments and blank lines ignored.
- Path-keyed and count-pinned — see [§c](#c-holdout_gate_exemptionstxt--read-this-before-touching-it) above for the two failure modes this creates and the one thing you must never do with it.

**STATUS** — live. Hand-edited, **only after reading the lines you are exempting**.

---

## indicator_library.yaml

**PURPOSE** — Domain-knowledge seed describing each indicator's regime affinity,
typical lag, crowding risk and data requirements.
*In plain terms: prior knowledge about which tools work in which market conditions,
so hypothesis generation starts from something better than a guess.*

**WHO READS IT (PROD, measured)**
- `workflow/stages.yaml [ARCHIVED 2026-08-24 -> E-033/artifacts/; never drove the pipeline]:15` — a `required_input` of the `hypothesis_generation` stage

**HOW IT IS CONSUMED** — Stage-level input to hypothesis generation.

**KEY PARAMETERS**
- Per indicator: `category`, `known_regime_affinity` (favorable / unfavorable / neutral per regime), `typical_lag_bars`, `crowding_risk`, `data_requirements`, `edge_source_compatibility`.
- Schema: `workflow_artifacts/schemas/indicator_library.schema.json` (`:7`).
- `:3-5`: `campaign_empirical_results` entries are a **read-view over the knowledge
  base**, not a separately maintained store. Don't hand-write empirical results here.

**STATUS** — live. Hand-edited.

---

## regime_retune_winner.json

**PURPOSE** — The winning regime-detector configuration from the last parameter
grid search.
*In plain terms: the settings that scored best on stability — ER period 24, smooth
5, trending when ER ≥ 0.25.*

**WHO READS IT (PROD, measured)**
- `tools/retune_regime_detector.py:72` — `_WINNER_CONFIG_PATH`, the tool that **writes** it

**HOW IT IS CONSUMED** — Output artifact. No consumer found beyond its own producer.

**KEY PARAMETERS**
- `regime_detector.components[0].params` — `period: 24`, `smooth_period: 5`.
- `rules[0]` — trending when the efficiency ratio is `gte 0.25`.
- `default_regime: unknown`.

**STATUS** — Its producer (`retune_regime_detector.py`) is orphaned and slated for
deletion elsewhere. This file's own disposition was **not** in scope for this pass
and no action was taken on it.

---

## venue_tradability.yaml

**PURPOSE** — Single source of truth for which (venue, product) combinations this
operator can legally trade *now* — French non-professional retail.
*In plain terms: stops the campaign spending effort on a strategy you would not be
allowed to place.*

**WHO READS IT (PROD, measured)**
- `workflow/run_campaign.py:190-196` — `_load_venue_tradability()`, cached per path at `:187`; `:215` applies it; `:181` names it the single source of truth
- Consumed by `_materialize_run()` to auto-flag `research_only`

**HOW IT IS CONSUMED** — Read at campaign start, when a run is materialized.

**KEY PARAMETERS**
- `venues.<venue>.<product>.tradable` — `true` / `false` / `unconfirmed`, each with a `basis` citing the survey that established it.
- Current state: Kraken spot `true`, Kraken perp `true` (CySEC 342/17, gated by a MiFID II appropriateness test), Kraken margin **`unconfirmed`**.
- The default is safe: `unconfirmed` is treated as not tradable (`:37-38`), and any pair absent from this file — or a brief declaring no venue/product at all — is flagged `research_only`. "Unconfirmed" is not "yes".

**STATUS** — live. Hand-edited when venue research changes.
