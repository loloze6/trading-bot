import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["year"] = ts.dt.year
            r1 = c.pct_change()
            df["vol20"] = r1.rolling(20).std()
            df["ret26"] = c / c.shift(26) - 1
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            df["above"] = c / top - 1
            df["thick"] = top / bot - 1
            df["cloud_rising"] = sa.diff(5)
            df["valid"] = top.notna()
            for h in [10, 26]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in [26, 10]:
        G = D[(D["pos"] % h == 0)].copy()
        G["u"] = G[f"f{h}"] - G.groupby("coin")[f"f{h}"].transform("mean")
        G["usd"] = G.groupby("coin")[f"f{h}"].transform("std")
        A = G[G.valid & (G.above > 0)].dropna(subset=["u"]).copy()
        A["strength"] = A["u"] / A["usd"]
        A["ab_v"] = A["above"] / (A["vol20"] * np.sqrt(26))
        out[f"h{h}_above_summary"] = pd.Series({"n": len(A), "unusual": A.u.mean(),
            "t": A.u.mean() / (A.u.std() / np.sqrt(len(A))), "total": A[f"f{h}"].mean(),
            "strength": A.strength.mean()})
        A["q"] = pd.qcut(A["ab_v"], 3, labels=False)
        q = A.groupby("q")["u"].agg(["mean", "std", "count"]); q["t"] = q["mean"] / (q["std"] / np.sqrt(q["count"]))
        out[f"h{h}_above_by_dist_over_vol_tercile"] = q
        out[f"h{h}_above_by_coin"] = A.groupby("coin")["u"].agg(["mean", "count"])
        out[f"h{h}_above_by_year"] = A.groupby("year")["u"].agg(["mean", "count"])
        A["rising"] = A["cloud_rising"] > 0
        out[f"h{h}_above_by_cloud_rising"] = A.groupby("rising")["u"].agg(["mean", "count"])
        # beyond ret26: above-cloud vs other bars among ret26>0
        P = G[G.valid & (G.ret26 > 0)].dropna(subset=["u"])
        a = P.loc[P.above > 0, "u"]; o = P.loc[P.above <= 0, "u"]
        out[f"h{h}_ret26pos_above_minus_not"] = pd.Series({"diff": a.mean() - o.mean(),
            "t": stats.ttest_ind(a, o, equal_var=False).statistic, "n_above": len(a), "n_not": len(o)})
        g = A.dropna(subset=["ab_v"])
        sl = stats.linregress(g["ab_v"], g["u"])
        out[f"h{h}_slope_u_on_dist"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(g)})
    return out
