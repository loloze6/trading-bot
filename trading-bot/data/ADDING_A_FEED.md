# Adding a new data feed

## Two feed types

| Type | When to use | Template to copy |
|---|---|---|
| **Global** | One value per timestamp, no symbol (e.g. Fear & Greed, macro index) | `fear_greed_fetcher.py` |
| **Per-symbol** | One value per symbol per timestamp (e.g. funding rate, open interest) | `funding_rate_fetcher.py` |

---

## Step 1 — Create the fetcher file

Copy the appropriate template into `data/fetchers/your_feed_fetcher.py`.
Implement exactly two methods:

```python
class YourFeedFetcher(BaseFetcher):

    def cache_key(self, symbol: str) -> str:
        # Unique CSV filename stem — no spaces, no slashes
        # Global:     return 'your_feed_daily'
        # Per-symbol: return f'{symbol}_your_feed_1h'
        ...

    def _fetch_remote(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        # Fetch data from your source for the given window.
        # Must return a DataFrame with AT LEAST these columns:
        #   timestamp  (datetime, UTC, no timezone)
        #   your_column_name  (float)
        # Return pd.DataFrame() on failure — do not raise.
        ...
```

Optional overrides (only if needed):

```python
    expected_gap_tolerance: float = 2.0   # raise above 1.5 for feeds with natural gaps
                                           # (e.g. weekends, 8h intervals)
```

---

## Step 2 — Declare the feed's causality window (REQUIRED)

**Every feed must declare `window_seconds`: how far past its own `timestamp`
row its value aggregates.** This is not optional and has no default —
`DataManager.register_feed()` raises if it is omitted. It is enforced at the
merge boundary (`_merge_asof_with_causality_guard`, `data_manager.py`), which
REFUSES (`AuxFeedCausalityError`) to attach any value whose declared window
would end after the bar it is about to be merged onto.

Why this exists: `tests/test_aux_feed_causality_canary.py` (dispatch W8)
empirically proved the merge/execution path applied NO independent defense
against a mistimed feed — a feature equal to a bar's literal NEXT return
produced a ~15x return with nothing anywhere raising. Causality rested
entirely on each fetcher individually respecting its own window; this guard
(dispatch W9) is the shared-code defense that was missing. **Run that
canary's two fixtures whenever you add a feed** (swap in your fetcher's real
output shape) — it is the permanent regression test for this requirement.

Two values cover almost every feed:

| `window_seconds` | When | Examples |
|---|---|---|
| `0` | Instantaneous observation — the value is fully known AT `timestamp`, using no data after it | Funding rate, Fear & Greed |
| your bar width | The value aggregates a FORWARD window `[timestamp, timestamp + window_seconds)` | Whale-footprint features (`window_seconds == bar_seconds`) |

```python
data_manager.register_feed(
    name           = 'your_feed',
    fetcher        = YourFeedFetcher(...),
    window_seconds = 0,        # or your feed's true aggregation width
    agg            = 'last',
)
```

The guard TRUSTS this declaration — it does not re-derive it from how the
value was actually computed. Declare the TRUE window (when is this value
actually finalized, relative to its own `timestamp`?), not the smallest one
that happens to pass. Understating it defeats the guard; overstating it just
means your feed gets rejected on bar grids too fine for it.

If you add the feed to `feed_registry.py`'s `FEED_REGISTRY` /
`RESERVED_FEED_REGISTRY`, add the matching entry to `FEED_WINDOW_SECONDS` in
the same file — `backtester.py`'s generic registration loop looks it up by
name and raises `KeyError` if it is missing (deny by default, same as the
guard itself).

---

## Step 3 — Add import to `fetchers/__init__.py`

```python
from data.fetchers.your_feed_fetcher import YourFeedFetcher
```

---

## Step 4 — Done

`feed_registry.py` auto-discovers the new class by naming convention:
`YourFeedFetcher` → feed name `'your_feed'`.

To use it in a backtest, pass the feed name in `extra_feeds` in `launcher.py`:

```python
bot.load_data(
    start_date  = start_date,
    end_date    = end_date,
    extra_feeds = {k: FEED_REGISTRY[k] for k in ['funding_rate', 'your_feed']},
)
```

The strategy then receives a DataFrame with a `your_feed` column at every
candle close. No other files need changing beyond `FEED_WINDOW_SECONDS`
(Step 2).

---

## Naming convention

`FeedNameFetcher` class → `'feed_name'` column in the DataFrame.

| Class name | Column name |
|---|---|
| `FundingRateFetcher` | `funding_rate` |
| `FearGreedFetcher` | `fear_greed` |
| `OpenInterestFetcher` | `open_interest` |
| `YourFeedFetcher` | `your_feed` |
