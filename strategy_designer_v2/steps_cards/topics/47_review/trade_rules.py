"""Topic 47, rules on trades tested out of fold (questions 2 and 4 of the operator, 2026-11-23). Per book, a rule is
chosen on three folds and judged on the fourth, each fold in turn (search luck: a rule found and judged on the same
dates says nothing). Judged per book on the test fold: win rate, mean result after costs per trade, summed result.
  (a) long only: short trades dropped (no setting);
  (b) one entry feature: on the training folds, the fifth (lowest or highest, of each feature) whose trades lost the
      most in sum is chosen; on the test fold, trades in that fifth (by the training folds' cut points) are dropped;
  (c) take profit at +T %: a trade whose best move after its entry bar (mfe_clean, clean_excursions.py: the engine's MFE
      includes the entry bar, look-ahead) reached T ends at +T less costs (an order resting at +T fills when the price
      reaches it); T in 1, 2, 3, 5 %: all shown, no choice;
  (d) stop at -S %: a trade whose worst move after its entry bar reached S ends at -S less costs; S in 2, 3, 5, 10 %.
The result after costs here is per trade, not the book's daily path (Calmar): a first screen.
  python3 topics/47_review/trade_rules.py TRADES.csv.gz"""
import sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
d = pd.read_csv(sys.argv[1]); d["cost"] = d.mae * 0 + 0.10            # the engine's fee per trade in these records: 10 bps
FEATS = ["abs_forecast", "vol20", "ret30", "below_high90", "volume_ratio", "market_ret30", "market_vol20", "crowd"]


def judge(base, kept):
    return {"win_before": base.win.mean(), "win_after": kept.win.mean() if len(kept) else np.nan,
            "mean_before": base.net_pct.mean(), "mean_after": kept.net_pct.mean() if len(kept) else np.nan,
            "sum_before": base.net_pct.sum(), "sum_after": kept.net_pct.sum(), "kept": len(kept) / len(base)}


rows = []
for (bar, book), x in d.groupby(["bar", "book"]):
    folds = sorted(x.fold.dropna().unique())
    if len(folds) < 4: continue
    for f in folds:
        tr, te = x[x.fold != f], x[x.fold == f]
        if len(te) < 20: continue
        rows.append({"bar": bar, "book": book, "fold": f, "rule": "(a) long only", **judge(te, te[te.direction == "long"])})
        best = None
        for feat in FEATS:
            cuts = tr[feat].quantile([0.2, 0.8]).to_numpy()
            for side, mask_tr in (("low", tr[feat] <= cuts[0]), ("high", tr[feat] >= cuts[1])):
                loss = tr[mask_tr].net_pct.sum()
                if best is None or loss < best[0]: best = (loss, feat, side, cuts)
        _, feat, side, cuts = best
        drop = te[feat] <= cuts[0] if side == "low" else te[feat] >= cuts[1]
        rows.append({"bar": bar, "book": book, "fold": f, "rule": "(b) drop the worst fifth of one feature", "feature": f"{feat} {side}", **judge(te, te[~drop])})
        for T in (1, 2, 3, 5):
            y = te.copy()
            hit = y.mfe_clean >= T
            y.loc[hit, "net_pct"] = T - y.loc[hit, "cost"]
            y["win"] = y.net_pct > 0
            rows.append({"bar": bar, "book": book, "fold": f, "rule": f"(c) take profit at +{T} %", **judge(te, y)})
        for S in (2, 3, 5, 10):
            y = te.copy()
            hit = y.mae_clean >= S
            y.loc[hit, "net_pct"] = -S - y.loc[hit, "cost"]
            y["win"] = y.net_pct > 0
            rows.append({"bar": bar, "book": book, "fold": f, "rule": f"(d) stop at -{S} %", **judge(te, y)})
r = pd.DataFrame(rows)
r["better_sum"] = r.sum_after > r.sum_before
pd.set_option("display.width", 220)
for bar, x in r.groupby("bar"):
    print(f"\n== {bar}: {x.book.nunique()} books, {len(x[x.rule == '(a) long only'])} book-folds")
    print(x.groupby("rule").agg(win_before=("win_before", "median"), win_after=("win_after", "median"), mean_before=("mean_before", "median"),
                                mean_after=("mean_after", "median"), kept=("kept", "median"), book_folds_better=("better_sum", "mean")).round(3).to_string())
    b = x[x.rule.str.startswith("(b)")]
    print(" (b) features chosen on the training folds:", b.feature.value_counts().head(6).to_dict())
r.to_csv("trade_rules.csv", index=False, float_format="%.4g")
