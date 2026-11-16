# Group 1 notes: stops 00, 01, 02, 03a, 03b, 04 (2026-11-05)

Sources: the six stop files under `guided_tour/`. Operator quotes are verbatim, typos kept. Inspector part (3) skipped.

---

## Stop 00: Orientation (SR/CLAUDE.md, USER_GUIDE §2, run_102 state file)

**Element.** The map a newcomer reads first: the research project's house rules, the official stage diagram, and one real run's state file showing which stages actually ran.

**Operator themes.**
- The house-rules file is mostly legacy and should be cut down hard, not curated.
  "Globally i would delete most of the content, as it seems legacy / confusing / too detailed / wrongly located in claude.md." `[stop 00]`
  "I would not spend much time ensuring that we do not loose info or that it is legacy, it does not worth it in my opinion." `[stop 00]`
- Keep only behavioural rules; engine and workflow rules led to surprises.
  "Validation is falsification-first led to unexpected behavior. So i would keep only rules related to behaviors not engine or workflow." `[stop 00]`
- A proposed shape for the file.
  "At best i would organize it in real memory category: Objective of the workflow of strategy research + quick overview ; Memory already there around behavioral aspects ; Memory around developments processes / test ." `[stop 00]`
- DOC_INDEX: delete it (preferred) or commit to maintaining it.
  "Either we delete it and its refrence (prefred like this) or we ensure that it is maintained and that all docs refrenced are updated and maintained." `[stop 00]`
- The stage list is wrong; the schemas block is misplaced.
  "Pipeline stages are wrong." / "Schemas block do not belong here." `[stop 00]`
- The run state file carries legacy sections.
  "Artifacts is empty. Governance seems legacy. Counters are linked to mechanics. Flags  seems for some of them legacy. Globally the part :17 to 29 seems challengeable." `[stop 00]`

**Inspector design themes (part 1).**
- SR/CLAUDE.md reaches no pipeline step (`setting_sources=[]`); it only shapes human and build sessions. It cannot move the pipeline toward the goal (00-1.1).
- The "screening, walk-forward, holdout" ladder in the rules does not exist in the live run; the state-file flags have no live writer. Progress is really tracked by the grid, the profit bars and the block registry (00-1.2).
- The stage registry still encodes the flag-off path; the live path exists only as overrides in `run_loop`. A session orienting from the registry builds for a path no run takes (00-1.3).
- The loop as oriented is not closed: no branch picks the next idea, decide-next does, behind a human approval gate. "Autonomous and continuous" is not the current shape (00-1.4).
- State-file lines 16-30 carry no live information; the cost ledger covers only AI calls (analyst ~79% of ~8.25 USD) and omits backtest compute (00-1.5, 00-1.6).

**Inspector legacy themes (part 2).**
- Replace the 65-line "Workflow stages" section with a one-line pointer to the guide (00-2.1); move the schemas note to artifact docs (00-2.2); delete the engine rules at `:16-18` (00-2.3).
- Delete the unread `pipeline_state.yaml` template and the dead state keys in `setup_run.py` (00-2.6).
- Redraw USER_GUIDE §2.1 as the live shape and move the flag-off diagram to a legacy appendix; blocked by a test that pins a block per registry entry (00-2.8).
- DOC_INDEX is recently touched and pointed to from eight live lines; deletion is cheap only if the pointers go too (00-2.5).

**Convergence.** Agree. Both say the orientation documents describe a pipeline that no longer runs; the inspector adds that the docs cannot affect runs anyway.

**Feeling.** Simplify. Both voices want the house rules shrunk to purpose, behaviour, and development process; the inspector's evidence shows nothing is lost by cutting.

---

## Stop 01: The brief

**Element.** The single input a run starts from: a form with a machine-read top block (idea, venue, product, coins, bar size, criteria, test period) and people-only prose; written by the operator or by decide-next.

**Operator themes.**
- The prose part has no guidance and becomes a mess nobody reads.
  "the brief template seems not giving enough guideline for the people-only part. As a results what we can find here is a mess (and worst might be lost as not read)." `[stop 01]`
- A claim should be a separate, structurally checked object, referenced from the brief.
  "Couldn't we have a separated structurally check "claim" object with reference only ? Reference listed in the brief." `[stop 01]`
  "Remember, a claim is an idea / a statement which give information on the behavioral elements for establishing a strategy, associated with quantitive tests and pass criteria that would allow us to prove this idea is valid." `[stop 01]`
