# Group 3 notes: stops 10, 11, 12a, 12b, 13, 14 (2026-11-05)

Sources: the six stop files only. Inspector part (3) skipped. Operator quotes verbatim, spelling kept.

---

## Stop 10: Step 1b, strategy config authoring

**Element.** The AI step that turns the one-page hypothesis card into the base strategy config the engine will run, followed by code checks (manifest, graded/standardised rules, forecast size probe) before any backtest is paid for.

**Operator themes.**
- Content; sees it as matching the intended design.
  - "No remark, seems aligned with my vision." [stop 10]

**Inspector design themes (part 1).**
- 10-1.1: on the live loop 1b is "a copy with commentary". For a follow-up run the AI is told to keep the start config unchanged; run_102's output equals its input key for key. The 0.45 USD call added rationale text. The AI step only decides something on an operator brief or a new-block candidate.
- 10-1.2: the checks after 1b are "real, ordered and bounded" and are "the right checks" in the right place. The manifest contract (block or scaffolding, never both) is what makes an idea a reusable unit for the registry.
- 10-1.3: D-149 (standardise first, target 10, cap 20) means "one strategy class is being searched": every idea becomes a rank-of-the-last-500-bars signal at near-full exposure, and the profit bars judge that class's cost structure every time.
- 10-1.4: the engine grows only through a human. A missing component parks the run and appends to a request list with no status field and no reader that builds it; the campaign increasingly tests approximations. "The pipeline can discover a missing piece and cannot add one."
- 10-1.5: four documents each say they win; 1b reads about 1,350 lines of rules, layered by date, to copy a config.
- 10-1.6: the replay gate under `exact_config_1b` checks code against its own input; the deviation gate (off) is the opposite policy of nearest-build (on).

**Inspector legacy themes (part 2).**
- 10-2.1 to 2.3: inputs and sections of the retired routing (`findings_carryover.yaml`, replication guard, `significance_methodology`, twelve lines on a field not to write).
- 10-2.4: quant-fundamentals keeps two identities; the 15-trade floor, Gate A and worked examples belong in the decision log.
- 10-2.5: the replay gate and the deviation gate are weight under the current flags.
- 10-2.6: `component_requests.yaml` mixes three kinds of row with no closure field; same pattern as the test requests at stop 09.
- 10-2.8: the skill's "Context rule" is overridden by five further required inputs; stale text.

**Convergence.** Talk past each other: the operator sees alignment with the vision; the inspector accepts the design but finds the AI call mostly a copy, the rulebook layered, and the search space narrowed by construction.

**Feeling.** Simplify. Keep the checks and the manifest contract; cut the retired inputs, the duplicate gates and the layered notes so the step reads one rulebook.

---

## Stop 11: The design documents

**Element.** The five hand-written documents (design guide, component catalogue, indicator library, coin universe, data availability) that are the closed-book manual and parts list the AI steps design from.

**Operator themes.**
- Doubt that the AI steps should read so many documents; questions why idea generation (1a) sees the indicator library at all.
  - "This stop makes me wonder if the AI steps have access to too many docs. Eg: except i am wrong, i do not understand why 1a would havr access to indicator library... (Objective being to create ideas from a brief)" [stop 11]
- Does not understand what the indicator library is for next to the catalogue.
  - "I struggle to understand also usage of indicator library (especially comparing to component catalog)" [stop 11]

**Inspector design themes (part 1).**
- 11-1.1: the guide and the catalogue are "the real contract" and are kept honest by tests against the engine; "the right way to give a closed-book model a parts list".
- 11-1.2: the guide documents silent engine behaviour (unknown keys, misspelt params, unknown modes) that nothing checks; "the one class of silent error the design documents name and leave to the reader".
- 11-1.3: the parts list allows one strategy family: price-only, Kraken-only, graded-only, gated by one of five measures. The library offers more than the engine can build.
- 11-1.4: the indicator library "reaches nothing but a prompt": no live code reader, the "code groups tried ideas by indicator_id" sentence describes a mechanism that is not there, and the campaign's results never flow back into it.
- 11-1.5: the coin universe's defaults name Binance and the contaminated cache; the live path is not misled, a reader would be.
- 11-1.7: the guide is "a good engine manual with its decision history pasted in"; a model reads 659 lines to learn about 60 lines of rules.

