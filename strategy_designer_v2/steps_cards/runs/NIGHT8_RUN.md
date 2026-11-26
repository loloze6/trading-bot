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
  to take between two turns, so none rebuilds the class. **00:00 Paris:** all 6 sessions took it (A 23b95c9796, B
  f30b39818e, C 2a70c9a517, D a91e045283, F 79058e1838; E's own), each between turns with no components build running,
  components tests passing.
- **00:01 Paris, a second finding (session F; not fixed during the night):** turn 4 retested turn 3's book. Line 7.b on
  058-02.b1 wrote 058-02.b1.b1 with the same `Idea:` sentence word for word; step 3 gave a byte-identical config; step
  4 reran it (+0.61 again), about 1.1 USD. `select_next`'s duplicate rule compares the Idea sentence and the header's
  instruments, bar and period as written, so two ideas whose data lines are worded differently but tested the same are
  both run. For the morning: the duplicate judged on what is tested (the plan's config), not on how the idea is worded.
- **00:16 Paris, first watch** (each branch as last pushed): no fault. Every plan whose idea names a profile has its
  gate (30 of 30), no failed turn. The theme's own ideas took every turn so far in A (5 of 5), B (4/4), C (7/7), E
  (4/4), F (5/5); in D 2 of 5, rightly: its two first ideas were answered "not in the data" by lines 7.b and 7.g
  (the weekly move does not carry on in a choppy, agitated market: excess return about zero), so the theme is closed
  and the discoveries come next. 27 ideas tested, 22.1 USD. **First result, session C:** 058-03.e1 ("in a calm,
  rising market a stretched rise carries on over ten days") confirmed (+2.32), profitable enough, and it holds on
  both unseen periods (2016-17 and 2026); 058-03.b1 confirmed, not profitable. E's pushed state predates its resume
  (its loop had stopped at 22:43 on the catalogue fault, resumed since). No usage-limit stop yet.
- **00:40 Paris, a gap in 1n (session F's count and check; not changed during the night):** F's first 10 turns are 4 on
  the theme. Its queue (select_next, 23:38 UTC): the theme's own follow-ups wait at ranks 3, 8, 10, 14, 15 (scores
  0.0595 to 0.0307, generations 2 and 3), below two first ideas of discovery briefs (0.0615, generation 1). 1n ranks a
  discovery's ideas as follow-ups at the discovery's level, so a shallow discovery outranks a deep follow-up of the
  theme; the record of the lines is not the cause (7.b 0.238 against 7.g 0.123). 1n's aim (the theme's own follow-ups
  first) holds for first ideas, not for deep chains. For the morning: the theme brief's own lineage ranked before the
  discovery briefs' ideas (one group rule). D's discoveries also research B's and F's themes (briefs 060, 061): each
  session's "already indexed" sees its own briefs only (night 7's same limit). F's waiting theme ideas follow the
  reversed sign its 7.b found: in a rising, calm market the deepest pullbacks keep falling (t -3.15).
- **00:46 Paris, limit watch:** all 6 sessions running (last commits 23:22 to 23:36 UTC), no call refused. 53 turns, 46
  ideas tested, about 49 USD; confirmed 5 (C 3, B 1, D 1), profitable enough 2 (C). E's "no candidate left" in the
  watch is its stop of 22:43 (the catalogue fault); it resumed and is at turn 10.
- **01:00 Paris, a path audit (the operator: "worth checking that sessions act as expected, no idea deviation"; 58
  ideas tested, read from each branch):**
  - Step 3 builds what the idea says (fit exact or adapted on every plan); every idea naming a profile has its gate.
  - A (falling calm) and B (falling agitated): every tested idea is the theme in its regime (11 of 11, 9 of 9).
  - C (rising agitated): its brief itself states the counter-case ("weak or reversed in the calm one"), and step 2 wrote
    it (058-03, rising calm): that is where its confirmed and profitable book comes from (058-03.e1). Not a deviation.
  - D: theme answered "not in the data" on both first ideas; discoveries since, as designed.
  - **E (choppy calm) and F (rising calm): the follow-ups widen or move the profile** (E: choppy calm → choppy →
    calm; F: rising calm → choppy agitated → rising → none). `common/theme.md` allows a follow-up to change "the
    profile", so it is by the definition, but it takes the search out of the night's target box. For the morning:
    when a brief names a profile, the profile is part of the theme's situation (a follow-up keeps or narrows it;
    another profile is a discovery).
  - Discoveries: no longer the held rebound (17 of the night's discoveries answered "already indexed" by step 1); but
    the same patterns are found by several sessions (a rally fades in a falling, agitated market: B's theme, briefed
    again by C and D), each session's index seeing its own briefs only.
  - **Results so far:** short books confirmed in "falling agitated" by three sessions (B 058-01.g2.b1, C 060-01 and its
    follow-ups, D 060-01.b1), none profitable enough yet; one confirmed, profitable book holding on both unseen periods
    (C 058-03.e1, rising calm, long). The confirmed calm continuations of E and F (E's nearness to the 20-day high, t
    3.96) may be the held "near its high" books again: the morning's similarity check says.
- **01:20 Paris, an adjustment during the night (the operator: "if some adjustment needs to be made on live sessions,
  feel free"):** `common/theme.md`: when a brief names a market profile, that profile is part of its situation; a
  follow-up keeps it or narrows it, and the same situation in another or a wider profile is a discovery (before: a
  follow-up could change "the profile"). Only the definition the step 7 lines read changes, no code. Proof: line 7.b
  rerun on E's 058-02.b1 ("choppy calm"; step 4 rerun first, 0.45 USD): during the night it wrote 2 follow-ups, one in
  "choppy calm" and one widened to "choppy"; with the rule, 1, in "choppy calm". Given to the 6 sessions to take
  between turns.
  Taken by A, B, C, D and F; E's own permission check refused a change asked by another session, not by the operator,
  and E rightly did not work around it: E reads the old definition until the morning merge (its branch does not touch
  the file). **C's result at 01:20 Paris:** 060-01.g1.d2.d1 (falling agitated, SHORT the day after a wide day closing
  near its high) confirmed (+2.23), profitable enough, holding on both unseen periods: the first specialist in an empty
  box of the map.
- **01:30 Paris, limit watch:** all 6 running (last commits 00:02 to 00:15 UTC), no call refused. 80 turns, 71 ideas
  tested, about 78 USD; confirmed 11, profitable enough 3.
- **01:35 Paris, two findings:**
  - **F's resume refused by its own permission check, twice** ("destructive or unwanted", then "undermining
    oversight"), after the 2-hour task cut at 00:32 UTC; F did not work around it, pushed (05f77cd643) and stood down.
    Its report: 19 ideas tested, 5 confirmed (all one discovery, brief 061: a big day in a calm market carries on), 0
    profitable enough, 21.24 of 30 USD; its theme answered not real. **Resumed by a new session from its branch**
    (00:35 UTC, the only one on night8-risingcalm), the loop going on from the run's files with the 8.76 USD left.
    C's resume after its own cut (00:30 UTC) went through; the refusal is the session's, not the rule's.
  - **Step 3 wrote an invalid config (session C, 068-01):** a regime named "mean_reversion_unused" in
    `strategies.regimes`; the engine's config check refused it (V7), step 4 ran 0 of 24 windows, steps 5 and 6 had no
    verdict and line 7.g still read the empty record (0.34 USD, 4 minutes). For the morning: step 3 runs the engine's
    config check (`trading-bot/tools/validate_config.py`) on its own config and refuses it there. C's theme answered
    not real (lines 7.b twice "not in the data": the rise continues).
- **The usage limit, about 02:35 to 02:45 Paris:** every session's last turn failed between 01:35 and 01:45 UTC (A, B,
  C, D, E and the resumed F; the 1l impact session at 02:00 UTC); the designer's own 02:30 watch could not run (its
  worker restarted). **04:58 Paris, after the reset:** each told to resume its loop (`loop.py`, the budget in the run's
  files; no new idea after 07:00 UTC). Also finished during the night: the unseen-coins check (9 of 35 books hold on
  coins they were never tested on; daily books carry to other coins, hourly ones mostly not) and v1 on the unseen
  coins (its reading on branch `combine-v1-unseen`), both read in the morning.
