def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    br = []
    for coin in days:
        for w, d in days[coin].items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w
            br.append(dd)
    D = pd.concat(br)
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday
    D["yr"] = D["day"].dt.year
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    sat = D[D["wd"].isin([4, 5])]
    out["Fri+Sat coin return t by coin"] = sat.groupby("coin")["coin_return"].agg(["count", "mean", tt])
    out["Fri+Sat coin return t by year"] = sat.groupby("yr")["coin_return"].agg(["count", "mean", tt])
    oth = D[~D["wd"].isin([4, 5])]
    out["other days coin return by year"] = oth.groupby("yr")["coin_return"].agg(["count", "mean", tt])
    out["Fri+Sat minus other, Welch t"] = str(stats.ttest_ind(sat["coin_return"].dropna(), oth["coin_return"].dropna(), equal_var=False))
    # book decomposition and positions by z
    rows = []
    for coin in bars:
        mu = pd.concat([days[coin][w]["coin_return"] for w in days[coin]]).mean()
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            pos = b["postRebalance_current_allocation"].astype(float)
            nxt = c.shift(-1) / c - 1
            r20 = c / c.shift(20) - 1
            rows.append(pd.DataFrame({"coin": coin, "w": w, "z": z, "pos": pos, "nxt": nxt, "mu": mu,
                                      "fwd1": nxt, "fwd2_5": c.shift(-5) / c.shift(-1) - 1, "r20": r20,
                                      "z20": r20 / (sd20 * np.sqrt(20)), "i": np.arange(len(b))}))
    A = pd.concat(rows).dropna(subset=["z"])
    A["gain"] = A["pos"] * A["nxt"]
    A["mkt"] = A["pos"] * A["mu"]
    out["mean gain, market part, timing"] = f"{A['gain'].mean():.6f}, {A['mkt'].mean():.6f}, {(A['gain']-A['mkt']).mean():.6f}, avg pos {A['pos'].mean():.3f}, share in {(A['pos'].abs()>1e-6).mean():.3f}"
    A["zb"] = pd.cut(A["z"], [-np.inf, -1, 0, 0.5, 1, 2, np.inf])
    out["by z bucket: pos, next-day ret, days 2-5 ret"] = A.groupby("zb").agg(n=("z", "size"), pos=("pos", "mean"),
        fwd1=("fwd1", "mean"), fwd2_5=("fwd2_5", "mean"), gain=("gain", "mean"))
    # 20d scaled trend, non-overlapping 5-grid
    G = A[A["i"] % 5 == 0].dropna(subset=["z20", "fwd2_5"]).copy()
    G["f5"] = (1 + G["fwd1"]) * (1 + G["fwd2_5"]) - 1
    G["ex5"] = G["f5"] - G.groupby("coin")["f5"].transform("mean")
    sl = stats.linregress(G["z20"], G["ex5"])
    out["slope ex5 on scaled 20d return, t, n"] = f"{sl.slope:.5f}, t={sl.slope/sl.stderr:.2f}, n={len(G)}"
    res = {}
    for coin, g in G.groupby("coin"):
        s = stats.linregress(g["z20"], g["ex5"]); res[coin] = s.slope / s.stderr
    out["per coin t, scaled 20d"] = pd.Series(res)
    G["up"] = G["z"] > 0
    res = {}
    for coin, g in G[G["up"]].groupby("coin"):
        s = stats.linregress(g["z"], g["ex5"]); res[coin] = s.slope / s.stderr
    out["per coin t, up-day z slope"] = pd.Series(res)
    G["yr"] = None
    return out