**Inspector legacy themes (part 2).**
- 11-2.1: the indicator library: "either wire it ... or cut it to a list of ids with one line each."
- 11-2.2: the coin universe's escalation-era header and blocks.
- 11-2.3: data availability's maintenance notes and the superseded playbook still indexed.
- 11-2.4, 2.5: the guide's negative examples and stale sentences; nine of 28 catalogue rows carry a name the catalogue itself calls wrong.
- 11-2.6, 2.7: delete the grouping sentence or build it; three copies of the 0.2 band / forecast-over-10 number.

**Convergence.** Agree, strongly. The operator doubts the library; the inspector finds it has no live reader and feeds nothing back. The inspector adds the "one family" point the operator does not raise.

**Feeling.** Simplify. Keep the two tested contracts (guide, catalogue), trimmed to their rules; wire or cut the library; strip the escalation-era fields from the coin universe.

---

## Stop 12a: The strategy config: shape, components, transform ops, sizing

**Element.** The config file as the unit of research: regime detector, per-state components from a fixed list of 28, 18 transform ops with standardise first, one volatility-target sizing block.

**Operator themes.** (One remark for stop 12, recorded under 12a and 12b.)
- The config as the workflow's central asset.
  - "Aligned with my vision. Key asset of the workflow." [stop 12]
- Refused code should not be kept.
  - "However agree that i do not understand why we would persist any code that is now refused (eg on off)" [stop 12]
- Surprise that block-combiner code exists; the combined-block run is not yet designed, and its config must not be special in the backtest.
  - "I see "block combiner code" is mentioned. I thought it was not designed yet, hoping nothing has been created here as hardcoded / specific rule. First, we have not agreed on the design of combined block run (run combining several claim passed right). Second, such run should have a config based on claim associated block, but nothing should differenciate them in the backtest!" [stop 12]

**Inspector design themes (part 1).**
- 12a-1.1: "a good unit of research"; no-lookahead notes match the code; one param checker shared by op and validator. "This is well made."
- 12a-1.2: standardise is scale-only, no centring: a forecast of 10 means "typical for this component lately", and "a strategy's average absolute exposure is set by the standardise target, not by the idea."
- 12a-1.3: the sizing block makes the forecast's size nearly irrelevant to exposure; the band fires on the signal path.
- 12a-1.4: unknown op params are silent; the checker pattern exists but is applied to three ops of eighteen.
- 12a-1.5: the registry carries the campaign's decision history in prose; two copies (registry, guide) can drift.

**Inspector legacy themes (part 2).**
- 12a-2.1: four of eighteen ops (`threshold_filter`, `volume_filter`, `vol_adjusted`, `vol_target` as op) are refused or discouraged on the live path and kept for old configs.
- 12a-2.2, 2.3: pre-D-149 scale ops and stale comments; three functions compute what a component needs, one would do.
- 12a-2.4: the components' base class carries dead methods (CUL-281).
- 12a-2.5: the root CLAUDE.md and the itinerary give stale op counts.

**Convergence.** Agree on the config as the keeper and on cutting refused ops. The inspector adds a structural worry the operator does not voice: with standardise plus vol-target, every idea is tested as a near-constant-exposure rank signal.

**Feeling.** Keep. The unit is right and well built; remove the refused ops and move the prose history to the decision log.

---

## Stop 12b: The two engines, readiness, the validator

**Element.** The runtime that executes a config: regime engine labels the bar, strategy engine combines components into one forecast, readiness gates silence it until warm, and a validator (V1-V19) refuses broken configs.

