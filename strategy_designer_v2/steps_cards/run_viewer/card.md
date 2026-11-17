# Function card: run viewer (2026-11-17)

## Business objective, one question
What did a research run do, and what came out of it?

**One page, readable on a phone, that gathers a run's committed files and shows its brief, its ideas, and for each
tested idea its steps in order with each step's result. Pure mechanics: it shows what the files say, it judges nothing.**

## Input
The committed files of the runs in `steps_cards/` (the `<name>_run` folders in each step's folder), read only. The list of
files and what each holds is in `current_state.md`. Nothing else: no price data, no `local_data/`, no model call.

## Output
One file, `run_viewer/runs.html`: self-contained (data, style and code inside, no network), opened in any browser, on
a PC or a phone.

## What a view of a run is
**A view of a run is the run's purpose, its briefs, and its ideas as a family tree, each tested idea showing its steps
in order with one result per step, and the run's cost and time.**

- One idea's line in the tree, left to right: step 3 (plan, or refused), step 5 (confirmed, inconclusive, rejected,
  not observable, with its t), step 6 (pays or not). Tap it: the detail.
- The detail of a tested idea: its text; step 3's reason; step 5's measure, t and "decided by"; step 6's measures with the
  failed ones marked; the step 7 lines with their findings and the ideas they proposed (links into the tree); the book
  by window; cost and time per step.
- Ideas not tested are in the tree too, greyed, with their place in the queue when the loop holds one.
- What the page never shows: an opinion, a score of its own, a date of its own.

## The fields of a view
1. **Run line** (the list of runs): name, ideas tested, step 5 and step 6 counts, cost, time.
   - For: choosing which run to open.
   - Used by: the operator.
   - Without it: one opens runs blind.
2. **Purpose**: the run brief's `Purpose` paragraph; the whole run brief one tap away.
   - For: reading the results against what the run was for.
   - Used by: the operator.
   - Without it: results with no question.
3. **Briefs**: title, the whole text one tap away.
   - For: the theory the ideas come from.
   - Used by: the operator.
   - Without it: ideas with no theory.
4. **Idea tree**: one node per idea, under the idea it came from (its id without the last segment). The line letter
   (b, d, g...) of the step 7 line that wrote it shown on the node; an idea whose parent is in another run is a root, and
   says where it came from.
   - For: how ideas lead to one another.
   - Used by: the operator.
   - Without it: a flat list of 40 ids that look alike.
5. **Step results**: step 3 `outcome` and `Reason`; step 5 `status`, t, `decided_by`; step 6 `status` and failed
   measures; step 7 `line`, `findings`, `ideas`.
   - For: the steps' answers, read from their own files.
   - Used by: the operator.
   - Without it: no result to read.
6. **Book by window**: each window's net return (`metrics.json`) averaged over the coins, chained in the windows' time
   order, from 1. Labelled with years only.
   - For: seeing how the book's value moved over time.
   - Used by: the operator.
   - Without it: the measures of step 6 with no picture.
   - Holding the coins: not in the committed files, so not drawn. Proposal in `current_state.md` (step 6 writes `curve.csv`).
7. **Cost and time**: the sum of `usd` and `seconds` over the run's journal lines; first and last journal time.
   - For: what the run cost.
   - Used by: the operator.
   - Without it: no cost to weigh the results against.

## Storage and naming
```
steps_cards/run_viewer/
  card.md            this card
  current_state.md   the measured picture: which file holds what, what is not committed
  helper/
    build_page.py    reads the run folders, writes runs.html (Python standard library only)
    page.html        the page: style and code; build_page.py puts the data into it
    test_build_page.py
  runs.html          the output; rebuilt by the script, kept out of git (.gitignore)
```
Practice copied: a static report page (like a test coverage report): built from the files, one self-contained file,
rebuilt in seconds, never edited by hand.

## The AI
None: this function reads files and writes one page. No model call.

## Quality criteria
- Every figure on the page is a field of a committed file, or a count or sum of such fields; the test checks this on a
  small built-in run.
- Readable at 390 px width with no horizontal page scroll.
- Writes nothing but `runs.html`; reads nothing outside `steps_cards/`.
- A missing or unreadable file shows as "not in the record", never as a failure of the page.

## Who judges the output
The operator, by opening the page.

## Done when
- [x] The page lists the 11 runs, and for each tested idea shows steps 3, 5, 6 and the step 7 lines from the files.
- [x] The idea tree follows the ids, across runs.
- [x] The book by window is drawn for every idea with a backtest.
- [ ] The operator has opened it on a phone. (status: waiting)
- [ ] Holding the coins on the chart: waits for the operator's ruling on the step 6 `curve.csv` proposal.

## Open (for the operator)
- The `curve.csv` proposal (`current_state.md`): one row per window, or one per week.
- Commit `runs.html` too, so a phone can fetch it without a PC? It is about 1 MB and rebuilt after every run; kept out
  of git for now ("records stay small").
- `verdicts_run2/` (full_data_run, hourly_run): a second set of verdicts on the same backtests. Not shown.

## What this function does not do
It does not judge, rank, filter or recompute a result; it does not read prices; it does not run anything.

## How to use
```
python strategy_designer_v2/steps_cards/run_viewer/helper/build_page.py
```
Then open `strategy_designer_v2/steps_cards/run_viewer/runs.html`. On a phone: copy the file to it (any file app opens
it), or serve the folder on the home network:
`python -m http.server 8770 --bind 0.0.0.0 --directory strategy_designer_v2/steps_cards/run_viewer` and open
`http://<PC address>:8770/runs.html`.
