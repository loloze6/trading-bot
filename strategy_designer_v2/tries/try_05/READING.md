# Try 05: branch 2 and the next idea (2026-11-05)

**What ran.** The analyst step (`steps/analyst/PROMPT.md`): one model call per finished run, reading the run's record (every claim with its code, the judge's numbers per window and symbol, the profit answer). Two questions: what did we see, what one claim runs next. Then the judge on the proposed claim, no hand in between.

**BTC overreaction run.** Nine observations, each with its number. Next claim: none. The analyst's reason: reversion failed in every form tried, the one pass (continuation on heavy volume) did not pay, and any follow-up would only move a threshold or a horizon, which the rules forbid. The brief's answer is no. A brief can end with no, and this one did.

**Time-of-week run.** Ten observations. Two claims held, both about volatility (weekend 0.64 to 0.78 of weekday; the US open hour 1.3 to 1.5x), three nearly held (CME reopen, funding hours, a US-open selloff on SOL only), all eight return claims failed. Next claim: continuation from the US open hour, 6 bars, min effect 0.2%. Judged on the three symbols: fail (+0.07%, +0.08%, +0.02%). Honest, and recorded.

**The loop, closed once.** Brief, claims, verdicts, profit answer, observations, next claim, verdict. The record of each step is a file the next step reads. Nothing in it was touched by hand. The model never cites a number it did not read from the judge's file; the judge never trusts a claim it did not measure.

**What this try showed.**
1. The analyst's observations were correct against the files in both runs, and its "none" was the right call.
2. A proposed claim is a claim like any other: same format, same judge, same ledger row. No special path.
3. The two validated volatility filters have no profit answer, because a filter is not a book. The spine needs one line: a validated filter waits for a return claim to attach to, and the record keeps it on the shelf.

**What is still missing for "runs on its own".** The model calls here went through this session's agent tool. On the PC they are one SDK call each, with the same prompt and files. One short script that runs the steps in order, brief by brief, is the last piece: try 06.
