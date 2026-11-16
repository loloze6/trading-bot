# Extraction brief for the overall-review note takers (2026-11-05)

You are a note taker for the first post-tour overall review of the trading-bot research workflow.
Repository: /home/user/trading-bot (already checked out on the right branch). SR = strategy-research/, TB = trading-bot/.

## The goal everything is judged against
A pipeline that finds a profitable automated trading strategy by itself, run autonomously and
continuously, with the operator deciding and the pipeline discovering, without fooling itself.

## Your sources (read-only; read nothing else unless told)
Stop files `guided_tour/NN_*.md`, each with three sections:
- "## Speech": what the element is. Read only enough to know what the element is (section "In one sentence", "Why it exists", "What is switched off").
- "## Operator remarks": the operator's own words, verbatim. PRIMARY voice. Some stops have none (15-18, 21a).
- "## Inspector notes": "(1) Design and mechanism", "(2) Legacy or simplifiable", "(3) Disagreements". Read (1) and (2) fully. SKIP (3) entirely.

## Hard rules
- Read-only. Write only your one output file (named below). Do not edit any other file. No code, no runs, no tests.
- Never open `trading-bot/local_data/` or anything named `holdout_sealed`. Never write a calendar date range that could be a holdout or protocol window; fold ids (A-D) and years only. Do not write any date you read from `SR/config/campaign_data_policy.yaml` (do not open it).
- Quote the operator VERBATIM, in quotation marks, with the stop ref (e.g. `[stop 07]`). Never paraphrase a remark as if it were yours. Keep the operator's spelling and typos.
- Not a detail review: no line-number chasing, no small errors, no speech-vs-code disagreements. High level: feelings about the design and the business process.

## What to write (plain words, short sentences, markdown)
For EACH stop in your group:
1. **Element** (one line): what it is, in business words.
2. **Operator themes**: each theme in one line, then the verbatim quote(s) that carry it (keep quotes short, 1-3 sentences each, but complete sentences; multiple quotes allowed). If a "direct" answer from the guide changed the picture, say so in one line. If the operator has no remarks, say "No operator remarks".
3. **Inspector design themes (part 1)**: 2-5 bullets. Does the inspector think this element helps reach a profitable strategy? Where is it weak? Any numbered finding IDs the inspector uses (e.g. "07-3") keep them.
4. **Inspector legacy themes (part 2)**: 2-5 bullets, the big ones only (what could be removed or simplified and why), with lead IDs if present.
5. **Convergence**: one line: do operator and inspector agree, diverge, or talk past each other, on this stop?
6. **Feeling**: one word for the element from {keep, simplify, rethink, remove} and one line why. This is your reading of the two voices, not a ruling.

Then, at the end of your file, a **Group synthesis**: 
- the 3-6 cross-stop themes you see in your group (operator-led, inspector-led, or both), each with stop refs;
- any remark where the operator speaks about the WHOLE workflow (rebuild vs clean up, what the pipeline is for, autonomy, trust, cost, what they want to decide themselves): quote these verbatim and completely, they matter most;
- any remark where the operator says what they would do differently or what they want.

Length: about 250-400 words per stop plus the synthesis. Precision over coverage: the quotes must be exact.
