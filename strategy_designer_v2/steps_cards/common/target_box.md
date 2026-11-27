What a run's target box is, how it is chosen, and which ideas act in it (the operator, 2026-11-27; next steps B2.1).
Read by `run_brief` (which writes it), `select_next` (which keeps the run in it) and line 7.g (which looks there first).
Code: `common/target_box.py`.

**A run's target box is the box (`market_profile.md`: one of the six market profiles and a side, long or short;
twelve boxes) where the run searches for strategies.** It is where the portfolio lacks strategies: each run searches
there, not wherever its ideas drift.

**Its elements:**
- **The box's profile:** one of the six profiles, trend and agitation ("rising agitated"). Never a trend or an
  agitation alone: a box is one of twelve.
- **The box's side:** long or short.

## The rule that chooses it (`--target-box auto`)
**The box with the most market days per strategy already named for it.**
- **Its strategies named exactly:** the proven and profitable strategies of the profile map (`market_profile.md`, "The
  profile map": step 5 confirmed, step 6 profitable enough) whose idea names **exactly** the box's profile, on the
  box's side (a "both" strategy counts on each side). An idea naming only "agitated" or only "rising" does not count
  for "rising agitated": it does not say its effect lives there. (The map places such a strategy in every profile its
  idea holds; that is why rising agitated looks covered, 10 long strategies, while no idea named it.)
- **Its share of market days:** the market's own share of the box's profile, read by the combination step's box
  reader (`orchestration/combine/helper/boxes.py`: on each strategy's own coins and dates, the share of coin-days in
  that profile) on the map's strategies, each strategy counted once (the mean of their shares). A strategy's reading
  is the one in `orchestration/combine/boxes.csv` (the reader's file, kept because the backtest records are not
  committed), else the reader on its record when it is on this machine; a strategy with neither is left out, and the
  number read is written with the choice.
- **Score = share / (1 + strategies named exactly).** The highest score wins; ties go to the larger share; then to
  the long side (the order of the twelve boxes: the rule needs one answer, and the long side is first in the map).
- **Why this rule:** a box no idea names is a market the research has never aimed at; a large box is where a strategy
  can trade often. Dividing by (1 + count), as `select_next` divides by (1 + generation), keeps one score.

## The operator's choice (`--target-box "rising agitated, long"`)
Any of the twelve boxes, written as its profile then its side. The rule is not applied.

## Kept in the run
Written once, before step 1, in `orchestration/loop/<run>/target_box.json` (beside `data_use.json`): the box, who
chose it (the rule or the operator), and for the rule the table of the twelve boxes (count, share, score). A resumed
run keeps it; a call naming another box is refused. A run without the option has no file and is unchanged.

## Which ideas act in the box
**An idea acts in the box when its profile shares the box's profile and its side includes the box's side.**
- **Its profile:** the idea file's `profile:` header line (`market_profile.md`, "An idea's profile"), read as
  `common/lib.py`'s `profile_name`. It acts in the box when the box's profile is its profile or one its profile holds
  ("rising" holds rising agitated; "agitated" holds it too; "rising calm" does not). One test: the words of the idea's
  profile and of the box's profile together are still one of the six profiles.
- **An idea naming no profile does not act in the box:** it says nothing of where its effect lives.
- **Its side:** the brief's `side:` header line (the brief the idea's header names, the run's copy in
  `01_brief/<run>/briefs/`, else step 1's list): "long only" is long, "short only" is short, anything else (no line,
  "long and short") is both sides. It is step 3's own source of the side (`03_test_plan/helper/make_test_plan.py`,
  `brief_side`), so the filter and the plan read the same side. Both lines are in files written before the test: the
  filter needs no plan.

## What the run does with it
- **`select_next`** lists an idea not acting in the box as "outside the run's box", not a candidate: the loop tests
  only ideas in the box.
- **A discovery outside the box** still becomes a brief (step 1's list, as before): it is kept for a later run; its
  ideas are listed in this run's queue as outside the box, not tested.
- **Line 7.g** is given the box as the first place to look, before the map's other empty boxes.

**Why this cannot leak:** the choice reads finished records (the map, the box reader's shares) before the run starts;
the filter reads the idea's and the brief's header lines. No bar of the run's data is read.