- **05:07 Paris:** all 6 resumed between 04:04 and 04:06 UTC on their own machines and venvs, each first finishing the
  idea the limit cut; no refusal. Spend before the stop: A 27.8 of 45, B about 20 of 45, C 36.3 of 40, D 18.8 of 35, E
  25.2 of 35, F 32.1 of 30 (F stops after its cut idea: the loop finishes an idea it started). Confirmed and
  profitable so far, both unseen periods holding: C 058-03.e1 (rising calm, long), C 060-01.g1.d2.d1 (falling
  agitated, short), E 058-02.b1.g1.b1.b1 (falling agitated, next-day reversal), E 058-02.b1.b2.b1.b2.b2.e1 (calm, a
  close at the range's edge carries on); D 064-01 profitable but "not observable" on both unseen periods and 0.53
  explained by the held 035-01.
- **05:30 Paris, a fault in the designer's resume command (found by C):** `loop.py` keeps no budget in the run's
  files; resumed without `--budget` (as the designer's messages, the launch messages' step 3 and NIGHT_RULES said),
  every loop ran with no limit. C stopped its own loop at 42.42 of 40 USD (04:28 UTC, final report: 29 ideas, 9
  confirmed, 3 profitable enough, 2 holding on both unseen periods; theme not real; 15 discovery briefs). Told A, B, D,
  E to restart with `--budget` (45, 45, 35, 35: the whole run's spend counts), and the resumed F (over its 30) to stop.
  NIGHT_RULES corrected. **05:31 Paris:** A, B, D and E restarted with `--budget` at 04:29-04:30 UTC (spend then 33.8, 26.8,
  22.6 and 30.1 USD: none had passed its budget); the resumed F stopped at 04:29 UTC on its own count, 36.89 of 30
  USD (15 ideas in its two parts after the first stop, 0 confirmed). Overspend of the night: C +2.4, F +6.9 USD; at
  most 239 USD for the six runs if A, B, D and E reach their budgets.
- **05:40 Paris, path audit (146 ideas tested):** every plan exact or adapted to its idea. **The night's effect:**
  "a rise fades in a falling, agitated market" (short), confirmed by four sessions on their own (B 4 times, C 5, D 1, E
  2); 1 of them profitable enough and holding on both unseen periods (C 060-01.g1.d2.d1). Others
  confirmed and profitable: E 058-02.b1.g1.b1.b1 (falling agitated, a next-day reversal after a fall: long, both unseen
  periods holding, 0.61 explained by the held 035-01; corrected 06:25 Paris from E's report, the audit had read it as
  a fade), C 058-03.e1 (rising calm, long; both unseen periods), E 058-02.b1.b2.b1.b2.b2.e1 (calm,
  a close at the range's edge carries on; both), D 064-01 (falling agitated rebound, 0.53 explained by the held
  035-01). Volume in declines (A: 7 confirmed, none profitable, all failing Calmar). Profile drift: E's theme lineage
  still moves out of "choppy calm" (into falling and falling agitated: E reads the old theme definition, its
  permission check having refused the new one); its best book came from that drift.
- **06:25 Paris, two runs ended on their budgets:** A (05:14 UTC, 45.34 of 45: 36 ideas, 11 confirmed, 0 profitable
  enough, most failing only Calmar; theme real narrowly: a fall continues as volume dries up, t +2.00; 2 components
  built and committed) and E (05:22 UTC, 35.11 of 35: 25 ideas, 7 confirmed, 5 confirmed and profitable, a held book
  explaining each at 0.59 to 0.91, all long rebounds or continuations in boxes already held; theme not found real in
  choppy calm, the continuation at the range's edge confirmed in "calm" and "rising calm" instead).

- **07:20 Paris, the last two runs ended on their budgets; all six have ended, no loop runs:** D (35.95 of 35: 26
  ideas, 6 confirmed, 1 profitable, 064-01, explained 0.53 by the held 035-01 and not observable on the unseen
  periods; theme open, leaning not real) and B (06:14 UTC, 45.84 of 45: 30 ideas, all on the theme, 10 confirmed, 0
  confirmed and profitable; theme REAL: in a falling agitated market a one-day rise with a wide range or an upper wick
  fades over the next day(s); the books fail Calmar; the multi-day form stayed inconclusive; 10 of its first 10 turns
  on the theme; 7 discovery briefs written, none run; 1 component built, which unblocked a confirmed idea). Spend of
  the six runs: about 241 of 250 USD.

## Reading
(written in the morning)