**Operator themes.** Same remark as 12a. The block-combiner line bears directly here, since the combiner's code lives in the strategy engine.
- "I thought it was not designed yet, hoping nothing has been created here as hardcoded / specific rule." [stop 12]
- "such run should have a config based on claim associated block, but nothing should differenciate them in the backtest!" [stop 12]

**Inspector design themes (part 1).**
- 12b-1.1: the real warm-up is about twice what the author documents say (first forecast at bar ~455 for run_102, not 288). The backtester prefetches so a window loses nothing; the live path has no prefetch, so "a live bot on run_102's config would trade nothing for ~455 hourly bars (about 19 days)". "That is the gap between the backtest and the bot."
- 12b-1.3: errors are fail-open in two layers with different visibility; a forecast error gives forecast 0 and is not counted, so a missing `transforms` key makes "a zero-trade run with no error count and no pause". One validator line closes it.
- 12b-1.4: the regime engine is "small and honest", and with every live config ungated none of it runs.
- 12b-1.5: the validator "refuses exactly what the engine refuses"; what it does not check is what the guide warns about (unknown keys, misspelt params, wrong-type values).
- 12b-1.6: three config keys with three different owners, a source of the silently-ignored class.

**Inspector legacy themes (part 2).**
- 12b-2.1: constructor arguments for a regrid "NOT YET wired"; wire or drop.
- 12b-2.2, 2.3: the warm-up drift story told three times, one of them stale.
- 12b-2.4: score / score-product modes, vetoes and margins unreached by every ungated live config.
- 12b-2.5: the block combiner is "a third of the strategy engine" serving "a path that has not run", with one active block in the registry.
- 12b-2.6: a readiness comment wrong the other way.

**Convergence.** Diverge on fact, agree in direction. The operator hopes no combiner code exists; the inspector reports it exists and is a third of the engine, unrun. Both treat it as not-yet-agreed.

**Feeling.** Simplify. Keep the engines and validator; close the uncounted error layer; decide the combined-block design before keeping the combiner, and fix the warm-up text and the live prefetch.

---

## Stop 13: Forecast -> allocation -> fill -> fee

**Element.** The per-bar trading cycle: gap check, forecast to sized target, the 0.2 no-trade band, fill at close with slippage, fee per leg, one recorded line per bar.

**Operator themes.** (Sent labelled "Stop 14"; recorded here by the guide.)
- Surprise that the indicator fill for gaps is switched off.
  - "The indicator fill for gaps is off ?? " [stop 13]

**Inspector design themes (part 1).**
- 13-1.1: the band is two thresholds in two units and the signal one decides: a change of 2 forecast points on a standardised signal passes almost always. "Trades fire whenever the forecast drifts 2 points from the last fill ... turnover and the cost bar (stop 20) follow from this line, not from the idea." The band "no longer filters in money terms."
- 13-1.2: costs are "consistent and conservative, in a model": fee on every leg, sign flip as two trades, forced close per window. Left out consistently: funding, margin interest, liquidation, partial fills, latency. "The same cost rule for every idea, not the live venue's economics."
- 13-1.3: the whole per-bar body is one try/except; with 12b that makes three fail-open layers, and a bar lost here "looks like 'no trade'". "The third layer should count like the first."
- 13-1.4: gap tiers are keyed to the doubled warm-up: on run_102 a 4-bar hole "costs 12 days of entries". Right idea, wrong unit.
- 13-1.6: research inherits the bar interval (for 1h) and the band from the live bot's config.json; "a coupling between the live config and the research record."
- 13-1.7: order and portfolio code is Binance-era (hard-coded USDT) under a Kraken campaign; provenance right, labels wrong.

**Inspector legacy themes (part 2).**
- 13-2.1, 2.2, 2.5: decision history inside docstrings and ninety lines of constructor comments, repeated three times.
- 13-2.6: the portfolio risk gate is built only from a config block research never passes; weight on the research path.
- 13-2.7: funding model daily-only and off, "the one modelling gap that bears on every perp brief".
- 13-2.8: pass the interval always so research never reads the live bot's interval.

