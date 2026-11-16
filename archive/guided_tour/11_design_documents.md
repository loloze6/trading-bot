# Stop 11: The design documents steps 1b and 2 read

## Speech (verbatim)

**Stop 11 of 29: The design documents.** Open on the side: `docs/STRATEGY_DESIGN_GUIDE.md`, `docs/COMPONENT_CATALOG.md`, `config/indicator_library.yaml`, `config/coin_universe.yaml`, `docs/DATA_AVAILABILITY.md`.

**In one sentence.**
These five documents are the manual and the parts list the AI steps design strategies from: how a config becomes a trade, which components exist and what each outputs, what indicators are known for, which coins may be tried, and which data exists.

**Why it exists.**
The AI steps work closed book: they see only what the prompt gives them. Without an exact manual they would invent component names, misjudge what a number means, or design for data that does not exist.
These documents are the one shared source of truth for steps 1a, 1b and 2. Two of them are also read by code, so the rules the AI is told and the rules code enforces are the same text.

**What comes in, what goes out.**
- In: written and maintained by hand; the catalogue's component table is checked against the engine.
- Out: nothing is produced. They are read.
- Read by: step 1a (indicator library), step 1b (design guide, catalogue, data availability), step 2 (design guide, catalogue, coin universe, data availability), and code (catalogue, coin universe, indicator library).

**What happens here, step by step.**
1. **The design guide** (658 lines) explains, in order: how a config becomes a trade on each bar (the window of past bars, the regime label, each component's value, the forecast as their weighted average clipped to ±20, the target position as forecast ÷ 10, the trade toward it at the bar's close, small changes below 0.2 refused); the graded-forecast rule (position size must follow signal strength, decision D-051, a row of the decision log); the config's shape; the regime detector (the part that labels market states) and its modes; each regime's components; every transform op; how to compose a signal; what the config cannot express; the block manifest (which part of a config is the idea); worked examples; and the validator's rules. The engine side of each rule is stop 12.
2. **The component catalogue** (182 lines) has one row per component: its parameters, its exact output, range and sign, kind (graded or on/off), units, warm-up, data needs. Code reads its "kind" column to refuse an on/off component as a forecast source.
3. **The indicator library** (320 lines) lists 15 known indicators: category, which market states they suit, how crowded they are, what data they need. Step 1a names the entry its idea builds on; code groups tried ideas by that name.
4. **The coin universe** (228 lines) lists 22 coins in five categories (store of value, smart contract platforms, DeFi, payment, memecoin), with which have data cached. Step 2 reads it to pick a coin of another category for an asset variant; code checks that choice.
5. **Data availability** (89 lines) says which bar sizes and feeds can be cached, how a coarser bar is built from a finer cache, the registered extra feeds, a bar-count check to run on a new bar size, and that no data is not a finding.

Example: run_102's card names `moving_average_crossover` from the indicator library; its step 2 picked LTC (another category) and XRP (payment) for its two asset variants.

**What it costs and how long it takes.**
No cost by themselves; they are prompt text. Together 1,477 lines (`wc -l` of the five files).

