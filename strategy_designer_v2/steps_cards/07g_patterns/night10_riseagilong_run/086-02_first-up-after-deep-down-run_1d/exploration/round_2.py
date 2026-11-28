import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []; coinmean = {}
    for coin, wins in bars.items():
        allg = {h: [] for h in (3, 5, 10)}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float)
            r = c.pct_change(); sd30 = r.rolling(30, min_periods=20).std().shift(1)
            f = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            f["prof"] = (b["regime"] != "chop").values
            f["yr"] = pd.to_datetime(b["timestamp"]).dt.year.values
            f["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64").values
            for k in (2, 3, 5, 7):
                f[f"r{k}z"] = (c.pct_change(k) / (sd30 * np.sqrt(k))).values
            f["dhigh20z"] = ((c / hi.rolling(20, min_periods=10).max() - 1) / sd30).values
            for h in (3, 5, 10):
                fr = c.shift(-h) / c - 1
                f[f"fr{h}"] = fr.values
                allg[h] += list(fr.iloc[::h].dropna().values)
            rows.append(f)
        coinmean[coin] = {h: np.mean(allg[h]) for h in allg}
    F = pd.concat(rows, ignore_index=True)
    for h in (3, 5, 10):
        F[f"ex{h}"] = F[f"fr{h}"] - F["coin"].map(lambda k: coinmean[k][h])
    P = F[F["prof"]]
    out = {}
    # offsets robustness for slope
    res = []
    for ft in ("r2z", "r3z", "r5z", "r7z", "dhigh20z"):
        for h in (3, 5, 10):
            for off in range(h if h < 6 else 5):
                G = P[P["pos"] % h == off][[ft, f"ex{h}"]].dropna()
                sl = stats.linregress(G[ft], G[f"ex{h}"])
                res.append({"feat": ft, "h": h, "off": off, "n": len(G), "t": sl.slope / sl.stderr, "slope": sl.slope})
    R = pd.DataFrame(res)
    out["slope t over grid offsets"] = R.groupby(["feat", "h"])["t"].agg(["mean", "min", "max"]).round(2)
    G = P[P["pos"] % 5 == 0].dropna(subset=["r3z", "ex5"])
    def tt(x): return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    out["r3z h5 by coin slope t"] = G.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "t": stats.linregress(d["r3z"], d["ex5"]).slope / stats.linregress(d["r3z"], d["ex5"]).stderr}))
    G["early"] = G["win"].str[1:].astype(int) <= 14
    out["r3z h5 early/late slope t"] = G.groupby("early").apply(lambda d: pd.Series({"n": len(d), "t": stats.linregress(d["r3z"], d["ex5"]).slope / stats.linregress(d["r3z"], d["ex5"]).stderr}))
    # positive side only: graded among r3z>0
    Gp = G[G["r3z"] > 0]
    sl = stats.linregress(Gp["r3z"], Gp["ex5"])
    out["r3z>0 slope"] = pd.Series({"n": len(Gp), "slope": sl.slope, "t": sl.slope / sl.stderr, "mean_ex5": Gp["ex5"].mean(), "t_mean": tt(Gp["ex5"])})
    Gn = G[G["r3z"] <= 0]
    out["r3z<=0 mean"] = pd.Series({"n": len(Gn), "mean_ex5": Gn["ex5"].mean(), "t_mean": tt(Gn["ex5"])})
    # all offsets pooled, day-clustered weighted mean ex5 by r3z bins
    A = P.dropna(subset=["r3z", "ex5"]).copy()
    A["bin"] = pd.cut(A["r3z"], [-9, -1.5, -0.5, 0.5, 1.5, 9])
    out["all bars r3z bins ex5 (overlapping, read only)"] = A.groupby("bin")["ex5"].agg(["count", "mean"])
    out["by year r3z h5 slope"] = G.groupby("yr").apply(lambda d: pd.Series({"n": len(d), "slope": stats.linregress(d["r3z"], d["ex5"]).slope if len(d) > 5 else np.nan}))
    return out
