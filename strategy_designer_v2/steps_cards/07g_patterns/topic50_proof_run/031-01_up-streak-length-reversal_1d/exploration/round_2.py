def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                if r1[i] > 0: up[i] = up[i-1] + 1
                if r1[i] < 0: dn[i] = dn[i-1] + 1
            ts = pd.to_datetime(b["timestamp"])
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            ret5 = pd.Series(c).pct_change(5).values
            ret10 = pd.Series(c).pct_change(10).values
            ret20 = pd.Series(c).pct_change(20).values
            ret60 = pd.Series(c).pct_change(60).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), fwd=c[i+H]/c[i]-1,
                                 up=up[i], dn=dn[i], vol30=vol30[i], ret5=ret5[i], ret10=ret10[i],
                                 ret20=ret20[i], ret60=ret60[i]))
    df = pd.DataFrame(rows)
    df["unu"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["z"] = df["unu"] / df.groupby("coin")["fwd"].transform("std")
    for k in ["ret5", "ret10", "ret20"]:
        df[k + "s"] = df[k] / (df["vol30"] * np.sqrt(int(k[3:])))
    df["trend"] = pd.cut(df["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    df["vrank"] = df.groupby("coin")["vol30"].rank(pct=True)
    df["agit"] = np.where(df["vrank"] > 0.5, "agit", "calm")
    def ctt(g, x):
        g = g.dropna(subset=[x, "z"])
        xs = (g[x] - g[x].mean()) / g[x].std()
        prod = xs * g["z"]
        s = prod.groupby(g["day"]).sum()
        G = len(s)
        m = prod.sum() / len(g)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum() / len(g) ** 2) if G > 1 else np.nan
        return pd.Series(dict(n=len(g), days=G, corr=m, t_day=m / se,
                              spearman=stats.spearmanr(g[x], g["z"])[0]))
    out = {}
    out["all: momentum vs fwd"] = pd.DataFrame({x: ctt(df, x) for x in ["ret5s", "ret10s", "ret20s"]}).T
    out["by window ret10s"] = df.groupby("win").apply(lambda g: ctt(g, "ret10s"))
    out["by coin ret10s"] = df.groupby("coin").apply(lambda g: ctt(g, "ret10s"))
    out["by trend ret10s"] = df.dropna(subset=["trend"]).groupby(["trend", "agit"]).apply(lambda g: ctt(g, "ret10s"))
    df["upl"] = df["up"].clip(upper=6)
    r = df[(df.up > 0)].dropna(subset=["trend"])
    out["up streak len vs fwd by trend"] = r.groupby("trend").apply(lambda g: ctt(g, "upl"))
    rr = r[r.trend == "rise"]
    out["rise up streak by len"] = rr.groupby(rr["up"].clip(upper=4)).agg(n=("z", "size"), mean_unu=("unu", "mean"), mean_z=("z", "mean"))
    out["rise up streak len by window"] = rr.groupby("win").apply(lambda g: ctt(g, "upl") if len(g) > 8 else pd.Series(dtype=float))
    out["rise calm ret10s"] = ctt(df[(df.trend == "rise") & (df.agit == "calm")], "ret10s")
    return out