**What is switched off or not used here.**
- The coin universe's header still says "for instrument escalation" and names Binance as default exchange; the escalation path that read it is not reached today, and research runs are Kraken only (the brief's scope).
- The indicator library is described in its header as a view over the knowledge base, but it is a separate hand-written file.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| How a config becomes a trade | `STRATEGY_DESIGN_GUIDE.md:7-33` | Window, regime, components, allocation = forecast / 10, rebalance band |
| Design principle | `STRATEGY_DESIGN_GUIDE.md:34-73` | Graded only (D-051), standardised forecast |
| Config shape | `STRATEGY_DESIGN_GUIDE.md:74-103` | Keys |
| Regime detector | `STRATEGY_DESIGN_GUIDE.md:104-221` | Veto, rules, score, score-product, ungated, limits |
| Forecast per regime | `STRATEGY_DESIGN_GUIDE.md:222-266` | Component spec, engine, block combiner |
| Transform ops | `STRATEGY_DESIGN_GUIDE.md:267-368` | Every op |
| Composing a signal | `STRATEGY_DESIGN_GUIDE.md:369-504` | Combinations before a gap |
| Cannot express | `STRATEGY_DESIGN_GUIDE.md:505-532` | Exits, position state, orders, symbols |
| Manifest contract | `STRATEGY_DESIGN_GUIDE.md:533-566` | Block vs scaffolding |
| Worked examples | `STRATEGY_DESIGN_GUIDE.md:567-623` | Mean reversion, normalised trend |
| Checklist and validator | `STRATEGY_DESIGN_GUIDE.md:624-658` | Rules code checks |
| Catalogue | `COMPONENT_CATALOG.md:1-182` | How to read (`:9`), kind legend (`:29`), naming (`:41`), rows (`:61-118`), variant patterns (`:119`), feeds (`:144`), other names (`:171`) |
| Catalogue readers | `tools/forecast_rules.py:48`; `tools/catalogue_section.py`; `trading-bot/tools/validate_config.py` | Kind column; sections for prompts; validator |
| Indicator library | `config/indicator_library.yaml` (15 entries) | Vocab header `:1-18` |
| Library readers | `templates/handoffs/research_brief_to_hypothesis.yaml:9-10`; `tools/campaign_memory.py`; `tools/build_exclusion_digest.py` | 1a input; tried-ideas grouping |
| Coin universe | `config/coin_universe.yaml` (22 coins, 5 categories, `:11-97`; sequences `:204`, `:222`) | Asset variants |
| Coin universe readers | `run_phase1_research.py:3169`, `:3202`; `tools/variant_coin.py`; escalation `:11693-11925` | Step 2 input; coin check; old escalation |
| Data availability | `docs/DATA_AVAILABILITY.md` (89 lines, sections `:12`, `:20`, `:46`, `:60`, `:74`, `:82`) | Caches, fallback, feeds, bar-count sweep |
| Who injects them | `run_phase1_research.py:9072-9100` (step 2), `templates/handoffs/hypothesis_to_strategy_config_authoring.yaml` (1b), `:3181-3190` (data availability) | Inputs |

Remarks: send them as "stop 11: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop11
This stop makes me wonder if the AI steps have access to too many docs. Eg: except i am wrong, i do not understand why 1a would havr access to indicator library... (Objective being to create ideas from a brief)

I struggle to understand also usage of indicator library (especially comparing to component catalog)

## Inspector notes

### (1) Design and mechanism

