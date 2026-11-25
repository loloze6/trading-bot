# Night 8 (2026-11-25): one session per market regime, the side free (written before the runs)

**The operator (2026-11-25, about 23:15 Paris):** "250 for the night"; "sessions are per market regime, but not focused
on a side only"; "you do not need to limit yourself, results is the objective". Standing rules: `NIGHT_RULES.md`. What
is new since night 7: 1n (a discovery's ideas rank as follow-ups), 1q and 1t (lines 7.e and 7.g see the profile map,
by profile and side), 1l (a move to flat is never refused by the band). Pilot passed (`PILOT_CHAIN_RUN.md`: 6 of 6);
the map with sides checked after it (line 7.g on night 7's 036-02, `07g_patterns/topic1t_check_run/`: it read the map,
left out the held rebound, named a profile for both ideas, one of them short in "falling agitated"). The pilot's 3
components merged (`night_merge`, e829bf8e50; tests: cards 167, bot 1676 passed).

## Purpose
One question: **does a search aimed at each market regime, its themes answered first, give proven and profitable
specialists in the boxes the portfolio lacks (the short side, choppy agitated), unrelated to what we hold?**
The map before the night (`orchestration/ideas_similarities_check/register/PROFILE_MAP.md`; v1 of the combination,
`orchestration/combine/portfolios/v1/`): of 109 proven and profitable strategies, 92 long only, 16 both, 1 short;
specialists only in "falling agitated, long" (7, one effect) and "rising, long"; "choppy agitated" empty on both sides.

## Sessions
| Session | Run | Regime | Theme (step 1 writes the brief; the expected move stated, no side lock) | Bar | Budget |
|---|---|---|---|---|---|
| A | `night8_fallingcalm_run` | falling calm | In a falling, calm market (a coin down more than 10 % over two months, swinging less than usual), the decline carries on: the more a coin has fallen over the past weeks, the more it keeps falling over the next days. | 1d | 45 USD |
| B | `night8_fallingagitated_run` | falling agitated | In a falling, agitated market, a sharp rally fails: the larger a coin's rise over the past few days, the more of it is given back over the next days. | 1d | 45 USD |
| C | `night8_risingagitated_run` | rising agitated | In a rising, agitated market, an overextended rise gives back part of it: the further a coin has run above its recent average, the more it falls back over the next days. | 1d | 40 USD |
| D | `night8_choppyagitated_run` | choppy agitated | In a choppy, agitated market (no clear trend over two months, swinging more than usual), a coin's move over the past week carries on over the next week. | 1d | 35 USD |
| E | `night8_choppycalm_run` | choppy calm | In a choppy, calm market, a coin at the top of its recent range falls back toward the middle, and a coin at the bottom rises back. | 1d | 35 USD |
| F | `night8_risingcalm_run` | rising calm | In a rising, calm market, a pullback is bought: the more a coin has dipped over the past few days, the more it recovers over the next days. | 1d | 30 USD |
| designer | check-ins (the usage limit), the morning merge and reading | - | - | - | 20 USD reserve |

Each session: `run_brief --theme "<theme>" --run <run> --python <venv> --budget <USD>` on branch `night8-<regime>` from the
working branch, by `NIGHT_RULES.md`. Brief numbers (3e) are not ruled: sessions number from the same list; the
morning merge reports the numbers used twice. The evidence per theme, for the reading: A (night 7: 5 of 5 falling-calm
ideas leaned the idea's way, t 1 to 2, none confirmed), B (the mirror of our only specialist; line 7.g's check proposed
it), C (2 strategies short in that box, both two-sided), D (night 7's control confirmed it 9 times, unrelated to the
held books, not as specialists), E and F (night 7: 0 of 12 choppy ideas confirmed, with many cases).

## Expected outcomes (by the counts)
| # | Outcome | Shown by |
|---|---|---|
| N1 | New specialists fill empty or thin boxes | confirmed and profitable books whose idea names the regime, in a box with at most 3 strategies before the night (the short side; choppy agitated), the nearest held book explaining under 0.5 |
| N2 | Themes answered, specialists not earning | themes found real (an idea on the theme confirmed) but no new book profitable in the target boxes |
| N3 | Themes not real | lines 7.b, 7.c answer "not in the data" on most themes |
| N4 | The machinery fails | a fault: a failed turn, a plan without its profile gate, discoveries taking the turns again (theme ideas under half of each run's first 10 turns), a component not committed |
Also counted per session: its theme's answer; the share of the first 10 turns on the theme; discoveries and the briefs
they became; confirmed and profitable books by box (the box reader, `orchestration/combine/helper/boxes.py`); the spend
on books a held book explains at 0.5 or more. Then, in the morning: v2 of the combination with the night's books, and
the new books on the unseen coins (1u).

## During the night (the designer's watch)
- **23:55 Paris, a machinery fault found by session E (N4), shared by every session:** since night 7 the catalogue's
  component row of `DonchianBreakoutComponent` was stale (only `period`, `scaling_factor`): a night 7 build's `with_row`
  had replaced the first line starting with the class's name, the class's line in the misleading-names table. Tonight
  step 3's settings check refused `source`, a setting the class has; the components step rebuilt the class twice; E's
  two first ideas ended "missing components" (4.58 USD spent before its loop stopped). E's fix (5ac0d5d770, checked
  by the designer): `with_row` replaces a row only inside "Component rows" (a new test fails on the old rule); the
  catalogue's two lines back in their tables; the class back to the night's start (same value on 7,600 of 7,600 bars).
  Taken onto the working branch (the three files; components and step 3 tests pass) and given to the 5 other sessions
  to take between two turns, so none rebuilds the class.

## Reading
(written in the morning)
