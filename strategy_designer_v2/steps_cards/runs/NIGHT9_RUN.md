# Night 9 (2026-11-26): data-first briefs aimed at the empty boxes (written before the runs)

**The operator (2026-11-26, about 23:00 Paris):** "this night would be launched soon ... continue research workflow
during the night (300 budget) with research workflow completion around 9am tomorrow morning"; earlier the same day, in
the night 8 review: B2 option a ("a run starts from a target box, explored in the data, not from a theme the designer
writes"). Standing rules: `NIGHT_RULES.md`.

**Nothing changed in the steps since night 8** (the theme rule of `common/theme.md` was taken by 5 sessions during
night 8; `night_merge`'s fix and the combination's judge run in the morning only): no pilot is needed (NIGHT_RULES,
before the night, 3). B2's own entry (a run started from a box) is not built yet; tonight takes its idea with what
exists: each session starts from **briefs written by the analysts from the data** (night 8's line 7.g discoveries,
written as briefs and never run), chosen for the boxes the portfolio lacks. No brief is written by the designer.

## Purpose
One question: **do briefs found in the data, aimed at the empty boxes (choppy agitated; the short side in falling calm
markets), give confirmed and profitable specialists there, where the designer's themes of night 8 gave none?**
The map before the night (combination v2b, 10 strategies): choppy agitated empty on both sides; falling calm short 3
strategies, none a specialist; the one short specialist is in falling agitated (night 8, C's 060-01.g1.d2.d1).

## Sessions
| Session | Run | Target box | Briefs (each a night 8 discovery, its file in `01_brief/<night 8 run>/briefs/`) | Budget |
|---|---|---|---|---|
| A | `night9_chopagishort_run` | choppy agitated, short | `night8_risingagitated_run/briefs/061_choppy-agitated-high-close-fades.md` | 42 USD |
| B | `night9_chopdeep_run` | choppy, short | `night8_risingagitated_run/briefs/072_choppy-deep-below-high-falls.md` | 42 USD |
| C | `night9_chopmonth_run` | choppy, both sides | `night8_choppyagitated_run/briefs/067_choppy-market-monthly-move-continues.md`, `night8_choppycalm_run/briefs/064_choppy-market-up-days-carry-one-way.md` | 42 USD |
| D | `night9_chopstretch_run` | choppy, both sides | `night8_risingagitated_run/briefs/067_choppy-average-stretch-carries-forward.md` | 42 USD |
| E | `night9_fallcalmfade_run` | falling calm, short | `night8_risingagitated_run/briefs/070_falling-calm-run-break-fade.md`, `night8_risingcalm_run/briefs/064_falling-calm-scaled-rallies-fade.md` | 42 USD |
| F | `night9_fallcalmwide_run` | falling calm, short | `night8_choppycalm_run/briefs/060_falling-calm-wide-high-close-fade.md`, `night8_choppycalm_run/briefs/061_falling-calm-rally-next-day-fade.md` | 42 USD |
| designer | check-ins (the usage limit), the coin-data session, the morning merge and reading | - | - | 48 USD reserve |
| data | `data-coins` (no model call for research): the 20 coins of the coin card fetched from Kraken's archive, daily | - | - | 0 USD of research calls |

Each research session: on branch `night9-<name>` from the working branch; for a session with two briefs, the second
brief is added first with a tiny budget (`run_brief <brief 2> --budget 0.01`: step 2 runs, the loop does not start),
then `run_brief <brief 1> --budget 42` starts the loop on both briefs' ideas (one queue, one score). No new idea after
07:00 UTC (08:00 Paris); the runs end by about 08:30 Paris; the morning merge and reading follow.

## Expected outcomes (by the counts)
| # | Outcome | Shown by |
|---|---|---|
| N1 | Specialists in the target boxes | a confirmed and profitable strategy whose positions sit in its target box (10 % or more of its days, by `boxes.py`), the nearest held strategy explaining under 0.5 |
| N2 | Effects real, strategies not profitable | confirmed in the target box, none profitable (Calmar, as night 8's falling markets) |
| N3 | Not real | lines 7.b and 7.g answer "not in the data" on most briefs: data-first briefs do no better than night 8's themes |
| N4 | The machinery fails | a failed turn, a resume without `--budget`, a component not committed |
Also counted: each brief's answer and the turn and spend at which it was answered; the share of first ideas confirmed
(night 8's designer themes: brief first ideas confirmed 9 % of the time, 1g); the confirmed and profitable strategies by
box; the spend after each brief was answered.

## During the night (the designer's watch)
(written during the night)

## Reading
(written in the morning)