- Field names are not self-explanatory; guidance for a new agent is missing.
  "Also thinkin that these names are really not self explanatory (criteria_from is authoritarive claim/ constraints is authoritative strategy_config)" `[stop 01]`
  "Here we would dictate a strategy without knowing the claim." `[stop 01]`
- Scope: drop the hourly/daily limit; keep the rest.
  "I would also challenge the Hourly or daily bars scope. I do not want to trade above daily (weekly/monghtly). However the backtest is smart enough to allow a trading at any granularity. Rest of the scope is good and should be kept as instruction." `[stop 01]`
- Claim-test capabilities and fold rules belong in dedicated guideline docs, not the template.
  "For me we should have it in a dedicated claim creation guideline doc (read by multiple steps)." `[stop 01]`
  "I would prefer having fold creation guideline in a separated doc. Also having start and end and window month might sound risky (too many rules), i would prefer to keep only the fold capability." `[stop 01]`
- Most fields optional; the rest decided later by the workflow.
  "Mandatory should be on strategy domain/research goal/venue/product." `[stop 01]`
  "When not provided, timeframe, available date, criteria, scope, constraints, fold should be considered as None or empty, and decided later in one of the workflow step." `[stop 01]`
- The decide-next brief is organised differently and carries doubtful data.
  "Why do we have source observation ? Is there a logical need to give it to step 1a?" `[stop 01]`

**Inspector design themes (part 1).**
- Only six keys plus `machine_constraints` are read as values; `scope`, `available_data` and `source_observations` reach the pipeline only as prompt text, and `available_data` has no reader at all (01-1.1).
- `criteria_from: hypothesis_generation` is load-bearing: omit it and a hand brief silently runs its backtests and ends without a verdict. Decide-next briefs are safe; hand briefs are not (01-1.2).
- An exact config is built regardless of what 1a concluded; nothing at this stop ties config to claim (01-1.3). Start/end/window_months are mandatory reads but ignored under a fold (01-1.4).
- Decide-next briefs carry no `scope` block although the 1a skill tells the model to use it; on the live loop this is the common case (01-1.6). The scope's 25 file:line pointers are partly stale and the model has no file tool (01-1.7).
- The candidate brief repeats its claim and its config change three times and ships a stale manifest rationale to 1b; 443 of 699 lines are observations with no code reader (01-1.8, 01-1.9).

**Inspector legacy themes (part 2).**
- Delete `available_data`; retire the second brief template (01-2.1, 01-2.2).
- Fold-only test period, code derives the span (01-2.4). Line-number pointers in the template should name functions or go (01-2.5).
- Render the scope by code at materialisation for every brief, or drop it and stop the skill naming it (01-2.6).
- Collapse the duplicate claim/change copies in candidate briefs; filter empty and duplicate observations (01-2.7, 01-2.9).

**Convergence.** Agree, with the inspector adding a warning: the operator's "mostly optional" wish collides with a required-key tuple and a silent-degradation path the operator did not know about.

**Feeling.** Rethink. The form mixes idea, trading parameters, claim, config and test period under unclear names; both voices want a smaller form with the claim and the fold pulled out into their own objects.

---

## Stop 02: Registration and the queue

**Element.** The campaign's backlog: a registrar that checks a brief's shape and appends one line to the to-do list, which is also the full history of every brief taken on.

**Operator themes.**
- A retired mechanism should not still be checked.
  "CHallenge here on It looks for an old pass/fail block from the retired verdict system. An empty one is refused. . If it is retired, why checking it. It seems adding complexity for nothing." `[stop 02]`
- The element is understood as the backlog manager.
  "Thanks, clear, so, in general this step is the workflow input backlog manager from my understaindg" `[stop 02]`

**Inspector design themes (part 1).**
- The operator's reading is right: the door checks form, not substance. The expensive mistake (a repeat idea) is not caught at the door but after 1a and 1b are paid for (02-1.1).
- No run self-launches: agent entries start blocked on operator approval, so "autonomous and continuous" is by the flag "run one brief, stop, wait for a person". This is the operator's chosen mode (D-071) (02-1.2).
- The retired promotion check exists only because `verdict_routing_retired` is still a flag; the simplification is upstream (02-1.3).
- `register` takes no lock while the runner rewrites the whole queue at each save: a registration can be lost silently (02-1.4).
- The vocabulary check is a real anti-fooling guard, but statuses are a regex, not a closed list (02-1.5). One file is both to-do list and load-bearing history, 76 entries rewritten whole each save (02-1.6).

