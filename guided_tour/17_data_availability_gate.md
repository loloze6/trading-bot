# Stop 17: The data availability gate

## Speech (verbatim)

**Stop 17 of 29: The data availability gate.** Open on the side: `tools/data_availability_gate.py`, `config/venue_data_capability.yaml`, `config/available_feeds.yaml`, `docs/DATA_AVAILABILITY.md`, `run_phase1_research.py`, run_102's `variants/base/data_availability/data_availability_gate.yaml`, `campaign_record/data_requests.yaml`.

**In one sentence.**
The data gate checks, for each variant and each test window, that the price bars and any extra data the strategy needs really exist and are nearly complete, before any backtest is run on them.

**Why it exists.**
A backtest on missing data does not fail loudly: it trades on the holes, or does nothing, and the result looks like a finding.
So before spending a backtest, each window's data is counted. A variant whose data cannot be assembled is set aside with the reason, and the missing data becomes a request rather than a false result.

**What comes in, what goes out.**
- In: each validated variant's config and protocol (from step 5a, stop 16: its coin, bar size and windows); a capability table of what each venue can supply; the list of available extra feeds; the local data caches.
- Out: per variant, a gate record (validate, refine or decline, per window and per feed, with the reasons); variants marked "not tested" when their data falls short; rows in the campaign's data request list.
- Next: the backtests (stop 18) for the variants still validated.

**What happens here, step by step.**
1. For each validated variant, separately: a failure on one never stops the others.
2. First, a cheap capability check with no network: could this venue, coin, bar size and feed combination exist at all, with enough history for the warm-up? If not, decline at once.
3. Then the real check, window by window: count the bars actually present against the bars expected. None missing: validate. Up to 5% missing: refine (usable with care). More, or no data: decline. Extra feeds are measured in their own update rhythm (a daily feed under an hourly strategy is not "95% missing").
4. A variant that does not fully validate is marked "not tested", with the reason, and its missing data is written to the request list.
5. The run then counts the variants left. At least 3 are needed. Fewer: if what is missing is data that can be fetched (or a missing component), the run is parked (waits off the queue until restored with an unpark command); otherwise it pauses for a person. A variant set aside as a repeat (stop 16) is not counted as a shortfall.

Example: run_102's base variant: exchange Kraken, hourly bars, gap tolerance 5%, outcome `validate` on all 6 windows of fold B (six 4-month blocks across 2018-2021), no extra feed. All four variants stayed validated.

**What it costs and how long it takes.**
No AI call; one gate run per variant, reading local caches. Duration not recorded in the audit log.
196 lines in `campaign_record/data_requests.yaml` (all runs so far).

**What is switched off or not used here.**
- Nothing: this is the one switch whose default is on.
- Live trading data is out of scope: the gate checks historical backtest data only.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Module doc | `tools/data_availability_gate.py:1-60` | Outcomes, two layers, 5% tolerance, feed rules |
| Capability check | `tools/data_availability_gate.py:170-500` | Layer 1 table, structural precheck, warm-up check |
| Window counts | `tools/data_availability_gate.py:505-752` | Expected bars, missing fraction, missing runs, classify, price window |
| Extra feeds | `tools/data_availability_gate.py:754-851` | Feed window in its own cadence |
| One variant | `tools/data_availability_gate.py:861-995` | `evaluate_variant`, aggregate |
| Command line | `tools/data_availability_gate.py:997-1042` | Exit codes |
| Capability table | `config/venue_data_capability.yaml` (645 lines) | Aggregation (`:105`), venues (`:113`), non-exchange feeds (`:567`) |
| Feed list | `config/available_feeds.yaml` (50 lines) | Available (`:12`), unavailable (`:35`) |
| Doc | `docs/DATA_AVAILABILITY.md` (89 lines) | Caches, fallback rule, feeds, sweep |
| Per-variant loop | `run_phase1_research.py:1846-2004` | One gate call each; not_tested marking; index save (`:1989`); requests (`:1997-2004`) |
| Requests | `run_phase1_research.py:6581` | `_append_data_requests` |
| Route | `run_phase1_research.py:20329-20397` | Floor of 3 (`_variant_floor`, `:19549`); park (`:6605`) or pause |
| Examples | `runs/run_102/variants/base/data_availability/data_availability_gate.yaml`; `campaign_record/data_requests.yaml` | validate on 6 windows |

Remarks: send them as "stop 17: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

### (1) Design and mechanism

1.1 Sound core. Layer 1 (`tools/data_availability_gate.py:195-388`) is a pure table lookup; Layer 2 (`:655-751`) uses the engine's own loader (`DataManager.fetch_historical_data`, `:711-714`) and the engine's own inclusive-end rule (`_measure_end :505-517`), so "available" means what it means to the backtest. Missing bars are counted in one unit (leading, internal, trailing; `_missing_fraction :538-584`) with a 2-second noise floor (`:535`). Per-variant isolation in the loop is real (`RP:1878-1987`, every failure `continue`s). Good for the goal: no backtest spends on holes.

