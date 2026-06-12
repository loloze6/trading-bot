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

## Step 2 — Add import to `fetchers/__init__.py`

```python
from data.fetchers.your_feed_fetcher import YourFeedFetcher
```

---

## Step 3 — Done

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
candle close. No other files need changing.

---

## Naming convention

`FeedNameFetcher` class → `'feed_name'` column in the DataFrame.

| Class name | Column name |
|---|---|
| `FundingRateFetcher` | `funding_rate` |
| `FearGreedFetcher` | `fear_greed` |
| `OpenInterestFetcher` | `open_interest` |
| `YourFeedFetcher` | `your_feed` |