**Inspector legacy themes (part 2).**
- Three functions serve a `promotion` key no live path reads; remove with the retired routing (02-2.1).
- `relation` carries one constant on the live path; remove (02-2.2).
- Legacy entry fields (`title`, `verdict_status`, several schema keys) and unused `origin` values and the `queued` status are candidates for pruning (02-2.3 to 02-2.6).
- Legacy-routing constants live only as refusals of shapes no run produces (02-2.7).

**Convergence.** Agree. The operator's one challenge is confirmed and traced to its cause (a flag that will never be switched back).

**Feeling.** Keep. The backlog itself is sound and cheap; what should go is the retired-routing residue around it, and the lock gap deserves a fix.

---

## Stop 03a: The switchboard, orchestrator flags

**Element.** The one file where the operator turns each piece of the process on or off and sets a token budget and model choices; 34 switches, 30 on.

**Operator themes.**
- Clean the file: drop unused flags and "core" flags that will never be switched back; keep only the modular ones.
  "Indeed, i would really propose to clean this file :" `[stop 03a]`
  "- removing the flags that we consider as "core" functionality of the workflow (mostly flagged initially to secure the delivery, but that would never be switched back again)" `[stop 03a]`
  "- keep the ones that are aligned with a "modular" workflow approach, eg: when a component is missing, the nearest buildable version is built instead, eg: list of tried ideas shown to AI." `[stop 03a]`
- Less wording, categorised.
  "- i would also limit the information wording to a reasonable amount (informing about functionality switched on/ not full history)" `[stop 03a]`
  "- i would categorize it to make it readable" `[stop 03a]`
- Budget and model settings are fine.
  "- model and budget makes sense" `[stop 03a]`

**Inspector design themes (part 1).**
- The switchboard describes one configuration, not a space: at least twelve flags' off-state is the retired pipeline and their dependency chains mean none can be turned off alone. A newcomer reads 1,145 lines to learn there is one path (03a-1.1).
- The only real choices left are three off flags and quarantine; quarantine off is the single largest autonomy limiter after operator approval: every halt stops the campaign until a person resumes (03a-1.2).
- The pre-flight checks are sound, but flag values are re-read from disk many times per run; a run cannot record "the flags I ran under" (03a-1.3).
- Step 2 (the step that most shapes what gets backtested) runs on the cheapest model with quality "not measured" (03a-1.4).
- Comments contradict the live state in at least six places; the file is "a decision log pretending to be a config" (03a-1.5, 03a-1.6).

**Inspector legacy themes (part 2).**
- Five dead keys at the top of the section (03a-2.1). `stale_input_path_fix` is a bug fix kept as a switch; fold into code (03a-2.2).
- Three switches for one feature (profit bars); one switch, or none (03a-2.5). `grid_evaluation` read under two names; one name (03a-2.7).
- `composition_runs` on with nothing to compose (03a-2.9). Analyst caps as comments: real keys or removed (03a-2.10).
- A reading of live values is 34 lines; the operator's "limit wording, categorise" is a 30x reduction (03a-2.11).

**Convergence.** Agree. The inspector's analysis of the dependency chains is the evidence for the operator's "core vs modular" split.

**Feeling.** Simplify. Fold the one-path flags into code, keep a short categorised list of modular switches, budget and models.

---

## Stop 03b: The switchboard, other sections and the flag register

**Element.** Five statistical settings sections written for the record (no code reads them) and a 929-line register that mirrors every switch with owner, state and reason, enforced by tests.

**Operator themes.**
- Delete the legacy; only workflow mechanism parameters belong in the config.
  "Same remarks than before - i would clean the ones legacy by deletion. In the file should sit only mechanism workflow parameter - no statistical / specific / etc..." `[stop 03b]`

**Inspector design themes (part 1).**
- The settings sections are not configuration: a second copy of code constants with a parity test. Deleting them changes no run; the rationale text belongs beside the constant in code (03b-1.1).
- Two of the five sections belong to stages no run reaches; one has no reader at all and its only mention is a stale docstring (03b-1.2).
- The register is a mirror with prose; its test checks state parity but not the prose, so 25 "on" entries still carry a "blocked_on" from when they were off. It teaches the flag-off pipeline as current (03b-1.3, 03b-1.4).
- The one register entry that touches the backtest is `model_funding` off: every perp brief is backtested without funding, a real modelling gap for the goal (03b-1.5).
- Quarantine, the switch that most bears on continuous running, has no register line and is outside the test's guarantee (03b-1.6).

