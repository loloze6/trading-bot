# Exercises 27 and 28 (the same file is in exercise_27)

**Changes** (approved: "Go").
- **Prompt:** "Holding is the coin's mean return over all the test's windows together, never a mean over a single window: such a mean contains the price moves that set the forecast, and biases the result." Found by the full-data run: the per-window mean gives t = -2.60 on random walks (`../../FULL_DATA_RUN.md`).
- **Default data:** BTC, ETH, LTC, XMR, XRP, ZEC (the cached coins with data in all four folds), daily bars, folds A to D (24 windows). A brief's header still overrides it (brief 001 keeps BTC, ETH, BNB).

The 13 fixed ideas, opus, two runs side by side. Cost 0.83 and 0.78 USD. No code retry.

| | Exercise 27 | Exercise 28 |
|---|---|---|
| Outcomes | 5 plans, 2 untestable, 6 missing-components | the same, idea by idea |
| Holding reference | the coin's mean over all 24 windows, 5 of 5 | 4 of 5; 001-03 compares extreme with neutral bars (also unbiased) |
| Near-zero rejects | 0 | 0 |
| RSI-extreme plans with exponent 3 | 2 of 2 | 2 of 2 |

- **003-07 (quiet hours)** is untestable in both runs (missing-components in exercises 25 and 26). Both are refusals with the situation replaced; untestable is the closer reading: on daily bars the hours are not in the data.
- **One setting differs:** 003-01 ("sharp" up move on low volume) uses `signed_power` exponent 3 in one run and 2 in the other. A minor deviation; no outcome depends on it.

**Status.** Two clean runs in a row: "done when" is met.