1.2 The three-tier outcome is two tiers in practice. `evaluate_variant` can return `refine`, but the loop sends every non-`validate` variant to `not_tested` (`RP:1948-1975`: `if outcome == "validate": pass / else: not_tested`), and a `refine` never parks either (`_gate_shortfall_fetchable RP:6466-6469` returns False unless outcome is `decline`; `_variant_park_kind RP:6553` lists "a gate refine" among the reasons that stay "what they are today", i.e. pause for a human). So "usable with care" (speech step 3) is nothing the pipeline does: a 0.1% gap and a 100% gap produce the same `not_tested`. The 5% tolerance only chooses the wording of the reason. The record shows the cost: `campaign_record/data_requests.yaml:35-134` has whole base and design variants of run_061/064/076 set aside for 0.2–4.9% missing bars; those rows are requests nobody can act on (the exchange wrote no candle in those hours).

1.3 CUL-374 (`:731-744`) is the real rescue: a within-tolerance window whose every missing stretch is <= `DEFAULT_GAP_POLICY["ignore_max_bars"]` (=3, `trading-bot/core/launcher.py:615`) is upgraded to `validate`. run_102 window 2021-01 passed this way (gate record `:48-60`, one 1-bar gap). Consistent with stop 13 note 1.4 (engine ignore tier). But a single 4-bar stretch still throws the whole window and therefore the variant out, while the engine itself would handle it in the "middle" tier (keep position, block new entry) and keep running. The gate is stricter than the engine it protects; no path narrows a variant to its good windows, although the module doc promises that (`:7-10`, `:32-34` "narrow around the bad part").

1.4 Warm-up is checked by calendar only. `layer1_warmup_check :449-480` counts whole bars between the coin's `earliest_ohlcv_utc` and the window start; Layer 2 measures `[test.start, test.end]` only (`:905-922`). A gap inside the 2 x required_bars prefetch span is never counted, and a coin with no `earliest_ohlcv_utc` entry is "not judged" (`:469-470`; Kraken does not decline on a missing entry, `:290-298`). So the "could this exist with enough history for the warm-up" claim (speech step 2) holds only for coins the start-date table lists (19-pair universe, `:229-231`). Cross-check with stop 06 note 1.5: decide-next's `_fold_data_reason` still ignores warm-up while this gate requires 2 x required_bars; the two readers of the same question disagree.

1.5 Train windows are not checked. Only `w["test"]` is read (`:907-908`, `:930`). Any protocol with a `train`/fit span, or any in-window data a component needs before `test.start`, is unmeasured. Not an issue on run_102 (test-only windows), but the gate's contract is narrower than "the data the strategy needs".

1.6 Aux feeds: the per-feed path is correct in principle (own cadence `:807`, `:835`) but `_VENUE_LESS_FEED_NAMES` is a hard-coded set of one (`:147`) and the venue-scoped branch's default cadence is a literal `28800` (`:835`), i.e. the funding feed's; a new feed registered in `FEED_REGISTRY` without an `interval_seconds` attribute would be measured in 8h units silently. `fear_greed` is read raw while the engine uses it one day late (`docs/DATA_AVAILABILITY.md:49-51`): the gate's coverage is a day ahead of what the backtest attaches, so a feed that ends exactly at the window end validates here and is stale for the last day in the engine.

1.7 Side effects. Layer 2 uses `localStorage=True` (`:662-676`) so it reads and may write the shared OHLCV caches; the writer is non-atomic (`:678-689`, documented truncation of a years-long cache on interrupt). The gate is therefore not a read-only check; it is a cache-building step with a known data-loss hazard that is only mitigated by "never interrupt it". For Kraken, old windows are archive-only (`:311-347`), so Layer 2 is in effect a cache-only check there, and a decline means "not in our cache", not "not obtainable" (Layer 1 says the archive could cover it). The request row cannot tell the two apart.

1.8 The floor and the park. `_variant_floor RP:19551-19561`: repeats and D-042 coverage skips are not shortfalls; otherwise 3 needed. A base variant excluded only by warm-up writes no request (`RP:1976-1983`) but is still not_tested; with a 3-variant run that alone drops the run below the floor and pauses (not parks) because the shortfall is unfetchable. Reasonable, but it means a late-listed base coin ends in `paused_for_human` with nothing in the request file that explains why.

1.9 Readers of the request file: `decide_next.py:1147,2563` only counts rows (`data_requests_count`), `campaign_review_retired.py` dedupes on unpark. No reader closes a row or checks whether a later run already fetched the data. Same shape as stop 16 note 1.4 (component_requests): append-only, no status, no consumer. 196 lines for 15 rows, 11 of them `refine` rows the pipeline cannot act on.

1.10 Verdict on the goal: the gate stops false findings (good) at the price of stopping real ones: any sub-5% gap longer than 3 bars silently removes a variant from the count, with no narrowing and no per-window re-run. For an autonomous loop the outcome `refine` should either drop the window (the thing the module doc promises) or map to the engine's own gap tiers; as built it is `decline` with a kinder reason.

