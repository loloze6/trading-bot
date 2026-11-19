import numpy as np, pandas as pd
from scipy import stats

def tt(s):
    s = s.dropna()
    return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan))

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    S = "debug_info.components.slow.last_history_value"; F = "debug_info.components.fast.last_history_value"
    Sp = "debug_info.components.slow.post_pipeline_value"; Fp = "debug_info.components.fast.post_pipeline_value"
    for h in [24, 72]:
        recs = []
        for c in coins:
            g = []
            for w, b in bars[c].items():
                cl = b["close"].values; idx = np.arange(0, len(b)-h, h)
                d = pd.DataFrame({"r": cl[idx+h]/cl[idx]-1, "f": b["forecast"].values[idx],
                                  "sz": b[Sp].values[idx] if Sp in b else np.nan,
                                  "fz": b[Fp].values[idx] if Fp in b else np.nan,
                                  "s_raw": b[S].values[idx] if S in b else np.nan,
                                  "f_raw": b[F].values[idx] if F in b else np.nan,
                                  "w": w, "year": pd.to_datetime(b["timestamp"].values[idx]).year})
                g.append(d)
            g = pd.concat(g); g["ex"] = g.r - g.r.mean(); g["coin"] = c
            recs.append(g)
        R = pd.concat(recs); on = R[R.f > 0].copy()
        on["fq"] = pd.qcut(on.f.rank(method="first"), 3, labels=["lo","mid","hi"])
        on["sq"] = pd.qcut(on.sz.rank(method="first"), 3, labels=["lo","mid","hi"])
        on["ffq"] = pd.qcut(on.fz.rank(method="first"), 3, labels=["lo","mid","hi"])
        out[f"h{h}_by_slowz"] = on.groupby("sq").ex.apply(tt).unstack().round(4)
        out[f"h{h}_by_fastz"] = on.groupby("ffq").ex.apply(tt).unstack().round(4)
        out[f"h{h}_corr"] = pd.Series(dict(
            spear_f=stats.spearmanr(on.f, on.ex, nan_policy="omit").correlation,
            spear_slow=stats.spearmanr(on.sz, on.ex, nan_policy="omit").correlation,
            spear_fast=stats.spearmanr(on.fz, on.ex, nan_policy="omit").correlation,
            spear_fastraw=stats.spearmanr(on.f_raw, on.ex, nan_policy="omit").correlation)).round(4)
        if h == 72:
            hi = on[on.fq == "hi"]
            out["h72_hi_by_coin"] = hi.groupby("coin").ex.apply(tt).unstack().round(4)
            out["h72_hi_by_year"] = hi.groupby("year").ex.apply(tt).unstack().round(4)
            out["h72_hi_excl_top10"] = tt(hi.ex.sort_values().iloc[:-10]).round(4)
    # book daily by day's mean forecast tercile (among active days)
    allday = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            fm = b.groupby("day")["forecast"].mean()
            d = days[c][w].copy(); d["day"] = pd.to_datetime(d["day"]).dt.floor("D"); d = d.set_index("day")
            d["fprev"] = fm.reindex(d.index).shift(1); d["coin"] = c
            allday.append(d)
    A = pd.concat(allday)
    act = A[A.fprev > 0].copy()
    act["q"] = pd.qcut(act.fprev.rank(method="first"), 3, labels=["lo","mid","hi"])
    out["book_daily_by_fq"] = act.groupby("q").book_return.apply(tt).unstack().round(5)
    out["book_sum_share_by_fq"] = (act.groupby("q").book_return.sum()/A.book_return.sum()).round(3)
    out["book_flat_days_sum_share"] = float(A[~(A.fprev > 0)].book_return.sum()/A.book_return.sum())
    return out
