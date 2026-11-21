def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 20
    rows = []
    ent = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            fwd = c.shift(-H) / c - 1
            fwd2 = c.shift(-2*H) / c.shift(-H) - 1
            sma = c.rolling(50, min_periods=50).mean()
            ma = c / sma - 1
            out_d = {}
            for L, mp in [(90, 60), (60, 40), (30, 25)]:
                out_d[L] = c / c.rolling(L, min_periods=mp).max() - 1
            lo60 = c / c.rolling(60, min_periods=40).min() - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n, H):
                if i + H >= n:
                    break
                rows.append(dict(coin=coin, win=w, fwd=fwd[i], d90=out_d[90][i], d60=out_d[60][i],
                                 d30=out_d[30][i], lo60=lo60[i], ma=ma[i], yr=ts[i].year))
            f = b["forecast"].astype(float).values
            for i in range(1, n):
                if f[i] > 0 and f[i-1] <= 0:
                    ent.append(dict(coin=coin, f20=fwd[i], f2040=fwd2[i], ma=ma[i], d60=out_d[60][i]))
    df = pd.DataFrame(rows)
    df["u"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    out = {}
    def grp(col, q):
        d = df.dropna(subset=[col, "u"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        g = d.groupby("q").agg(mean=("u", "mean"), count=("u", "count"), std=("u", "std"), x=(col, "median"))
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.round(4), d
    for col in ["d90", "d60", "d30", "lo60"]:
        g, d = grp(col, 5)
        out["u by quintile of " + col] = g
        rho, p = stats.spearmanr(d[col], d["u"])
        out["spearman " + col] = f"rho {rho:.3f} p {p:.4f} n {len(d)}"
    g, d = grp("d60", 5)
    out["d60 quintile x coin mean u"] = d.pivot_table(index="coin", columns="q", values="u", aggfunc="mean").round(3)
    out["d60 quintile x year mean u"] = d.pivot_table(index="yr", columns="q", values="u", aggfunc="mean").round(3)
    # within ma>0 vs ma<0
    d["up"] = d["ma"] > 0
    out["d60 quintile x above sma50"] = d.dropna(subset=["ma"]).pivot_table(index="up", columns="q", values="u", aggfunc=["mean", "count"]).round(3)
    E = pd.DataFrame(ent)
    out["entries: fwd 0-20 vs 20-40"] = E[["f20", "f2040"]].agg(["mean", "median", "count"]).round(4)
    t1 = stats.ttest_1samp(E["f2040"].dropna(), 0)
    out["entries 20-40 t"] = f"t {t1.statistic:.2f} n {E['f2040'].notna().sum()}"
    return out
