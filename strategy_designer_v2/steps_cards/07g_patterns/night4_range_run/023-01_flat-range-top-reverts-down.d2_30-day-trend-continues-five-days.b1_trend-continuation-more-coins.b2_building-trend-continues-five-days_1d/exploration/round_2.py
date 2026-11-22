def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        allg = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allg.append(c[i + H] / c[i] - 1)
        dr = np.mean(allg)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float).rolling(30).max()
            lo = b["low"].astype(float).rolling(30).min()
            R30 = c / c.shift(30) - 1
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            zR30 = R30 / (vol30 * np.sqrt(30))
            z1 = r1 / r1.rolling(20).std().shift(1)
            vz = np.log(b["volume"].astype(float) + 1)
            vz = (vz - vz.rolling(30).mean().shift(1)) / vz.rolling(30).std().shift(1)
            pos = (c - lo) / (hi - lo)
            dd = c / c.rolling(30).max() - 1
            al = b["postRebalance_current_allocation"].astype(float)
            n = len(c)
            for i in range(0, n - H, H):
                f = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 R30=R30.iloc[i], zR30=zR30.iloc[i], z1=z1.iloc[i], vz=vz.iloc[i],
                                 pos=pos.iloc[i], dd=dd.iloc[i], fc=b["forecast"].iloc[i],
                                 al=al.iloc[i], fwd=f, ex=f - dr))
    g = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    h = g.dropna(subset=["R30"]).copy()
    # finer R30 bottom: ventiles
    h["rv"] = pd.qcut(h["R30"], 20, labels=False)
    out["excess by R30 ventile"] = h.groupby("rv")["ex"].apply(tt).unstack()
    # vol-scaled 30d return
    h2 = h.dropna(subset=["zR30"]).copy()
    h2["zd"] = pd.qcut(h2["zR30"], 10, labels=False)
    out["excess by vol-scaled R30 decile"] = h2.groupby("zd")["ex"].apply(tt).unstack()
    # drawdown from 30-day high
    h3 = h.dropna(subset=["dd"]).copy()
    h3["ddq"] = pd.qcut(h3["dd"], 10, labels=False, duplicates="drop")
    out["excess by drawdown-from-30d-high decile"] = h3.groupby("ddq")["ex"].apply(tt).unstack()
    # bottom R30 decile split by year halves and by coin count
    bot = h[h["rv"] <= 1]
    out["bottom R30 tenth by year"] = bot.groupby("year")["ex"].apply(tt).unstack()
    out["bottom tenth minus next tenth Welch"] = pd.Series(dict(
        diff=bot["ex"].mean() - h[h["rv"].isin([2, 3])]["ex"].mean(),
        t=stats.ttest_ind(bot["ex"], h[h["rv"].isin([2, 3])]["ex"], equal_var=False).statistic,
        coins_pos=(bot.groupby("coin")["ex"].mean() > 0).mean()))
    # large up days: continuation, graded
    k = g.dropna(subset=["z1"]).copy()
    up = k[k["z1"] > 0]
    sl = stats.linregress(up["z1"], up["ex"])
    dn = k[k["z1"] < 0]
    sl2 = stats.linregress(dn["z1"], dn["ex"])
    out["slope ex on z1, up days / down days"] = pd.DataFrame(dict(slope=[sl.slope, sl2.slope], t=[sl.slope / sl.stderr, sl2.slope / sl2.stderr], n=[len(up), len(dn)]), index=["up", "down"])
    big = k[k["z1"] > 1.5]
    out["big up day by year"] = big.groupby("year")["ex"].apply(tt).unstack()
    out["big up day median ex, share>0"] = pd.Series(dict(median=big["ex"].median(), share_pos=(big["ex"] > 0).mean(), n=len(big)))
    # volume surge
    v = g.dropna(subset=["vz", "z1"]).copy()
    v["vq"] = pd.qcut(v["vz"], 5, labels=False)
    v["sgn"] = np.sign(v["z1"]) * v["ex"]
    out["1-day-direction signed excess by volume quintile"] = v.groupby("vq")["sgn"].apply(tt).unstack()
    # book: long vs short gain per grid cell
    a = g.dropna(subset=["al"]).copy()
    a["side"] = np.where(a["al"] > 0, "long", np.where(a["al"] < 0, "short", "flat"))
    a["gain"] = a["al"] * a["fwd"]
    out["position gain by side (5-bar)"] = a.groupby("side")["gain"].apply(tt).unstack()
    out["position excess gain by side"] = a.assign(eg=a["al"] * a["ex"]).groupby("side")["eg"].apply(tt).unstack()
    return out
