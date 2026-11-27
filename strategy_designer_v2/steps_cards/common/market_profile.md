What a market profile is (the operator, 2026-11-24; topic 49). Read by steps 1, 2, 3 and 7; step 3's code builds it.

**A market profile is the kind of market a coin is in, read from its own recent bars: which way it has been going, and
how much it has been swinging.** Traders use it to say "this works in a rising, calm market" or "only in a falling,
agitated one". An idea that names a profile says where its effect lives; a strategy built from it holds positions only
in that profile.

**Its two elements, both read on the coin's own bars at a bar's close** (each coin is tested on its own bars only:
`idea_definition.md`):
- **The trend:** the coin's return over the last 60 days.
  - **rising:** above +10 %;
  - **falling:** below -10 %;
  - **choppy:** between the two.
- **The agitation:** the coin's swing over the last 30 days (the standard deviation of its daily returns) against its
  swing over the past year.
  - **agitated:** above the past year's median (more swinging than usual for this coin);
  - **calm:** at or below it.

**The six profiles:** rising calm, rising agitated, choppy calm, choppy agitated, falling calm, falling agitated.

**When it is known:** at a bar's close, from that bar and the bars before it only. Times are in days, so a profile means
the same on daily and on hourly bars (60 days is 1,440 hourly bars).

**How often each profile occurs** (the six core coins together, 2016 to 2026, measured with the six coins' average on
2026-11-24, `topics/44_review/p10_map.py`): rising calm 31 %, rising agitated 14 %, choppy calm 22 %, choppy agitated 3 %,
falling calm 17 %, falling agitated 11 %. A coin's own profile matches that average's on 46 to 63 % of days (its trend
on 61 to 75 %): coins move together, but not always in the same profile.

**Terms built on it:**
- **An idea's profile:** the profile an idea names as the place its effect lives ("in a falling, agitated market, a
  sharp one-day fall rebounds over the next two days"). At most one. It names only what the idea's theory implies: its
  trend and its agitation (one of the six profiles), or its trend only ("in a choppy market": calm or agitated), or its
  agitation only ("in an agitated market": any trend). An idea that names none acts in every profile.
- **A profile specialist:** a strategy whose positions are all in one profile: the book of an idea that names its
  profile, built with that profile as its regime (`forecast.md`: a regime limits where a position exists; inside it
  the forecast is graded).
- **A strategy's side:** long when at least 90 % of its coin-days in a position are long, short when at least 90 % are
  short, both otherwise. Read from its backtest's positions when it enters the similarity register, and kept there
  (`books.json`, field `side`; 2026-11-25, next steps 1t).
- **A box:** a profile and a side (long or short): twelve boxes. **A strategy's presence in a box:** the share of its
  coin-days in a position that fall in that box (the coin's own profile that day, the position's sign). **Its times
  the market:** that presence divided by the market's own share of the profile over the same coins and dates (about
  1: it does not choose that market; well above 1: it does). Used by the combination step
  (`orchestration/combine/card.md`, 2026-11-25).
- **The profile map:** the proven and profitable strategies (step 5 confirmed, step 6 profitable enough), by profile
  and side: twelve cells (six profiles, long or short), and the strategies acting in every profile.
  - **A cell holds** the specialists whose idea names a profile that holds that cell ("rising" holds rising calm and
    rising agitated; "agitated" holds the three agitated profiles), on their side (a "both" strategy on each side),
    each with its idea. They are placed by the profile their idea names because that is where they trade: step 3's
    code keeps the book flat outside it, and the positions confirm it: after 1l, every day outside is within the
    idea's horizon after the profile ended (2026-11-25: 034-02 "rising" 94 % inside, 6 % within its 5 days, 0 other).
  - **Strategies acting in every profile** (their idea names none) are counted by side, not placed in cells.
  - **Kept by code:** `orchestration/ideas_similarities_check/register/PROFILE_MAP.md`, rewritten each time a book enters
    the register, and after a night's merge. Read by lines 7.e and 7.g: a discovery is looked for where the map is
    empty or thin, by profile and by side. A filled cell is a profile and side some strategy specialises in; an empty
    cell is a place no strategy acts in on purpose: a target for the next briefs.
  - **A run's target box** (`target_box.md`, 2026-11-27) is chosen from the map, counting only the strategies whose
    idea names the box's profile exactly (a cell here also holds those whose idea names a wider profile).
  - **Not yet in it:** the boxes where the strategies acting in every profile really trade (their presence by box,
    above); the combination step reads them first. Whether a profile reads the market rightly is topic 54.

**How step 3 builds a profile.** An idea's profile is a line of its own (`profile: falling agitated`, `profile: choppy`); step 3's code,
not the model, adds it to the config, the same way for every idea (`03_test_plan/helper/make_test_plan.py`,
`add_profile`). The model writes the idea's forecast as if the profile were not there; the code then keeps the book flat
on every bar outside the profile.

| Element | Component (existing) | Settings, in days (converted to bars) | In the profile when |
|---|---|---|---|
| The trend | `PriceEvolutionComponent` | `period` 60 days, `scaling_factor` 1 (the 60-day return, in percent) | rising: above +10; choppy: from -10 to +10; falling: below -10 |
| The agitation | `VolatilityPercentileRegimeComponent` | `vol_period` 30 days, `lookback_period` 365 days, `smooth_period` 1 (no smoothing): the share of the past year's 30-day swings at or below today's | agitated: above 0.5; calm: 0.5 or below |

An element the idea does not name is not built. Each condition the bar does not meet is a veto of the regime detector that sends the bar to a regime with no position;
inside the profile the config's own regimes and forecast apply unchanged. On hourly bars the swing is that of hourly
returns over the same 30 days.

**Why this cannot leak:** both elements use closes up to the bar being decided; the past year's median uses that year
only.
