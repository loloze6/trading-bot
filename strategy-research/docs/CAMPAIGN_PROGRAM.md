# The Campaign Program — From Here to "Profitable Strategy Found" (v2, granular)
**Date: 2026-07-19 · For: Loloze (operator) · v2 changes: four concepts explained (campaign, validation, prescreen, cost-per-idea); near-miss scoreboard added; your concern-3/4/5 additions dispatched into numbered steps; every step now carries an objective and a deliverable.**

> This file describes the campaign: its concepts (Part 1), its phase plan
> (Part 2), and its standing guarantees (Part 4). It is not a roadmap —
> engineering work has its own home in `engineering/roadmap/EPICS.md`. The
> seven engineering items originally embedded in Part 2 (1.2, 1.3, 1.4, 3.1,
> 3.2, 3.4, 4.1) are implemented as epics: 1.2 → E-014, 1.3 → E-015,
> 1.4 → E-016, 3.1 → E-017, 3.2 → E-018, 4.1 → E-019; 3.4 is not an epic —
> it is a standing guarantee, carried in Part 4. Part 2 below carries only a
> one-line pointer to each.
> Part 3 below is superseded by engineering/DISPATCH_MODEL.md.

---

## Part 1 — What we built, in plain words (now including your four questions)

Two machines. The **lab bench** (`trading-bot/`) replays history: give it a strategy recipe and a date range, it produces the trades and the numbers. The **research factory** (`strategy-research/`) is the discipline around it, whose purpose is that we cannot fool ourselves.

**What is the "campaign"?** A *run* is one idea going through the factory once. The **campaign is the layer above all runs**: the memory and the scheduler. Concretely it is (a) the **queue** — the ordered list of registered ideas waiting their turn; (b) the **knowledge base** — every verdict ever recorded, with its reason, so a dead idea can never be quietly re-tested and every failure stays consultable; (c) the **campaign runner** — the program that picks the next ready idea, launches its run, records every transition in a log, and pauses everything when something needs a human. Without the campaign layer, each run would be an isolated experiment with amnesia; with it, run #60 knows everything runs #1–59 learned.

**Validation — what are the criteria?** It is an AI reviewer that reads the registered idea *before any test money is spent* and tries to break it on paper. Its checklist, in plain words: Is the idea **falsifiable** (does it predict something specific enough to be proven wrong)? Is there a **plausible mechanism** (a reason the inefficiency exists and would persist — who is on the losing side and why)? Is the test **honestly constructed** (no peeking at the future, no windows chosen after seeing results, data actually available)? Does it **collide with the graveyard** (same mechanism as something the knowledge base already killed)? (It may note a rough fee estimate, but since O-3 (2026-10-01) that estimate is information only: costs are judged only by the backtest, never by a guess before it.) Honest caveat: validation is a judgment stage, and it has misfired — it once rejected an idea while misreading which windows were being tested. That is why this week we forced it to always read the registration contract, and why its rejections get reviewed rather than blindly trusted.

**Prescreen (historical — removed in E-039 step 5, 2026-09-12; there is no prescreen stage today, and no idea is stopped on a cost estimate before its backtest) — how did it act, and could it wrongly refuse ideas?** It computes the signal's values over history and asks one cheap question: *does this signal, when it fires, correlate with what price does next?* It measures the correlation (called IC), whether it is statistically distinguishable from luck, how often the signal fires, and a first edge-vs-cost ratio. Strong enough → proceed to the full backtest; indistinguishable from zero → stop before spending. **Its honest limits — yes, it can wrongly refuse certain shapes of idea:** it tests *linear entry-forecast* correlation at a fixed horizon. A strategy whose value lives in (a) non-linear payoffs (rare big wins), (b) trade *management* (exits, sizing) rather than entry prediction, or (c) a specific regime diluted in the pooled average, can look like noise to prescreen while being real. Three protections exist: it measures only *active* bars (so conditional signals aren't diluted by silence); the registration contract outranks the rulebook — a brief can declare "this idea's value is in exits, judge prescreen accordingly"; and a cross-check compares prescreen vs backtest in both directions and raises a flag on disagreement (this exact flag caught our engine bug this week). Rule going forward: any registered idea whose edge is *not* an entry forecast must say so in its brief, so prescreen is applied to what the idea actually claims.