### (2) Legacy or simplifiable

2.1 Dead tier: `refine` as an outcome (`classify_missing_fraction :622-627`, aggregation `:983-988`) has no consumer that treats it differently from `decline` on the live loop (`RP:1951-1975`, `RP:6466`, `RP:6553`). Either implement narrowing or collapse to two outcomes and delete the 5% constant (`:106`); the tolerance's only remaining effect is the reason string.

2.2 Flag-off single-gate branch (`RP:20399+`, "Path C" in `campaign_config.yaml:484-487`) and the CLI exit-code convention (`:1038`, 3 = refine) exist for the pre-variant-loop pipeline; with `variant_loop` on they are unreachable from `run_loop`. Checked: `RP:20329` is the only route under `_variant_loop_enabled()`; not checked: whether any test still pins the flag-off branch.

2.3 `_read_ambient_fetch_interval_seconds :633-652` reads `trading-bot/config.json` for the CUL-250 opt-in while the protocol is the source of truth for everything else (`:26-31`). Stop 13 note 1.6 found the engine inherits the 1h interval from config.json via `run_protocol.py:2549-2550`; here a second ambient read of the same file decides which cadence to measure in. Both should come from the protocol.

2.4 `config/available_feeds.yaml` (50 lines) is a stale duplicate of `FEED_REGISTRY`: `venue_data_capability.yaml:613-620` already records it as out of step (no whale feeds), and `data_availability_gate.py` never reads it (`:92-96` imports the registry directly). Who reads it: only the step-2 skill (stop 15), by paste. Candidate for deletion or auto-generation (its own header `:1` says "auto-derivable").

2.5 `venue_data_capability.yaml` mixes a durable venue audit with an "our cache" fact: `earliest_ohlcv_utc` for Kraken is populated from local cache first rows (`:229-231`, `tools/refresh_coin_start_dates.py`), contradicting the file's own header (`:40-47` "NOT a record of what this codebase has fetched"). The per-coin warm-up rule (1.4) therefore depends on a refresh script being re-run after any cache change. Not checked: when it was last run.

2.6 `docs/DATA_AVAILABILITY.md` §4 checklist and §6 are playbook residue unrelated to the gate (§6 is a Linear status correction). §1-3 are the live content; the file is read by step 1a by paste (stop 07), not by this stage.

2.7 `_missing_fraction` and `_missing_runs` (`:538-612`) are the same scan written twice; one function returning runs, with the fraction as their sum, would remove the duplication and the risk of the two drifting.

### (3) Disagreements between speech and element

3.1 "Up to 5% missing: refine (usable with care)" (step 3). The pipeline never uses a refine variant: `RP:1948-1975` marks it `not_tested` exactly like a decline, and `RP:6466`/`6553` exclude refine from parking. Refine is a label, not a tier.

3.2 "Could this venue, coin, bar size and feed combination exist at all, with enough history for the warm-up? If not, decline at once" (step 2). The warm-up half is only applied when the coin has an `earliest_ohlcv_utc` entry (`:469-470`), and Layer 1 does not check feeds at all (`evaluate_variant :924-933` sends feeds straight to Layer 2; the Layer-1 feed sections of the YAML, `:567+`, are not consulted by code; checked by grep for `non_exchange_feeds` in the module: no hit).

3.3 "Its missing data is written to the request list" (step 4). True except for the base variant excluded only by warm-up (`RP:1976-1983`, no row). And a request row for a `refine` names missing bars the exchange never produced; nothing in the row says whether it is fetchable (`_gate_shortfall_fetchable` is computed at route time, not stored).

3.4 "Fewer: if what is missing is data that can be fetched (or a missing component), the run is parked ... otherwise it pauses" (step 5). Correct, with the addition that a `refine` shortfall always pauses (never parks), and the "missing component" case at this stage comes from 5a's V12 report, not from the gate (`RP:6564-6565`).

3.5 "Nothing: this is the one switch whose default is on." The stage's default is on (`campaign_config.yaml:463-464`), but the gate's behaviour on the live path is itself shaped by two other switches: `variant_loop` (selects the per-variant branch, `RP:1846`, `RP:20329`) and `verdict_routing_retired` (park vs pause, `RP:20364`; dedupe, `RP:2000`). Flag-off, the gate is a single run-level check with a different route.

3.6 "Duration not recorded in the audit log." Not checked against the audit log; the gate record carries `checked_at` only (`:939`).

3.7 "Reading map: Capability check `:170-500` ... warm-up check." Correct. The reading map omits `_gate_excluded_only_by_warmup RP:6495-6516`, `_gate_shortfall_fetchable RP:6459-6492` and `_variant_park_kind RP:6545-6578`, which are where the gate's outcomes actually become routing decisions.

3.8 run_102 example is accurate: Kraken, 1h, tolerance 0.05, six windows `validate`, one via the CUL-374 small-gap rule (gate record `:48-60`), `aux_feeds: []`. The record's `protocol_path` is the per-variant file (`:72`), consistent with stop 16 note on per-variant protocols.
