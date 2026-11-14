# Try 03: brief to verdict, end to end, three briefs (2026-11-05)

**What ran.** The ideas step with claims written in the judge's terms (five measures, a few lines of pandas per claim), one model call per brief; then the generic judge `steps/judge/judge.py`, code only, on fold A, each symbol the brief names, with the common rule (the claim's own `min_effect`, same sign in 5 of 6 windows, 30 bars minimum in each group, cost 0.15% per round trip). No hand translation anywhere between the brief and the verdict.

**Result.** 30 claims judged. 3 pass, 27 fail, 0 refused.

| Brief | Claims | Pass | What passed |
|---|---|---|---|
| BTC overreaction, 1h | 10 | 1 | a big bar on at least 3x median volume keeps going over 12h: +0.24% mean difference, 185 events, 5 of 6 windows |
| ETH volatility regime and trend, 1d | 9 | 0 | nothing; the closest is a Donchian breakout net of cost with only 17 events |
| Time of week, three pairs, 1h | 11 | 2 | weekend volatility is 64 to 78% of weekday volatility, 6 of 6 windows, all three pairs; the US open hour has 1.3 to 1.5x the volatility, all three pairs |

Honest fails worth noting, because the belief was right and the number was wrong: a big bar raises the next 6h volatility by 1.2x (asked 1.5x), 6 of 6 windows; the CME reopen hour has 1.4x volatility on BTC and ETH (asked 1.3x) but 1.29x on SOL; funding hours have 1.04 to 1.09x (asked 1.10x). The rule is the rule: the number written before the data is the judge. The record keeps the measured effect, so the next brief can be written with the right number.

**What the three passes mean.** Two are volatility filters, not books: they say when to size up or down. One is a tradable belief on BTC: informed flow on extreme volume continues. It passed on one fold, which is the design: one fold, one verdict. It is now a validated claim and the next step of the spine applies to it.

**What the runs told us.**
1. All 30 code blocks ran first time. The format is enough for the model; no claim needed a human.
2. The judge is about 150 lines and claim-agnostic. The claim-specific part is the model's few lines of pandas.
3. The one return pass compares against every other bar with the same direction rule, which is the right baseline for "continues".
4. Four briefs' worth of calendar ideas worked with UTC hours only; no calendar library was needed.
5. Each model run checked its YAML with one command although told not to run code. Harmless, and the check belongs to the pipeline anyway: the judge refuses bad YAML.

**Trial rows.** 30 rows appended to `records/trials.yaml` (plus 2 smoke rows), one per claim measured on market data.

**Proposed try 04: the config and the profit answer.** Take the one validated BTC claim, write its strategy config for the engine, backtest it on fold A with `trading-bot/`, and answer branch 3: profitable enough after cost, or not. That closes the spine once: brief, claim, verdict, config, backtest, profit.
