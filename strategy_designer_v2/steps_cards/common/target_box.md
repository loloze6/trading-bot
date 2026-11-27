What a run's target box is, how it is chosen, and how a run keeps to it (the operator, 2026-11-27; next steps B2.1,
revised the same day). Read by `run_brief` (which writes it and checks the brief), step 2 and every step 7 line (the
box is part of the brief's theme: `theme.md`), and `loop` (which records whether each idea acts in it).
Code: `common/target_box.py`.

**A run's target box is the box (`market_profile.md`: one of the six market profiles and a side, long or short;
twelve boxes) where the run searches for strategies.** It is where the portfolio lacks strategies: each run searches
there, not wherever its ideas drift.

**Its elements:**
- **The box's profile:** one of the six profiles, trend and agitation ("falling calm"). Never a trend or an agitation
  alone: a box is one of twelve.
- **The box's side:** long or short.

## Three ways to start a run
- **No option:** the run as before: no box, no note, no check, no field.
- **`--target-box auto`:** the rule below picks the box.
- **`--target-box "falling calm, long"`:** the operator's choice, any of the twelve boxes (its profile, then its side).

## The rule that chooses it (`auto`)
**The box with the most market days per strategy already named for it.**
- **Its strategies named exactly:** the proven and profitable strategies of the profile map (`market_profile.md`, "The
  profile map": step 5 confirmed, step 6 profitable enough) whose idea names **exactly** the box's profile, on the
  box's side (a "both" strategy counts on each side). An idea naming only "agitated" or only "rising" does not count
  for "rising agitated": it does not say its effect lives there.
- **Its share of market days:** the market's own share of the box's profile **on the 25 portfolio coins, 2016-2026**:
  the coins and days of the common records (`data_use.md`, steps 9 and 10). Read from the last portfolio version built
  on them (`orchestration/combine/portfolios/<v>/boxes.csv`, the box reader `boxes.py` on each candidate's common
  record), each candidate counted once. **Why these coins:** the portfolio trades and is judged on them; a box is worth
  filling for the days it has there, not on the research coins a strategy happened to be tested on.
- **Score = share / (1 + strategies named exactly).** The highest score wins; ties go to the larger share.
- **A tie of the two sides of one profile** (they always have the same share): the side with **fewer strategies acting
  in the box at all**, the profile map's own count (wider-profile ideas included). A tie still left: the map's order.
- **Why this rule:** a box no idea names is a market the research has never aimed at; a large box is where a strategy
  can trade often. Dividing by (1 + count), as `select_next` divides by (1 + generation), keeps one score.

## Kept in the run
Written once, before step 1, in `orchestration/loop/<run>/target_box.json` (beside `data_use.json`): the box, who
chose it (the rule or the operator), and for the rule the table of the twelve boxes (counts, share, score) and where
the shares came from. A resumed run keeps it; a call naming another box is refused.

## A boxed run's brief
**It names a profile and a side that hold the box**, in its header: a `profile:` line naming the box's profile or a
wider one holding it ("falling", "calm" or "falling calm" for falling calm), and a `side:` line including the box's side
("long only" or "long and short" for long). Otherwise `run_brief` refuses it, with the reason, before step 2. A brief from a theme or a source is written by step 1
inside the box (below), so the operator can launch a boxed run with a theme that says nothing of the box. Why: the
brief's theme is the run's question; a theme about another market would set every line against the box.

## The box is part of the brief's theme
In a boxed run, **the theme's situation includes the box's profile and side** (`theme.md`). One note, written by code
from the run's `target_box.json` (`target_box.py`, `theme_note`), is pasted after the brief wherever a prompt is given
the brief: step 1 when it writes the run's brief or a discovery's brief (`01_brief/helper/make_brief.py --run`, which
`run_brief` passes only for a boxed run; the brief then has `profile:` and `side:` header lines), step 2
(`02_ideation/helper/make_ideas.py`) and every step 7 line (`07_common/helper/analyse.py`, the
lines 7.a to 7.g). It asks every idea to keep to the box: its situation in the box's profile, named in a `profile:`
line, its position on the box's side, named in its `side:` line; and a discovery (a pattern off the theme) to be looked for inside the box only.
Without a box the note is empty and the prompts are byte for byte as before.

## A boxed run starts from the ideas already written in its box (next steps B13; the operator, 2026-11-27)
**Before its first turn, a boxed run takes the untested ideas of every other run that name its box exactly**; they are
ranked with the run's own ideas by `select_next`'s one score, then the loop goes on as usual.
- **Named exactly:** the idea file's `profile:` line is the box's profile word for word (as `profile_name` reads it): an
  idea naming only "falling" or only "calm", or no profile, is not taken. **Its side is known and is the box's side**
  (next steps A12; the operator, 2026-11-27): the idea's side below. An idea whose side is unknown, or is `both`, is
  not taken.
- **Untested:** no step 5 answer in any run (the `step5` field of every run's `orchestration/run_idea/*/table.json`).
- **Kept as written:** the idea keeps its id and its brief. The loop copies the idea file into the run's step 2 folder
  (`02_ideation/<run>/ideas/`, where `run_idea` copies every idea it tests) with one header line added,
  `taken-from: <its run>`, and copies its brief into the run's briefs (`01_brief/<run>/briefs/`, as `run_idea` does).
- **No clash with the run's own ideas:** a brief's own ideas are those with its number whose header names that brief
  (`run_brief`, `ideas_of`), not the number alone: brief numbers were shared by parallel sessions (next steps E3), so an
  idea taken from another run with the same number is not counted as the run's own brief's. An id already written in
  the run is not taken again; an id found in several runs is taken once, from the first run by name.
- **Recorded:** one line per idea taken in `loop.jsonl` (`"taken"`: the id, `"from"`: its run), and each turn of such an
  idea carries `taken_from`, so the reading counts them and what they gave. Taken again on resume: only ideas not yet in
  the run.

## Visibility, not control
An idea written outside the box anyway is neither refused nor filtered: it is tested like any other. **Each turn of a
boxed run says whether its idea acts in the box** (`loop.jsonl`, field `in_box`), so the reading can count them. An
idea acts in the box when its `profile:` line holds the box's profile and **its own side is the box's side** (the
idea's side below). An idea naming no profile, or whose side is unknown, is counted outside.

## The idea's side (next steps A12; the operator, 2026-11-27)
**An idea's side is what the idea bets** (`idea_definition.md`): `long`, `short` or `both`, on its own `side:` header
line, written by step 2 and by every step 7 line for every run, boxed or not, and checked by code when the idea file is
written (a missing or unknown value is refused and asked again, as an unknown `profile:` is).
- **One reading for `in_box` and for the ideas taken (B13)** (`target_box.py`, `idea_side`): the idea's own `side:`
  line; else, for an idea written before the line existed, its brief's "long only" or "short only"; else unknown. A
  brief saying "long and short", or with no side line, tells nothing of what one of its ideas bets.
- **Why:** before, both read the brief, and a brief without a side line counted as both sides. In pilot A4 a long box
  took ideas that bet short (032-01.b1 and 032-02.b1, measured in the short direction by step 5) and the short box
  took a "rise continues" idea; `in_box` said true for all of them.
- **The side the book may trade stays the brief's** (step 3, `add_side`: a brief's "long only" or "short only" caps
  every component's forecast, by code). One rule, unchanged: the brief limits what is traded; the idea says what it
  bets; neither is enforced on the other. An idea betting short under a "long only" brief gives a flat book, and its
  turn says `in_box: false` in a long box: visible, not refused.

**Why this cannot leak:** the choice reads finished records (the map, the last portfolio's box reading) before the run
starts; the note, the brief's check and the field read header lines. No bar of the run's data is read.
