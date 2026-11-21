def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    allbars = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            rs = np.array(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values; hi = df["high"].values
            n = len(c)
            ret20 = np.full(n, np.nan); ret20[20:] = c[20:] / c[:-20] - 1
            sw = [(j, lo[j]) for j in range(2, n - 2)
                  if lo[j] < lo[j-1] and lo[j] < lo[j-2] and lo[j] < lo[j+1] and lo[j] < lo[j+2]]
            sh = [(j, hi[j]) for j in range(2, n - 2)
                  if hi[j] > hi[j-1] and hi[j] > hi[j-2] and hi[j] > hi[j+1] and hi[j] > hi[j+2]]
            for t in range(n):
                lows = [v for (j, v) in sw if j + 2 <= t and j >= t - 90]
                highs = [v for (j, v) in sh if j + 2 <= t and j >= t - 90]
                # weighted nearness just below lows (0..3%)
                nbw = sum(max(0, 1 - (1 - c[t] / v) / 0.03) for v in lows if 0 < 1 - c[t] / v <= 0.03)
                nb = sum(1 for v in lows if 0 < 1 - c[t] / v <= 0.03)
                nh = sum(1 for v in highs if 0 < c[t] / v - 1 <= 0.03)
                rec = dict(coin=coin, w=w, t=t, nb=nb, nbw=nbw, nh=nh, ret20=ret20[t],
                           year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for h in H:
                    if t + h < n:
                        r = c[t + h] / c[t] - 1
                        rec[f"x{h}"] = r - drift[(coin, h)][0]
                        rec[f"r{h}"] = r
                        rec[f"s{h}"] = drift[(coin, h)][1]
                    else:
                        rec[f"x{h}"] = np.nan; rec[f"r{h}"] = np.nan; rec[f"s{h}"] = np.nan
                allbars.append(rec)
    A = pd.DataFrame(allbars)
    def tm(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    tab = {}
    for h in H:
        G = A[A.t % h == 0]
        for k in [0, 1, 2, 3]:
            s = G[G.nb.clip(upper=3) == k][f"x{h}"]
            r = tm(s); tab[(h, k)] = r
    out["nb count by horizon x"] = pd.DataFrame(tab).T
    G = A[A.t % 5 == 0].copy()
    G["nbc"] = G.nb.clip(upper=3)
    Gb = G[G.nb >= 2]
    out["nb>=2 by coin x5"] = Gb.groupby("coin")["x5"].apply(tm).unstack()
    out["nb>=2 by year x5"] = Gb.groupby("year")["x5"].apply(tm).unstack()
    out["nb>=2 by 20d trend sign x5"] = Gb.groupby(np.sign(Gb.ret20))["x5"].apply(tm).unstack()
    out["nb>=1 total move r5 and strength"] = pd.Series({
        "total r5 % (short side, -r5)": -100*G[G.nb >= 1].r5.mean(),
        "unusual % (short, -x5)": -100*G[G.nb >= 1].x5.mean(),
        "strength": (-G[G.nb >= 1].x5 / G[G.nb >= 1].s5).mean(),
        "total nb>=2 %": -100*Gb.r5.mean(),
        "strength nb>=2": (-Gb.x5 / Gb.s5).mean(),
        "spearman nbw vs x5 (nb>=1)": G[G.nb >= 1][["nbw", "x5"]].corr("spearman").iloc[0, 1]})
    out["nh count (just above highs) x5"] = G.groupby(G.nh.clip(upper=3))["x5"].apply(tm).unstack()
    # half split of windows
    G["half"] = np.where(G.w.str[1:].astype(int) <= 12, "w1-12", "w13-24")
    out["nbc by window half x5"] = G.groupby(["half", "nbc"])["x5"].apply(tm).unstack()
    return out
