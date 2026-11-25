# Night 7 (2026-11-24): four briefs aimed at market profiles, under topics 49 and 50 (written before the runs)

**The operator (2026-11-24, about 00:15 Paris):** "So I will go off, time to prepare for the night." The standing rules
are `NIGHT_RULES.md` (first use); this file says what is new.

## Purpose
The first night with ideas that name their market profile (topic 49) and follow-ups that stay on their brief's theme,
with discoveries turned into briefs (topic 50). One question: **do briefs aimed at market profiles the portfolio has no
specialist in give confirmed books that earn on their own and are unrelated to the portfolio's 20?** The profiles
chosen are those of 2026, where the portfolio failed (P4: choppy, slowly falling): choppy and falling markets, on both
sides.

## Expected outcomes (one of them, by the counts)
| # | Outcome | What would show it |
|---|---|---|
| N1 | A profile specialist enters the portfolio's candidates | a confirmed book naming a profile, step 6's Sharpe above 0, correlation under 0.5 with the 20 (P1's rule, `topics/44_review/p7_night6_candidates.py`) |
| N2 | Themes answered real, books not earning | confirmed ideas on the theme, none earning on its own (or all close to held books) |
| N3 | Themes answered not real; the search moves to discoveries | lines 7.b/7.c answer "not in the data"; discoveries become briefs and carry the night |
| N4 | The new machinery fails | a profile not built, a discovery not turned into a brief, a merge stopped: the defect named |

Also counted, per brief: its answer (real, not real, open), the discoveries and the briefs they became, the share of
ideas naming a profile, and how many confirmed books are profile specialists.

## Sessions
| Session | Run | Theme (step 1 writes the brief) | Bar | Budget (model calls) |
|---|---|---|---|---|
| 1 | `night7_rangefail_run` | In a choppy market (a coin with no clear trend over the past two months), a close beyond its recent range fails: the coin comes back inside the range over the next days, the more so the further it broke out. | 1d | 35 USD |
| 2 | `night7_chopreversal_run` | In a choppy, agitated market, a coin's move over the past week is given back over the next week: with no trend to carry it, a large swing is noise that reverses. | 1d | 35 USD |
| 3 | `night7_steadydecline_run` | In a falling, calm market (a steady decline without panic), the decline carries on: the more a coin has fallen over the past weeks, the more it keeps falling over the next days, as holders sell into every pause. | 1d | 35 USD |
| 4 | `night7_panic_run` | In a falling, agitated market, does a coin's new low over the past month lead to more falling, as forced selling feeds itself, or to a rebound, as sellers run out? | 1d | 35 USD |
| designer | the night 6 replay of `night_merge` (3g's proof); check-ins; the morning merge and reading | - | - | 0 USD |

Each session: `run_brief --theme` with its theme and budget, on branch `night7-<name>` from the working branch
(`ccr-6624e33e-aakrpv`), by `NIGHT_RULES.md`. Brief numbers (3e) are not yet ruled: the sessions will number from the
same list, so the morning merge reports the numbers used twice and the reading names briefs by their full file name.

## The control arm (added 2026-11-25 about 00:30 Paris, before its runs)
**The operator (about 00:30 Paris):** "You even have until 250 to spend ... In the morning we will look at results and
advise if such major change is useful and going into the good direction. If not we might reverse." To judge the change
by evidence, the same four themes also run on the code before topics 49 and 50 were built (`bf8dd5bff2`: no profile
line, no theme rule, no discoveries; P9 and the folds rule as today): 4 sessions, 25 USD each (night total 240 USD).

| Session | Run | Branch | Theme | Budget |
|---|---|---|---|---|
| C1 | `night7c_rangefail_run` | `night7c-rangefail` | as session 1 | 25 USD |
| C2 | `night7c_chopreversal_run` | `night7c-chopreversal` | as session 2 | 25 USD |
| C3 | `night7c_steadydecline_run` | `night7c-steadydecline` | as session 3 | 25 USD |
| C4 | `night7c_panic_run` | `night7c-panic` | as session 4 | 25 USD |

**The comparison, fixed now (revised 2026-11-25 about 00:45 Paris, before any result, after the operator asked
whether the control is really useful):** each new-code run cut at its first 25 USD (`loop.jsonl`'s spend) against its
control, theme by theme. Judged on what has enough cases to show a difference:
- follow-ups on the brief's theme (by `common/theme.md`), as a share of the ideas written;
- the spend on ideas re-finding the portfolio's effects (nearest held book explains 0.5 or more);
- each brief's answer (real, not real, open);
- for ideas naming a profile: the share of their days in a position inside it, against the control's reading of the
  same words.
Counted but not judged: portfolio candidates (night 6 found 2 for 140 USD; at 25 USD a theme, 0 or 1 per arm is
chance). **The change goes the good way** if the new code keeps more follow-ups on the theme, answers more themes, and
does not spend more on the portfolio's effects; whether it finds better strategies needs several nights and their
unseen test, and the reading says so.
The control branches are read in place, not merged.

## During the night (the designer's watch)
- **00:35 Paris, first watch** (a script reads each pushed branch: profile lines, the profile gate in every plan, theme
  marks, discoveries and their briefs, failures): no defect. The 4 new-code runs: every idea from a brief names a
  profile; the 3 plans whose idea names one have the gate, none without; lines 7.e/7.g mark discoveries and leave ideas
  on the theme unmarked (read as on the theme, as intended); 3 discoveries already turned into briefs.
- **A gap between topic 50's card and the code:** the card says P9 still pushes copies of held books down for a brief
  from a discovery; it does not: P9 weighs only follow-ups of confirmed ideas, and a brief's first ideas are always group
  1. Of the first 5 discoveries, 3 are the next-day rebound after a fall (an effect the portfolio holds); session 2 made
  it brief 033. Not changed during the night (the sessions run the code they cloned); the reading counts the spend on
  such briefs, and the fix is proposed in the morning.

- **00:46 Paris:** the 4 new-code sessions alive and progressing, no fault (steadydecline and panic 5 turns each, 3
  confirmed in steadydecline; 11 discoveries turned into briefs). **The 4 control sessions had never started:** the
  cloud refused the short commit id (`bf8dd5bff2`: "ref not found"), nothing spent; archived and relaunched at 00:48
  Paris with the full id, all four running. They start about 30 minutes after the new-code sessions; the comparison at
  equal spend is not affected.
- **00:50 Paris, 3g proven:** night 6's merge replayed with `night_merge` (its card): the components file and the
  register's pages identical to the hand repair, the catalogue right where the hand repair was wrong. It will merge
  night 7.

- **01:40 Paris watch:** no fault on the 8 branches (every plan has the profile gate exactly when its idea names a
  profile); all 8 sessions committed within the last 20 minutes. The designer's container restarted at about 01:32
  Paris: nothing lost (tree clean, last commit in place). New code, about 75 minutes in: 54 ideas tested, 20 confirmed,
  5 profitable enough, 53 USD; 31 discoveries made into briefs (panic alone 13). Control, about 45 minutes in: 25 tested,
  1 confirmed, 3 profitable enough, 26 USD.

- **The usage limit stopped the whole night at about 02:10 Paris:** all 8 sessions on the account's 5-hour limit
  (reset 05:20 Paris); none could schedule its wake-up, since its own model calls were refused too. The designer's
  check-ins of 02:30, 03:30 and 04:30 Paris did not run (its worker restarted several times and its triggers waited).
  State at the stop: new code 74 ideas tested, 30 confirmed, 10 profitable enough, 74 USD; control 47 tested, 12
  confirmed, 5 profitable enough, 54 USD. **05:35 Paris:** the watch: no fault; all 8 sessions told to resume (their
  branch first if their machine was replaced), the time rule unchanged (no new idea after 08:00 Paris). About 2.5 hours
  of the night remain: the budgets will not be spent.

- **05:45 Paris:** all 8 sessions resumed at 05:40-05:42 Paris, each on its own branch and venv (their machines were not
  replaced), each finishing the idea the limit cut first. Spent before the stop: new code 17.9, 20.7, 23.0, about 23
  USD; control 12.4 to 18.1 USD. **A commit gap:** two sessions had built components without committing the classes
  under `trading-bot/` (session 3: 5 components, now committed by itself; control C2: 1, asked to commit). The other 6
  branches have every built class in their components file (checked). Without it the morning merge would have carried
  build records for classes that do not exist.

- **05:56 Paris:** the 8 sessions confirmed running (new code committed within 5 minutes; controls at their resume, they
  commit hourly); control C2 committed its missing component class (checked on its branch).

- **06:35 Paris watch:** no fault; the 4 new-code runs and control C3 moving (commits within 10 minutes); controls C1,
  C2, C4 ended on their budgets (reports received). The "already indexed" answer works in the runs: two repeated
  rebound discoveries were not made into briefs (chopreversal, panic). It cannot see other sessions' briefs: rangefail
  made the same rebound its brief 036 (each branch indexes its own briefs; the merge reports such repeats only by number).

## Reading (the morning)
To be written after the merge: the outcome, the counts, the step back.