**Inspector legacy themes (part 2).**
- Delete `symbol_correlation` and `verdict_interpreter`; move `episode_significance` rationale to code; rename or move `prescreen` (03b-2.1 to 03b-2.5).
- Reduce the register to name, state, one-line effect and blocker for off entries (03b-2.6).
- A sync test pins a dead config key to a source-text literal (03b-2.7).

**Convergence.** Agree. The inspector confirms nothing live depends on these sections and adds the funding gap as the one item of substance.

**Feeling.** Remove. The settings sections and most of the register are documentation of a past delivery process; the funding gap is the only thing here to carry forward.

---

## Stop 04: Launch

**Element.** The launcher: takes the next line off the backlog, opens a run folder, writes the brief and the frozen pre-registration (criteria and test period fixed before any result), checks the switchboard and the lock, and hands over to the orchestrator.

**Operator themes.**
- Three steps were unclear and needed direct answers (actions, pre-registration checks, the ideas-already-produced file). The guide's answers changed the picture: the operator now reads the step as a mechanics-and-orchestration step and summarises it in nine bullets.
  "Ok so i think i understand that we are testing the validity of the criterias associated to a claim, the ones that will decided pass/fail. ONLY  when claims are given in brief and not decided step 1a." `[stop 04]`
- Validation of criteria and windows does not belong at launch; the writer is responsible.
  "The part about "in case of claim given, check validity" as well as "in case of windows, check time". For me this is not the place. The writer should be responsible to ensure that both are valid." `[stop 04]`
  "But this step should be mechanics around run preparation and orchestration of calls around that." `[stop 04]`
- Legacy to be cleaned here too.
  "Of course legacy should be cleaned as well." `[stop 04]`

**Inspector design themes (part 1).**
- The launcher's one job for the goal is to freeze the rules before any result; that part is sound and read back by the grid. Everything else is routing around it (04-1.1).
- On the operator's challenge the code half-agrees: of six pre-registration checks only two do work on the live path; the lints could move to the writers, but the menu resolution must stay at launch because it is what fixes the rule on launch day (04-1.2).
- The venue check has no effect until a holdout spend: a non-tradable brief would be researched to the end (04-1.3).
- The protocol pre-flight is almost entirely for legacy shapes; for the live case its real content is "the fold's windows generate and clear the holdout" (04-1.4).
- The sealed range is copied in clear into every run's pre-registration and seen by 1b's prompt; the rule says to refer to it only through the policy file (04-1.7). The orphan scan clears nothing; the operator's summary misreads it (04-1.8).

**Inspector legacy themes (part 2).**
- The refinement-brief action and its helpers go with the retired routing (04-2.1); the pinned/promotion/regeneration branches of the pre-flight serve three legacy briefs (04-2.2).
- Six of nine handoff templates are copied into every run for stages it will not reach (04-2.3). `setup_run.py` predates the runner and writes a TODO brief overwritten seconds later (04-2.4).
- Three pre-registration fields per run with no reader (04-2.5). The dry run simulates legacy states only (04-2.7).

**Convergence.** Mostly agree. The operator wants validation moved to the writers; the inspector agrees for the lints but keeps the resolution step at launch as the anti-fooling guarantee.

**Feeling.** Simplify. Keep lock, folder, pre-registration freeze and hand-over; strip the legacy branches and move the form lints upstream.

---

## Group synthesis

### Cross-stop themes