**Convergence.** Talk past each other. The operator asks one narrow question about gap fill; the inspector's weight is on the band deciding turnover and the gap tiers' unit. Both circle gap handling without meeting.

**Feeling.** Rethink. The fill and fee model is sound; the band's unit and the gap tiers' unit decide the cost structure of every run and should be chosen deliberately, not inherited.

---

## Stop 14: The data feed and the backtest's outputs

**Element.** The data feed with the sealed-holdout guard, and the backtester's seven files per window (manifest, bars, trades, metrics, states) that every later judge reads.

**Operator themes.** (Sent labelled "Stop15"; recorded here by the guide; last line arrived cut off.)
- Questions the "shared trade log" framing: trades.json should be a consumed output.
  - "Wait, trades.json should be read as an output by further post backtest steps, no ?? " [stop 14]
- Wants the backtest record complete to low granularity, per bar and per trade, including component sub-details.
  - "Here it is key to make sure that backtest output is generating complete details of the backtest : per bar (bar file), per trade (trade file)." [stop 14]
  - "Each of this file should have a line per element (resp. bar, trade) and associated details around it until low granularity (eg: forecast component sub details on the bar and trade lines, " [stop 14]

**Inspector design themes (part 1).**
- 14-1.1: the seal is enforced twice and the refusal cannot be swallowed; provenance (config hash, data hash, git SHA with dirty marker, costs, gap rule) is complete. "This is the part of the pipeline that lets a result be found again."
- 14-1.2: real numbers confirm the earlier readings: band passed on the signal path, stretch leg at the cap, 383 trades in 2,952 bars, cost drag 56%, net return 1.4%: "the cost structure stop 13 predicted."
- 14-1.3: "the record carries documented defects that no one fixes": A1 (balances columns are end-of-run values on every row), A7 HIGH (cost paid omits slippage while return is net of it), legacy route labels still written. A7 bears on the profit bar.
- 14-1.4: three definitions of Sharpe and two of drawdown in one record, "the kind of thing that fools a reader more than a model".
- 14-1.5: the shared `results/trades.json` is guarded only by the house rule "one test process at a time"; a per-run path exists and is not passed.
- 14-1.6: per-window outputs are "the right granularity for the judges"; the end-of-run assembly is one 345-line function where a defect like A1 lives unnoticed.

**Inspector legacy themes (part 2).**
- 14-2.1: about 13 of 50 bars.csv columns are wrong or unread; the dictionary marks them, the writer keeps them.
- 14-2.2: legacy prescreen/verdict labels in the core block.
- 14-2.3, 2.4: an Excel report per window with no reader; a forecast analyser constructed for nothing.
- 14-2.5, 2.6: debug prints and a loader that loads nothing.
- 14-2.8: trade-diagnostic fields known wrong (A5, A7) and still written.

**Convergence.** Agree on purpose, diverge on state. The operator sets the standard (complete, per bar, per trade, component sub-details); the inspector says the granularity meets it but the contents carry known defects and a shared file. On trades.json the voices pass each other: the per-window file is read; the shared one is an extra.

**Feeling.** Keep. The record is the right thing and already has the component debug columns the operator asks for; fix A1 and A7, drop the dead columns, pass the per-run trade path.

---

## Group synthesis

### Cross-stop themes

1. **One strategy family is being searched, by construction** (inspector-led; stops 10, 11, 12a, 13, 14). Standardise-first (D-149) and the vol-target sizing (D-176) make every forecast a rank of its own last 500 bars at near-constant exposure [10-1.3, 12a-1.2, 12a-1.3]; the catalogue allows price-only, Kraken-only, graded-only ideas [11-1.3]; the band fires on the signal path so turnover comes from the band's unit, not the idea [13-1.1]; run_102's window shows the result: cost drag 56%, net 1.4% [14-1.2]. The operator calls the config "Key asset of the workflow" [stop 12] and does not raise this; it is the inspector's largest point in the group and it bears straight on "finds a profitable strategy".