**"Cost per new idea dropped sharply this week" — meaning what?** Before this week: registering an idea required hand-editing the queue file (once needing special authorization), the validation stage judged ideas *without reading their registration contract* (three incidents — whole runs wasted on rejections argued from the wrong premises), and format mismatches burned a launch. This week shipped: a one-command **register** path (write the brief document, run one command, it's queued safely), the **contract-always-read** fix for validation and all later stages, and the format cures. Net effect: idea #N went from "a session with several manual interventions and known ways to waste a run" to "one document + one command, with those failure modes mechanically prevented." That is what makes *batches* of ideas (the whole Phase 3) affordable at all.

**Your challenge: "is mechanical pass/fail worth it — shouldn't we keep a top ranking to feed new ideas?"** Half yes, half no, and the half-no matters. **No** to replacing frozen pass/fail with a ranking for *promotion*: a ranking without frozen gates becomes "our best losers," and iterating toward the top of an in-sample leaderboard is the single most common way private traders overfit themselves into a fake edge. The bright line (frozen rule → one-shot holdout) is the part of this system that keeps us honest. **Yes** — emphatically — to your underlying point for *ideation*: "failed a criterion but ground for an idea" is real information we currently under-use. So we build both, firewalled: the **near-miss scoreboard** (new, step 3.2) — a ranked table of every tested idea (IC, cost ratio, which criteria it failed and by how much, root cause, era behavior) that the idea-generation stage reads as raw material, and that promotion is *forbidden* to read. The scoreboard inspires; only the gates decide. One asset already works this way: the trade-diagnostics layer that motivated the exit-filter candidates ("the pattern motivates, it never validates").

---

## Part 2 — The phase plan, granular

Phases gated by conditions. "Session" = one working session with agent dispatches. Your five concerns are dispatched into the steps where they live: C1→1 & Part 1; C2→the KPI + anti-corner rule; C3→3.1/3.4; C4→2.2–2.5 & 3.3; C5→1.1–1.4.

### Phase 0 — Close the current arc *(in flight, hours)*
- **0.1 — run_059 terminal verdict.** Objective: the campaign's first honest end-to-end verdict (the pending dispatch G5c: clear a stale cached artifact, resume, read the final numbers). Deliverable: verdict recorded in the knowledge base; KPI counts 1.
- **0.2 — Session close.** Objective: nothing learned this week can be lost. Deliverable: all commits landed (fixes, registration, run artifacts policy), the week's five defects ledgered with their fix-or-trigger, provenance caveats written on pre-fix daily-bar runs, this roadmap committed as `docs/ROADMAP.md`, session log + next-session file rewritten around Phase 1.
- **Gate:** repo clean, verdict counted, roadmap in repo.

### Phase 1 — Reality alignment: France, venue, fees *(1–2 sessions — your concern 5)*
- **1.1 — Venue survey.** Objective: know where you may legally trade as a French non-professional *today*, with sources. Deliverable: a one-page comparison (authorization status under current French/EU rules; spot vs perpetuals availability for retail; maker/taker fee schedules and tiers; API and historical-data quality) and a target venue decision (or shortlist of 2). Done fresh with citations — not from anyone's memory.
- **1.2 — Venue-parameterized cost model + calibration re-runs.** Graduated to `engineering/roadmap/E-014/EPIC.md`.
- **1.3 — Registration rule: venue declared.** Graduated to `engineering/roadmap/E-015/EPIC.md`.
- **1.4 — Fee-reduction autopsy field.** Graduated to `engineering/roadmap/E-016/EPIC.md`.
- **Gate:** venue decided in writing; cost model live; the three calibration runs reported; funding family's live status settled yes/no.

### Phase 2 — Data moat: the raw material for non-book ideas *(2–4 sessions, parallel tracks — your concern 4)*
- **2.1 — Breadth download (Track A).** Objective: escape the two-coin corner. Deliverable: price + funding history for the top ~20 liquid pairs, integrity-checked (gaps, timestamps — with the timezone lesson institutionalized as checks), documented provenance. Free and retroactive.
- **2.2 — First cross-sectional run.** Objective: the already-registered, never-run XS_momentum idea gets its verdict (its data blocker dies with 2.1; a 4-coin pilot on data already on disk can run even earlier). Deliverable: first breadth verdict in the KB.
- **2.3 — Whale-footprint dataset (Track B).** Objective: your "big players" thesis becomes measurable. Deliverable: from historical public *trade-by-trade* records (retro-downloadable; access to be verified given the France block — data download ≠ trading service), build per-coin series of: large-trade imbalance, cumulative volume delta, trade-size distribution shifts; define the first 2 registrable whale-flow indicators. Optional extension if archives allow: exchange in/outflow proxies.
  **Status (W24 correction): BUILT and UNEVALUATED, not "queued behind Track A."** `tools/recorder/whale_features.py`, `whale_persistence.py`, `whale_report.py`, `protocols/prereg_whale_footprint_v1.yaml`/`v2.yaml`, and `tools/whale_footprint_evaluation.py` all exist. No KB verdict exists for this family. This is PARKED PENDING DATA/evaluation, not queued, and must not be recorded as closed.
- **2.4 — Forward recorders (Track C).** Objective: start the clock on data that cannot be downloaded backwards (order-book depth; live liquidation events if wanted later). Deliverable: a small always-on recorder daemon + storage plan. Cheap now, priceless in 6 months.
  **Status (W24 correction): BUILT and RUN, not "queued."** The recorder was built and executed; it was stopped on a storage-budget gate, not left unstarted. See ledger item R3 / `engineering/roadmap/E-007/EPIC.md`.
- **2.5 — News/text scoping (Track D — your addition, adopted as exploratory).** Objective: decide honestly whether news ingestion is worth building. Deliverable: a scoping memo — which historical news/text sources exist with *point-in-time timestamps* (the hard requirement: we must only use what was knowable at that moment, else the backtest lies), free vs paid, and one candidate indicator design (event/sentiment shock vs subsequent drift). Build only if the memo clears the bar; note our one crude sentiment test so far (Fear&Greed index) is the weak cousin of this axis.
- **Gate:** ≥2 new data axes on disk with provenance + a first registrable indicator each; recorders running.

### Phase 3 — Hypothesis wave 2, with real autopsies *(ongoing once Phase 2 delivers — your concerns 3+4; this is where verdicts/week becomes the number that matters)*
- **3.1 — Autopsy standard v1, with the right metrics.** Graduated to `engineering/roadmap/E-017/EPIC.md`.
- **3.2 — Near-miss scoreboard.** Graduated to `engineering/roadmap/E-018/EPIC.md`.
- **3.3 — Registration waves.** Objective: throughput. Deliverable: batches of 3–5 registered ideas per wave from the new axes — cross-sectional momentum & carry across ~20 coins, the 2 whale-flow indicators, fee-reduced variants from 1.4, anything the scoreboard/autopsies motivate. Target once the machinery holds: ≥2 honest verdicts per week at declining cost per verdict. Old-corner single-asset TA stays parked unless an autopsy specifically licenses a variant.
- **3.4 — Diagnostics extensions on demand.** Not an epic — a standing guarantee, see Part 4.
- **Gate:** a pre-registered candidate passes its full frozen in-sample gates. (If an entire wave dies with clean autopsies: that is the loop *working* — the autopsies + scoreboard write the next wave.)

### Phase 4 — Combination and ML *(starts when Phases 2–3 give a handful of individually-informative features — your concern 4, "technological fit")*
- **4.1 — Feature matrix.** Graduated to `engineering/roadmap/E-019/EPIC.md`.
- **4.2 — ML ranker, registered like everything else.** Objective: extract what combination adds. Deliverable: a walk-forward-trained model that ranks/sizes coins, with its pass rule frozen *before* training ever touches the evaluation windows — same contract discipline as any idea. Outcome either way is recorded: "combination adds X" or "combination adds nothing here" (also a real answer).
- **Gate:** a combined candidate passes in-sample gates where singles didn't — or the recorded negative.

### Phase 5 — Promotion: from "passed" to "found"
- **5.1 — Sealed holdout, once.** The 2026 first-half data, evaluated a single time. No tuning after seeing it, ever.
- **5.2 — Paper trading on the Phase-1 venue.** 2–3 months, real fee schedule, real data feed, real order types.
- **5.3 — Small live capital** with hard risk limits, only after 5.2 is positive.
- **Definition of done — "profitable strategy found":** frozen in-sample gates passed → one-shot holdout passed → paper-traded profitably after the real venue's real costs for the defined period. Anything less, we say "not yet" out loud.

---

## Part 3 — How we work: roles, process, and which model for which job

**Extracted to `engineering/DISPATCH_MODEL.md`** (dispatch W25): the dispatch
loop, the roles and their models, cost discipline, context economy, and the
standard verification command. Read it there — it is a living document, kept
current independent of this document's own revision cadence.

## Part 4 — Standing guarantees (unchanged, plus one)

The KPI (honest verdicts/week, cost per verdict) is reported every session close. The **anti-corner rule**: every session ends with at least one hypothesis-level advance — a verdict, a registration, or a data-axis milestone — never process alone. Pipeline/autonomy work happens only where it raises verdicts-per-week. What the roadmap guarantees: searching where edges plausibly still live (big-player behavior, breadth, costs, combination), every failure leaving a tested reason, machinery that cannot lie, and live assumptions matching a venue you may legally use. What nobody can guarantee: that an edge exists. What I can promise: if one is findable with our data and our size, this process finds it — and if not, the knowledge base will show *why*, precisely enough that time and money stop going to ghosts.

**3.4 — Diagnostics extensions on demand.** The autopsy palette never blocks on a missing metric: small, ledgered additions to the diagnostics layer are added exactly when an autopsy needs a metric that doesn't exist yet (e.g. the regime-correctness measure) — never speculatively.