1. **The documents and config describe a pipeline that no longer runs (inspector-led, operator agrees).** SR/CLAUDE.md, the §2 diagram, the stage registry defaults, the flag comments and the register all teach the flag-off shape as current; the live shape exists only as overrides and prose. Stops 00, 03a, 03b, 04.
2. **One path, many switches (both).** At least twelve flags can never be turned off without reviving retired routing; the retired-routing residue then shows up as checks at the door (stop 02), launch actions and pre-flight branches (stop 04), and 65 lines of flag history (stop 03a). The operator's "core vs modular" split is the decision rule. Stops 02, 03a, 03b, 04.
3. **Cut, do not curate (operator-led).** At every stop the operator chooses deletion over maintenance and says explicitly not to spend time preserving legacy content. Stops 00, 02, 03a, 03b, 04.
4. **The brief needs to become smaller and its parts separated (operator-led, inspector supports with evidence).** Claim as its own object, fold as its own guideline, most fields optional, names that say what they are. The inspector adds the traps: a missing default silently degrades a run, and the live child briefs carry no scope block. Stops 01, 04.
5. **Autonomy is bounded by two deliberate switches (inspector-led, not yet ruled on by the operator).** Operator approval on every agent line and quarantine off mean every run end and every halt wait for a person. The inspector records this as the operator's chosen mode. Stops 00, 02, 03a, 03b.
6. **Mechanics vs controls (operator-led).** The operator wants launch to be pure run preparation and the writers to own validity; the inspector keeps one check at launch (rule resolution on launch day) as the anti-fooling guarantee. Stop 04, with stop 02 (door checks form, not substance).

### Remarks on the whole workflow (verbatim, complete)

"Globally i would delete most of the content, as it seems legacy / confusing / too detailed / wrongly located in claude.md. 
I would not spend much time ensuring that we do not loose info or that it is legacy, it does not worth it in my opinion. At best i would organize it in real memory category: Objective of the workflow of strategy research + quick overview ; Memory already there around behavioral aspects ; Memory around developments processes / test . Any other suggestion are welcomed." `[stop 00]`

"Some of global rules are referencing legacy files. Some are by design in the workflow artifacts
Validation is falsification-first led to unexpected behavior. So i would keep only rules related to behaviors not engine or workflow." `[stop 00]`

"Indeed, i would really propose to clean this file : 
- removing the flags not used
- removing the flags that we consider as "core" functionality of the workflow (mostly flagged initially to secure the delivery, but that would never be switched back again) 
- keep the ones that are aligned with a "modular" workflow approach, eg: when a component is missing, the nearest buildable version is built instead, eg: list of tried ideas shown to AI.
- some that might sound duplicate (eg: pausing when approximation? 
- i would also limit the information wording to a reasonable amount (informing about functionality switched on/ not full history) 
- i would categorize it to make it readable" `[stop 03a]`

"Same remarks than before - i would clean the ones legacy by deletion. In the file should sit only mechanism workflow parameter - no statistical / specific / etc..." `[stop 03b]`

"Challenge: 
The part about "in case of claim given, check validity" as well as "in case of windows, check time". For me this is not the place. The writer should be responsible to ensure that both are valid. Happy to be challenged, or even to move the control in another place. But this step should be mechanics around run preparation and orchestration of calls around that. 
Of course legacy should be cleaned as well." `[stop 04]`

### What the operator would do differently or wants

- Brief template: "I would suggest to change the research brief template to clearly indicate objective of the prose and redactional instruction fitting the objective (a few words on context around brief drafting, a really simple purpose of the brief, plain words, etc... and a suggestion of maximum lenght" `[stop 01]`
- Brief structure: "Also i would challenge the category of the brief that could be separated in : 
Ideas (research goal) and trading param (venue, product)" `[stop 01]`
- Mandatory fields: "Finally on this template, i would like to ensure that most of the fields are optional.. Mandatory should be on strategy domain/research goal/venue/product." `[stop 01]`
- Claim object: "Couldn't we have a separated structurally check "claim" object with reference only ? Reference listed in the brief." `[stop 01]`
- Guideline docs: "For me we should have it in a dedicated claim creation guideline doc (read by multiple steps)." and "I would prefer having fold creation guideline in a separated doc." `[stop 01]`
- Scope: "I do not want to trade above daily (weekly/monghtly). However the backtest is smart enough to allow a trading at any granularity. Rest of the scope is good and should be kept as instruction." `[stop 01]`
- DOC_INDEX: "Either we delete it and its refrence (prefred like this) or we ensure that it is maintained and that all docs refrenced are updated and maintained." `[stop 00]`
- Run state file: "If this file is useful, it could be explained in claude.md when we want to have an overview of the workflow mechanical specific to a run." `[stop 00]`
- Retired checks: "If it is retired, why checking it. It seems adding complexity for nothing." `[stop 02]`

### Note for the review

The operator has not yet spoken, in this group, on the autonomy limiters the inspector names (operator approval on every agent line, quarantine off, the analyst's share of run cost, the missing funding cost on perp backtests). These are the group's open questions for the operator rather than disagreements.
