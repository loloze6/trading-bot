def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 7
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float); n = len(cl)
            s_ = pd.Series(cl)
            r1 = s_.pct_change(1).values; r3 = s_.pct_change(3).values
            r14 = s_.pct_change(14).values; r60 = s_.pct_change(60).values
            vol20 = pd.Series(r1).rolling(20).std().values
            for i in range(0, n - H, H):
                rows.append(dict(coin=c, w=w, fwd=cl[i+H]/cl[i]-1, r1=r1[i], r3=r3[i], r14=r14[i], r60=r60[i],
                                 vol20=vol20[i], reg=df["regime"].iloc[i]))
    s = pd.DataFrame(rows)
    s["dm"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
    out = {}
    def tab(g, col):
        a = g.groupby(col)["dm"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    tr = s[s.reg == "trending"].dropna(subset=["r1", "r14", "r3"]).copy()
    un = s[s.reg != "trending"].copy()
    # partial: r1 and r3 beyond r14 in trending
    X = np.column_stack([np.ones(len(tr)), tr["r14"], tr["r1"]])
    b, res, *_ = np.linalg.lstsq(X, tr["dm"].values, rcond=None)
    e = tr["dm"].values - X @ b; s2 = e @ e / (len(e) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["trend OLS dm~r14+r1 (coef,t)"] = pd.DataFrame({"coef": b, "t": b / se}, index=["c", "r14", "r1"])
    tr["q1"] = pd.qcut(tr["r1"], 5, labels=False); out["trend r1 quint"] = tab(tr, "q1")
    tr["q3"] = pd.qcut(tr["r3"], 5, labels=False); out["trend r3 quint"] = tab(tr, "q3")
    # per coin corr r1/r14 in trending
    pc = {}
    for c, g in tr.groupby("coin"):
        pc[c] = (round(stats.pearsonr(g.r14, g.dm)[0], 3), round(stats.pearsonr(g.r1, g.dm)[0], 3), len(g))
    out["trend per coin corr r14,r1"] = pd.DataFrame(pc, index=["r14", "r1", "n"]).T
    # untrending: r60 and vol20
    u = un.dropna(subset=["r60"]).copy()
    u["q60"] = pd.qcut(u["r60"], 5, labels=False); out["untrend r60 quint"] = tab(u, "q60")
    pc = {}
    for c, g in u.groupby("coin"):
        pc[c] = (round(stats.pearsonr(g.r60, g.dm)[0], 3), len(g))
    out["untrend per coin corr r60"] = pd.DataFrame(pc, index=["r", "n"]).T
    u2 = un.dropna(subset=["vol20"]).copy()
    u2["qv"] = pd.qcut(u2["vol20"], 5, labels=False); out["untrend vol20 quint"] = tab(u2, "qv")
    # weekday: per coin and per year, and book
    d = []
    for c in days:
        for w, df in days[c].items():
            x = df.copy(); x["coin"] = c; x["w"] = w; d.append(x)
    d = pd.concat(d).dropna(subset=["coin_return"])
    d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; d["yr"] = pd.to_datetime(d["day"]).dt.year
    d["dmc"] = d["coin_return"] - d.groupby("coin")["coin_return"].transform("mean")
    out["sat-minus-rest t per coin"] = d.groupby("coin").apply(lambda g: pd.Series(stats.ttest_ind(g.dmc[g.wd == 5], g.dmc[g.wd != 5], equal_var=False), index=["t", "p"]))
    out["sat mean by year"] = d[d.wd == 5].groupby("yr")["dmc"].agg(["mean", "count"])
    out["weekday mean by coin"] = d.pivot_table(index="wd", columns="coin", values="dmc", aggfunc="mean")
    # cross-coin daily mean by weekday (one obs per day to avoid correlation)
    dd = d.groupby(["day", "wd"])["coin_return"].mean().reset_index()
    out["weekday, one obs per day"] = dd.groupby("wd")["coin_return"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["book by weekday"] = d.groupby("wd")["book_return"].agg(["mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
