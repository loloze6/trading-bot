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

- One idea's card in the tree: its title, the idea in one sentence (three lines at most), then its results in words:
  step 3 only when it refused, step 5's verdict with its t, step 6's with its Sharpe (operator, 2026-11-19). Tap it:
  the detail.
- The detail of a tested idea: its text; step 3's reason; step 5's measure, t and "decided by"; step 6's measures with the
  failed ones marked; under step 7, each line with its findings folded and the ideas it wrote as cards (two generations
  open); the book by window; cost and time per step, last (operator, 2026-11-19).
- Ideas not tested are in the tree too, greyed, with their place in the queue when the loop holds one; in the run's tree
  a branch's untested ideas fold into one line; under an idea, two generations show and deeper ones fold.
- A backtest page: the idea in one sentence, the book of all coins, then one coin at a time (its book by window and day
  by day); each coin's button green or red by the Sharpe of its own book.
- A "?" next to each notion that needs it: a plain-words explanation, written from the step cards and
  `common/measures.md`.
- What the page never shows: an opinion, a score of its own, a date of its own (dates shown are the record's own:
  journal lines dated in full, the engine's run times).

## The fields of a view
1. **Run line** (the list of runs, last updated first): name and bar size (from its backtests' ids, e.g. `_4h`; with
   more than one, how many backtests each; operator, 2026-11-21), dates, ideas, backtested ideas, cost, step time; "Is it
   real": step 5's counts, "Does it pay": step 6's, each in one fixed order (confirmed, inconclusive, rejected,
   mismatch, not observable; profitable, not profitable) with the best of its key figure (step 5: t; step 6: Sharpe);
   the depth in one line (field 11).
   - For: choosing which run to open.
   - Used by: the operator.
   - Without it: one opens runs blind.
2. **Purpose**: the run brief's `Purpose` paragraph; the whole run brief one tap away.
   - For: reading the results against what the run was for.
   - Used by: the operator.
   - Without it: results with no question.
3. **Briefs**: title, the whole text one tap away; under each, its ideas (an idea's brief is the number its id starts
   with: `011-01_...` is from brief 011; a brief written in another run is named with that run).
   - For: the theory the ideas come from, and which ideas come from which theory.
   - Used by: the operator.
   - Without it: ideas with no theory.
4. **Idea tree**: one node per idea, under the idea it came from (its id without the last segment); an idea whose
   parent is in another run is a root. The step 7 line that wrote an idea is named in words on the idea's page.
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
7. **Cost and time**: the sum of `usd` and `seconds` over the run's journal lines; per idea, per step (the step 7
   lines journaled "not run" in one line).
   - For: what the run cost.
   - Used by: the operator.
   - Without it: no cost to weigh the results against.
8. **What happened to each idea**: each idea in one state: backtested, blocked at step 3, planned but not backtested,
   waiting in the queue, duplicate (the queue's own word), not tested.
   - For: the run's ideas accounted for, untested and blocked ones included.
   - Used by: the operator.
   - Without it: the untested majority is invisible (night_013_run: 56 of 91 ideas waiting).
9. **Dates** (UTC): run: the earliest and latest full timestamps of its record (journal lines dated in full, written
   since 2026-11-17; the backtests' `manifest.json` `created_utc`); idea: its first dated journal line, else its
   backtest's `created_utc`; otherwise "date not recorded". Git commit times are not used (operator, 2026-11-17).
   - For: when a run happened, what is newest.
   - Used by: the operator.
   - Without it: runs with no order in time.
10. **Backtest page**: per coin, its own book by window (`metrics.json` net returns, chained) and its Sharpe on the
   coin's button, green above 0, red at or below: step 6's definition (`common/measures.md`: mean of the daily returns
   over their standard deviation, times the square root of 365) on the coin's own book from the chart files, a day's
   value being its last bar's; no chart files, no colour. The window-by-window table was removed (operator, 2026-11-19).
   - For: which coins and periods carry or sink the book.
   - Used by: the operator.
   - Without it: one averaged line hides the coin that lost.
   - Day by day, from the backtest's chart files (step 4): the committed `chart_bars.csv.gz` / `chart_trades.csv.gz`
     (backtests confirmed by step 5 or profitable enough by step 6) first, then `chart_*.local.csv.gz` (every other
     backtest; ignored by git, only on the disk where the run happened); neither: "not in the record". Per coin, the price with each trade's entry and
     exit, "1 invested": the strategy against holding the coin (each window's values over its first, windows chained in
     time order, from 1; log scale, the line at 1 marked "start"; operator, 2026-11-19), the forecast and the position, on one time axis; zoom with + / - / All, a pinch or the mouse wheel, move by
     dragging, read a day by touching it. The files are fetched when the page opens, never embedded.

11. **Depth**: per level below the brief (1: the brief's own ideas, 2: written from a level 1 idea, and so on; the
   number of segments in the idea's id), the ideas backtested of the ideas written: "L1 6 of 6 · L2 3 of 24 ...", on
   the run line.
   - For: how far each brief was explored, and at which depth what pays was found.
   - Used by: the operator.
   - Without it: no way to tell a brief tried once from one followed five generations down.

## Storage and naming
```
steps_cards/run_viewer/
  card.md            this card
  current_state.md   the measured picture: which file holds what, what is not committed
  helper/
    build_page.py    reads the run folders, writes runs.html (Python standard library only)
    page.html        the page: style and code; build_page.py puts the data into it
    test_build_page.py
  runs.html          the output, rebuilt by the script; committed on the run-visualizer branch so a phone can open it
                     (operator, 2026-11-17); ignored elsewhere (.gitignore)
```
Practice copied: a static report page (like a test coverage report): built from the files, one self-contained file,
rebuilt in seconds, never edited by hand.

## The AI
None: this function reads files and writes one page. No model call.

## Quality criteria
- Every figure on the page is a field of a committed file, or a count, sum, mean, product or largest of such fields;
  the tests check this on a small built-in run.
- Readable at 390 px width with no horizontal page scroll.
- Writes nothing but `runs.html`; reads nothing outside `steps_cards/`.
- A missing or unreadable file shows as "not in the record", never as a failure of the page.

## Who judges the output
The operator, by opening the page.

## Done when
- [x] The page lists the 11 runs, and for each tested idea shows steps 3, 5, 6 and the step 7 lines from the files.
- [x] The idea tree follows the ids, across runs.
- [x] The book by window is drawn for every idea with a backtest.
- [x] The operator has opened it on a phone (2026-11-17). First feedback built: dates, purpose subtitle, idea states,
  briefs linked to their ideas, backtest page, help buttons, two generations under an idea.
- [x] Day-by-day chart per coin (price and trades, book against holding, forecast, position), zoomable on a phone:
  checked at 390 px with touch (load, tap, +, pinch, drag, coin switch, no script error) on a corrected copy of one
  backtest's chart file. Real dates from the record.
- [x] The swapped `position` and `value` columns are fixed at step 4 (commit 2df7d7a2); the rewritten file of the
  checked backtest is byte-identical to the corrected copy the chart was tested on.
- [ ] Holding all the coins on the window chart: waits for the operator's ruling on the step 6 `curve.csv` proposal.

## Open (for the operator)
- The `curve.csv` proposal (`current_state.md`): one row per window, or one per week.
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
