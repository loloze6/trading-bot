import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []      # grid-based rows for every h
    cases = []     # replicated step-5 cases (h=5)
    sdall = {}
    for coin, wins in bars.items():
        allsd = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=30).std()
            allsd.append(sd)
        sdall[coin] = pd.concat(allsd).median()
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=30).std()
            z = r / sd
            tr = c / c.shift(60) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr[i], z=z[i], fwd=fwd[i],
                                     agit=(sd[i] > sdall[coin]) if pd.notna(sd[i]) else np.nan,
                                     tr=tr[i], day=b["timestamp"].iloc[i]))
            f = b["forecast"].fillna(0).values
            low = 0.0; taken = set()
            fwd5 = (c.shift(-5) / c - 1).values
            for i in range(len(b)):
                if f[i] <= 0:
                    low = 0.0; continue
                low = min(low, f[i])
                if f[i] - low >= 2:
                    cell = i // 5
                    if cell not in taken:
                        taken.add(cell)
                        cases.append(dict(coin=coin, w=w, f=f[i], z=z[i], fwd=fwd5[i], year=yr[i],
                                          agit=(sd[i] > sdall[coin]) if pd.notna(sd[i]) else np.nan,
                                          tr=tr[i], day=b["timestamp"].iloc[i]))
                    low = f[i]
    G = pd.DataFrame(rows)
    drift = G.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    G = G.join(drift, on=["coin", "h"]); G["un"] = G["fwd"] - G["drift"]
    out = {}
    # graded test on grid: slope of unusual move on z, by h, agitation, sign of z
    res = []
    for (h, ag, sgn), g in G.dropna(subset=["z", "un", "agit"]).assign(sgn=lambda d: np.sign(d.z)).groupby(["h", "agit", "sgn"]):
        if len(g) < 30: continue
        sl = stats.linregress(g.z, g.un)
        big = g[g.z.abs() > 1.5]
        res.append(dict(h=h, agitated=ag, side=sgn, n=len(g), slope=sl.slope, t_slope=sl.slope / sl.stderr,
                        n_big=len(big), big_un_mean=big.un.mean(),
                        big_t=big.un.mean() / (big.un.std() / np.sqrt(len(big))) if len(big) > 2 else np.nan))
    out["grid graded by h/agit/side"] = pd.DataFrame(res)
    C = pd.DataFrame(cases)
    d5 = drift.xs(5, level="h")
    C["un"] = C["fwd"] - C["coin"].map(d5)
    C = C.dropna(subset=["un"])
    def summ(g):
        return pd.Series(dict(n=len(g), un=g.un.mean(), t=g.un.mean() / (g.un.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out["cases total"] = summ(C).to_frame().T
    out["cases by agitation"] = C.dropna(subset=["agit"]).groupby("agit").apply(summ)
    C["trend"] = pd.cut(C.tr, [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["cases by trend"] = C.groupby("trend").apply(summ)
    out["cases by trend x agit"] = C.dropna(subset=["agit"]).groupby(["trend", "agit"]).apply(summ)
    C["fq"] = pd.qcut(C.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["cases by forecast quartile"] = C.groupby("fq").apply(summ)
    out["cases by coin"] = C.groupby("coin").apply(summ)
    out["cases by year"] = C.groupby("year").apply(summ)
    out["cases by window"] = C.groupby("w").apply(summ)
    return out
