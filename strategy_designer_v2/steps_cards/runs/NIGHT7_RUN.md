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

**The comparison, fixed now:** each new-code run cut at its first 25 USD (`loop.jsonl`'s spend) against its control,
theme by theme, on: confirmed ideas; confirmed books earning on their own (step 6's Sharpe above 0); of those, unrelated
to the portfolio's 20 (correlation under 0.5): the portfolio candidates; follow-ups on the brief's theme (by
`common/theme.md`); the brief's answer (real, not real, open). **The change goes the good way** if the new code gives
at least as many portfolio candidates in total and more ideas on the theme; it is **not useful** if it gives fewer
candidates and no clearer answers. Four themes are few: the reading says so, and gives the counts.
The control branches are read in place, not merged.

## Reading (the morning)
To be written after the merge: the outcome, the counts, the step back.