1. Two of the five documents are the real contract, and they are kept honest by tests: the catalogue's component rows are re-derived against `strategy_components.py` (class set, row count, kind, warmup, every param default; `tests/test_design_guide_in_sync.py:8-17`), its Kind column is what code refuses on (`forecast_rules.py:86-100`), the guide's op tables are parsed for the analyst's prompt (`catalogue_section.py:8-17`), and the guide's JSON examples run through the validator (`test_design_guide_examples.py`, by name). 28 classes (26 `*Component` plus `EMADiff` and `BuyAndHoldStrategy`, `strategy_components.py`) and 18 ops (`registry.py:314-350`) match the two texts (`COMPONENT_CATALOG.md:6`, `STRATEGY_DESIGN_GUIDE.md:269`, catalogue `:177`). This is the right way to give a closed-book model a parts list: the prose cannot drift from the code without a test failing.
2. The guide documents engine behaviour it cannot fix, and the model is the only guard. Unknown keys and misspelt params are "silently ignored ... the default is used and nothing warns" (`:98-102`, catalogue `:11-12`); an unknown detector mode "silently runs score mode", an unknown rule op "silently evaluates to false" (`:215-218`); V12 checks that a class imports, "not that `params` are right" (`:652`). So a typo in a Sonnet-written config is a different strategy with no error anywhere, and the replay/size/manifest checks (stop 10) do not see it: the manifest resolves pointers, not spellings, and the size probe only measures magnitude. For a loop meant to run unattended this is the one class of silent error the design documents name and leave to the reader.
3. What the parts list allows is one strategy family. The catalogue's graded rows are price-derived trend, distance-from-average, range position, RSI, MACD level and volatility (`:83-105`); the feed-based graded rows need `funding_rate`/`fear_greed` (`:112`, `:114`), whose data policy range ends before the research folds' hourly Kraken data (stop 06, by key names only), and the whale row needs reserved feeds (`:115`, `:160-163`). The regime measures are five (`:73-77`). With D-149's standardise-first rule and D-176's sizing (stop 10 note 1.3), every idea the campaign can build is a weighted mean of standardised price indicators, optionally gated by one of five measures. The indicator library lists 15 ideas (`indicator_library.yaml:26-303`), of which `order_book_imbalance`, `open_interest_divergence` and `on_balance_volume` need data or a component the catalogue has not; the library offers more than the engine can build. The guide says what to do (approximate, declare a deviation, `:527-531`); the consequence for the goal is that the search space is price-only, Kraken-only, graded-only, by construction.
4. The indicator library reaches nothing but a prompt. `library_lookup.indicator_id` has no reader in `run_phase1_research.py` or `campaign_memory.py` (grep: none); its one code reader is `build_exclusion_digest.py:152-154`, which the campaign does not run (itinerary stop 25). The 1a skill's sentence "Code groups tried ideas by `indicator_id`" (`hypothesis-design/SKILL.md:76`) and the library's header "an indicator-indexed read-view over [the KB]" (`:3-5`) describe a mechanism that is not there: every entry's `campaign_empirical_results` is `[]` (`:37`, `:55`, ...), and the tried-ideas view groups by nothing (stop 07 note 1.6). So the library is 320 lines of textbook affinity text the model reads twice (1a, step 2) and writes one id from; the campaign's own results never flow back into it.
5. The coin universe's defaults point at the wrong venue. `default_exchange: binance` (`:7`); BTCUSDT and ETHUSDT carry `data_cached: true` with no `exchange`/`cache_key` (`:16-24`), so by the file's own rule (`refresh_coin_start_dates.py:126`) they name the Binance cache, which the data policy lists as contaminated by the holdout (policy key `binance_cache_holdout_contaminated`, stop 06). On the live path the venue comes from the brief through `venue_resolver` (stop 18) and the Kraken rows carry explicit cache keys (`:34-35`, ...), so the backtest is not misled; a reader of this file would be. The `escalation_order`/`timeframe_escalation` blocks (`:201-229`) belong to the retired escalation route (`RP:11693-11925`); the `15m` suggestion (`:225`) names a bar size the brief's scope forbids (stop 01).
6. `DATA_AVAILABILITY.md` reaches 1b only as an optional input (template `:22-23`), is a `refine_only`/optional input of two unreached stages (`RP:3181`, `:3188`), and is not given to step 2 at all (`_CLOSED_BOOK_STAGE_INPUTS["innovation_expansion"]` holds the coin universe only, `RP:3168-3172`; the step-2 template names no doc). Its content is three corrections of an older playbook and a checklist (`:3-8`, `:20-25`, `:82-89`): "read this in full every time a timeframe changes" is addressed to a person; the model that picks coins for variants never sees it, and the data gate (stop 17) does the real check in code. Harmless, because code guards what the document warns about.
7. The guide is a good engine manual with its decision history pasted in. Three worked examples of what not to do (`:569-599`, the production config's refused chain), the D-149 sentence pasted mid-paragraph (`:321-324`, byte-equal to `forecast_rules.RULE_SENTENCE`, pinned by a test), bounds with their ruling dates (`:291`, `:656`), and the sizing block's full semantics (`:332-364`) are all correct; a model reads 659 lines to learn about 60 lines of rules. Stop 10 note 1.5 stands.

### (2) Legacy or simplifiable (leads)

1. `indicator_library.yaml` (320 lines): no live code reader (note 1.4); the header's KB read-view claim, `campaign_empirical_results: []` on every entry, the `typical_lag_bars` strings and the `edge_source_compatibility` lists feed nothing. Either wire it (memory writes results back, a reader groups by id) or cut it to a list of ids with one line each. Not checked: `indicator_library.schema.json` and the D-200 `regime_affinity` values (`SKILL.md:76`) against the file's `known_regime_affinity` keys (`trending`/`ranging`/`high_vol`, `:28-31`: three keys, not the skill's one value).
2. `coin_universe.yaml:1-7` header ("for instrument escalation", `default_exchange: binance`), `:201-229` (`escalation_order`, `timeframe_escalation`), per-coin `min_trade_count_floor` (`:19`) and `strategy_affinity` lists: the retired escalation route's fields. The live readers (`variant_coin.py:151-182`, `RP:19330-19334`) need `symbol`, `exchange`, `cache_key`, `data_cached` and the category name. Not checked: whether `min_trade_count_floor` or `strategy_affinity` has any reader.
3. `DATA_AVAILABILITY.md:82-89` (section 6, a Linear ticket status correction) and `:3-8` (what it was extracted from): maintenance notes, not availability facts. The playbook it supersedes (`TIMEFRAME_CHANGE_PLAYBOOK.md`) is still referenced from `DOC_INDEX.md` (stop 00 note 2.5).
4. `STRATEGY_DESIGN_GUIDE.md:569-599` (the production component shown twice, once as the refused pattern) and `:40-46` (the on/off class list, duplicated from the catalogue's Kind column, with "once that check ships" though it shipped as D-051): the second is a stale sentence; the first is a negative example a model does not need.
5. `COMPONENT_CATALOG.md:41-60` (naming rule and the nine misleading names "kept so past configs still load"): a rename list that is also an engine cleanup list (CUL-281 at stop 00). Nine of 28 rows carry a name the catalogue itself calls wrong.
6. The hypothesis-design skill `:76` ("Code groups tried ideas by `indicator_id`") and the library header `:3-5`: delete the sentence or build the grouping.
7. The guide's "Scale rule" (`:307-312`) and the 0.2 band / forecast-over-10 arithmetic appear in the guide, in quant-fundamentals (`:60-69`) and in the engine; three copies of one number (`config.json`, stop 13).

### (3) Disagreements between the speech and the element

1. Step 3, "code groups tried ideas by that name": no code does (note 1.4); the speech repeats the skill's stale sentence. Wrong as stated.
2. "Read by: ... step 2 (design guide, catalogue, coin universe, data availability)": step 2 does not receive `DATA_AVAILABILITY.md` (note 1.6); 1b receives it as optional only. "code (catalogue, coin universe, indicator library)": the library's code reader is a tool the campaign does not run. Two of the three code readers are right.
3. Reading map "Library readers: `tools/campaign_memory.py`": grep finds no `indicator_id`/`library_lookup`/`indicator_library` in that file. Wrong row.
4. Reading map "Who injects them ... `:3181-3190` (data availability)": those lines are the `validation` (refine-only) and `backtest_specification` (flag-off) entries, neither on the live path; the live injection of the doc is the 1b template's optional input.
5. Step 1 says 658 lines, step 2 182, step 3 320, step 4 228, step 5 89: the files end at 659, 183, 320 (not read to the end), 229, 90; the one-line pattern of earlier stops. "15 known indicators": 15 ids (grep); "22 coins in five categories": 22 `symbol:` rows, five category keys (`:11`, `:26`, `:53`, `:81`, `:97`); correct.
6. Section 6: both facts correct (`coin_universe.yaml:1`, `:7`; `indicator_library.yaml:3-5`); the speech does not say the library has no live code reader, nor that the universe's BTC/ETH rows default to the contaminated cache by the file's own rule (note 1.5).
7. Reading-map ranges verified against the guide's headings: `:7`, `:34`, `:74`, `:104`, `:222`, `:267`, `:369`, `:505`, `:533`, `:567`, `:624`; catalogue `:9`, `:29`, `:41`, `:61-118` (rows `:69-116` inside the markers `:67`/`:117`), `:119`, `:144`, `:171`; `DATA_AVAILABILITY.md` sections `:12`, `:20`, `:46`, `:60`, `:74`, `:82`; `RP:3169`, `:3202`, `:11693-11925`, `:9072-9100`; `forecast_rules.py:48`; the 1b template `:17-23`.
