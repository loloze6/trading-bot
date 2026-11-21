import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    D = []   # daily returns per coin with weekday, year
    G = []   # 30d-return grid cells (h=10, 20) per coin
    E = []
    for coin, wins in bars.items():
        allr = {h: [] for h in (5, 10, 20)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        mu = {h: np.mean(allr[h]) for h in allr}; sd = {h: np.std(allr[h], ddof=1) for h in allr}
        for w, df in wins.items():
            c = df["close"].values; ts = pd.to_datetime(df["timestamp"]); n = len(c)
            f = df["forecast"].fillna(0).values
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            D.append(pd.DataFrame(dict(coin=coin, r=r, wd=ts.dt.dayofweek.values, yr=ts.dt.year.values)))
            for h in (10, 20):
                for t in range(30, n - h, h):
                    G.append(dict(coin=coin, h=h, r30=c[t] / c[t - 30] - 1, yr=ts.iloc[t].year,
                                  s=(c[t + h] / c[t] - 1 - mu[h]) / sd[h]))
            brk = df.get("debug_info.components.break.last_history_value")
            brk = brk.values if brk is not None else np.full(n, np.nan)
            for t in range(30, n):
                if f[t] > 0 and f[t - 1] <= 0:
                    d = dict(coin=coin, r30=c[t] / c[t - 30] - 1, brk=brk[t], yr=ts.iloc[t].year)
                    for h in (5, 10, 20):
                        d[f"s{h}"] = (c[t + h] / c[t] - 1 - mu[h]) / sd[h] if t + h < n else np.nan
                    d["x11_20"] = (c[t + 20] / c[t + 10] - 1 - mu[10]) if t + 20 < n else np.nan
                    E.append(d)
    D = pd.concat(D).dropna(subset=["r"]); G = pd.DataFrame(G); E = pd.DataFrame(E)
    out = {}
    # weekday: per-coin demeaned daily return, mean by weekday, and count of years positive
    D["rx"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    g = D.groupby("wd").agg(n=("rx", "size"), mean_bps=("rx", lambda s: s.mean() * 1e4))
    g["t"] = D.groupby("wd")["rx"].apply(tstat)
    # average over dates first (cross-coin correlation): mean of coin-average per weekday per year
    yy = D.groupby(["yr", "wd"])["rx"].mean().unstack()
    g["years_pos"] = (yy > 0).sum().values; g["years"] = yy.notna().sum().values
    g["coins_pos"] = (D.groupby(["coin", "wd"])["rx"].mean().unstack() > 0).sum().values
    out["weekday_daily"] = g
    # 30d return quintiles at h=10,20, plus year consistency of top-minus-bottom-two
    for h in (10, 20):
        d = G[G.h == h].copy()
        d["b"] = d.groupby("coin")["r30"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        gg = d.groupby("b").agg(n=("s", "size"), strength=("s", "mean"), r30=("r30", "median"))
        gg["t"] = d.groupby("b")["s"].apply(tstat); out[f"r30_q_h{h}"] = gg
        if h == 10:
            yy = d.groupby(["yr", "b"])["s"].mean().unstack()
            out["r30_h10_by_year_top_minus_q1"] = (yy[4] - yy[1]).to_frame("top_minus_q1")
    # entries: graded by break measure and r30, longer horizons
    e = E.dropna(subset=["s20"]).copy()
    for col in ["brk", "r30"]:
        x = e.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col].rank(method="first"), 3, labels=False)
        gg = x.groupby("b").agg(n=("s20", "size"), s5=("s5", "mean"), s10=("s10", "mean"), s20=("s20", "mean"),
                                feat=(col, "median"))
        gg["t20"] = x.groupby("b")["s20"].apply(tstat); out["entries_by_" + col] = gg
    out["entries_11_20"] = pd.Series(dict(mean=E.x11_20.mean(), t=tstat(E.x11_20), n=E.x11_20.notna().sum()))
    yy = E.groupby("yr")[["s5", "s10", "s20"]].mean(); out["entries_strength_by_year"] = yy
    return out