2. **The AI steps read too much, layered by date** (both; stops 10, 11, 12a). Operator: "the AI steps have access to too many docs" [stop 11]. Inspector: four notes each say they win and 1b reads ~1,350 lines to copy a config [10-1.5]; the guide is 659 lines for about 60 lines of rules [11-1.7]; the indicator library has no live reader [11-1.4]; the registry carries decision history in prose [12a-1.5].

3. **Refused, dead and unreached code is kept** (both; stops 12a, 12b, 13, 14). Operator: "i do not understand why we would persist any code that is now refused (eg on off)" [stop 12]. Inspector: four of eighteen ops [12a-2.1]; regime modes unreached by every ungated config [12b-2.4]; the risk gate, the funding model [13-2.6, 13-2.7]; 13 of 50 columns, an Excel report per window, legacy route labels [14-2.1 to 2.4].

4. **The block combiner exists before its design is agreed** (both; stops 12a, 12b). The operator was "hoping nothing has been created here as hardcoded / specific rule" [stop 12]; the inspector finds a third of the strategy engine, plus V13 and the `blocks` branches of V14-V18, serving a path that has not run, with one active block in the registry [12b-2.5].

5. **Silent and fail-open errors across the engine** (inspector-led; stops 11, 12a, 12b, 13, 14). Unknown keys and misspelt params run a different strategy with no error [11-1.2, 12a-1.4, 12b-1.5]; forecast errors and per-bar errors are not counted [12b-1.3, 13-1.3]; the record carries known defects A1 and A7 that no one fixes [14-1.3]. For a loop meant to run unattended and "without fooling itself", this is the group's main trust gap.

6. **The pipeline cannot grow its own engine** (inspector-led; stops 10, 11). A missing component parks the run and appends to a request list with no reader [10-1.4]; the library lists ideas the engine cannot build [11-1.3]; the campaign's results never flow back into the library [11-1.4]. Autonomy stops at the parts list.

7. **Backtest and bot are not the same machine** (inspector-led; stops 12b, 13). No live prefetch, so the bot would trade nothing for ~19 days [12b-1.1]; research inherits the band and the interval from the live bot's config.json [13-1.6]; Binance-era labels under a Kraken campaign [13-1.7]; costs are a model, not the venue's economics [13-1.2].

### Operator remarks on the whole workflow (verbatim, complete)

- [stop 12] "Aligned with my vision. Key asset of the workflow. 
However agree that i do not understand why we would persist any code that is now refused (eg on off)
I see "block combiner code" is mentioned. I thought it was not designed yet, hoping nothing has been created here as hardcoded / specific rule. First, we have not agreed on the design of combined block run (run combining several claim passed right). Second, such run should have a config based on claim associated block, but nothing should differenciate them in the backtest!"
- [stop 11] "This stop makes me wonder if the AI steps have access to too many docs. Eg: except i am wrong, i do not understand why 1a would havr access to indicator library... (Objective being to create ideas from a brief)"
- [stop 14] "Here it is key to make sure that backtest output is generating complete details of the backtest : per bar (bar file), per trade (trade file). 
Each of this file should have a line per element (resp. bar, trade) and associated details around it until low granularity (eg: forecast component sub details on the bar and trade lines, "

### What the operator says they want or would do differently

- Decide the combined-block run design themselves before any code: "we have not agreed on the design of combined block run" and "nothing should differenciate them in the backtest!" [stop 12].
- Not persist refused code: "i do not understand why we would persist any code that is now refused (eg on off)" [stop 12].
- Fewer documents for the AI steps, with each input justified by the step's objective: "i do not understand why 1a would havr access to indicator library... (Objective being to create ideas from a brief)" [stop 11].
- A complete backtest record, per bar and per trade, down to component sub-details [stop 14].
- Two open questions, not stances: "The indicator fill for gaps is off ?? " [stop 13] and "Wait, trades.json should be read as an output by further post backtest steps, no ?? " [stop 14].
