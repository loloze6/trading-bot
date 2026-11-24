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

## Reading (the morning)
To be written after the merge: the outcome, the counts, the step back.
