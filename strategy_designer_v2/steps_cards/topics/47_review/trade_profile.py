"""Topic 47, the trades' profile (questions 1 and 3-4 of the operator, 2026-11-23). From the trade table
(trade_table.py): per bar size (1d, 1h), every entry feature cut into fifths WITHIN each book (so books with different
typical trades are not mixed), then the books averaged: win rate and mean result after costs per fifth. Then the
excursions: how deep losers and winners went (MAE), how far in profit they went (MFE), the share of losers that were
once in profit by 1 %, how much of their best gain winners kept (exit efficiency), what the price did after exits.
  python3 topics/47_review/trade_profile.py TRADES.csv.gz"""
import sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
d = pd.read_csv(sys.argv[1], parse_dates=["entry_time"])
FEATS = ["abs_forecast", "vol20", "ret30", "below_high90", "volume_ratio", "market_ret30", "market_vol20", "crowd"]
pd.set_option("display.width", 220)
for bar, x in d.groupby("bar"):
    print(f"\n################ {bar}: {len(x)} trades, {x.book.nunique()} books; win rate {x.win.mean():.3f}, mean after costs {x.net_pct.mean():.3f} %")
    rows = []
    for f in FEATS:
        q = x.groupby("book")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) if s.nunique() > 4 else np.nan)
        g = x.assign(q=q).dropna(subset=["q"]).groupby(["book", "q"]).agg(win=("win", "mean"), net=("net_pct", "mean")).groupby("q").mean()
        rows.append(pd.Series({**{f"win q{int(k)+1}": v for k, v in g.win.items()}, **{f"net q{int(k)+1}": v for k, v in g.net.items()}}, name=f))
    t = pd.DataFrame(rows)
    print("win rate by fifth (q1 lowest value of the feature, q5 highest), books averaged:")
    print(t[[c for c in t if c.startswith("win")]].round(3).to_string())
    print("mean result after costs (%) by fifth:")
    print(t[[c for c in t if c.startswith("net")]].round(3).to_string())
    for f in ("weekday", "direction"):
        g = x.groupby(["book", f]).agg(win=("win", "mean"), net=("net_pct", "mean"), n=("win", "size")).groupby(f).agg(win=("win", "mean"), net=("net", "mean"), books=("n", "size"))
        print(f"by {f}:", g.round(3).to_dict("index"))
    w, l = x[x.win], x[~x.win]
    print("excursions (medians, %):")
    print(f"  losers: final {l.net_pct.median():.2f}, went against {l.mae.median():.2f}, went in favour {l.mfe.median():.2f}; "
          f"share once +1 % in profit {100 * (l.mfe >= 1).mean():.0f} %, once +2 % {100 * (l.mfe >= 2).mean():.0f} %")
    print(f"  winners: final {w.net_pct.median():.2f}, went against {w.mae.median():.2f} (share that first went 3 % against: {100 * (w.mae >= 3).mean():.0f} %), "
          f"best {w.mfe.median():.2f}, share of the best kept {w.exit_efficiency.median():.2f}")
    print(f"  after the exit, 5 bars: winners {w.post_exit_return_5bars.median():.2f}, losers {l.post_exit_return_5bars.median():.2f}; "
          f"20 bars: winners {w.post_exit_return_20bars.median():.2f}, losers {l.post_exit_return_20bars.median():.2f}")
    top = x.groupby("book").apply(lambda g: g.net_pct.clip(lower=0).sort_values(ascending=False).head(max(1, len(g) // 10)).sum() / g.net_pct.sum() if g.net_pct.sum() > 0 else np.nan)
    print(f"  books with a positive total: the best tenth of trades makes {top.median():.1f} times the total (median)")
