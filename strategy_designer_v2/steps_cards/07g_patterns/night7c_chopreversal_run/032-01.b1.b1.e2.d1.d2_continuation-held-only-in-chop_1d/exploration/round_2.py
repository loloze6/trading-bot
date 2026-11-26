def explore(data):
    import numpy as np, pandas as pd
    daily = []; rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            absd = c.diff().abs()
            er = (c - c.shift(30)).abs() / absd.rolling(30).sum()
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "er": er, "z": r7 / (sd30 * np.sqrt(7)),
                               "z1": r1 / sd30, "r30": c / c.shift(30) - 1,
                               "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2) / c - 1,
                               "fwd3": c.shift(-3) / c - 1, "fwd7": c.shift(-7) / c - 1,
                               "rng": (b["high"].astype(float) - b["low"].astype(float)) / c / sd30,
                               "clv": (c - b["low"].astype(float)) / (b["high"].astype(float) - b["low"].astype(float))})
            df["pos"] = np.arange(len(df))
            daily.append(df)
    D = pd.concat(daily)
    out = {}
    def st(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"mean": s.mean(), "n": n, "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    for h in ["fwd1", "fwd2", "fwd3", "fwd7"]:
        D["dm_" + h] = D[h] - D.groupby("coin")[h].transform("mean")
    # signed continuation by side in chop, 7d grid
    G = D[D.pos % 7 == 0].dropna(subset=["er", "z", "dm_fwd7"]).copy()
    G["side"] = np.where(G.z > 0, "up", "down")
    G["erc"] = np.where(G.er <= .3, "chop", "notchop")
    out["fwd7 demeaned by side of 7d move and regime (raw, not signed)"] = G.groupby(["erc", "side"])["dm_fwd7"].apply(st).unstack().round(4)
    # 30d direction continuation in ER .15-.3, by coin
    G["s30"] = np.sign(G.r30) * G.dm_fwd7
    g2 = G[(G.er > .15) & (G.er <= .3)]
    out["30d-dir fwd7, ER .15-.3, by coin"] = g2.groupby("coin")["s30"].apply(st).unstack().round(4)
    out["30d-dir fwd7, ER .15-.3, by window"] = g2.groupby("w")["s30"].apply(st).unstack().round(4)
    # daily reversal after large down days: grid of 1 is fine for fwd1; for fwd3 use pos%3
    Dd = D.dropna(subset=["z1"]).copy()
    Dd["z1b"] = pd.cut(Dd["z1"], [-99, -3, -2, -1.5, -1, 0, 99])
    out["dm fwd1 by z1 bucket"] = Dd.groupby("z1b", observed=True)["dm_fwd1"].apply(st).unstack().round(4)
    D3 = Dd[Dd.pos % 3 == 0]
    out["dm fwd3 by z1 bucket (3-day grid)"] = D3.groupby("z1b", observed=True)["dm_fwd3"].apply(st).unstack().round(4)
    big = Dd[Dd.z1 <= -1.5]
    out["dm fwd1 after z1<=-1.5 by coin"] = big.groupby("coin")["dm_fwd1"].apply(st).unstack().round(4)
    out["dm fwd1 after z1<=-1.5 by window"] = big.groupby("w")["dm_fwd1"].apply(st).unstack().round(4)
    big = big.copy(); big["erc"] = np.where(big.er <= .3, "chop", "notchop")
    out["dm fwd1 after z1<=-1.5 by regime"] = big.groupby("erc")["dm_fwd1"].apply(st).unstack().round(4)
    big["clvb"] = pd.cut(big["clv"], [-.01, .2, .5, 1.01])
    out["dm fwd1 after z1<=-1.5 by close location in range"] = big.groupby("clvb", observed=True)["dm_fwd1"].apply(st).unstack().round(4)
    # graded: correlation of -z1 with dm fwd1 over down days
    dn = Dd[Dd.z1 < 0].dropna(subset=["dm_fwd1"])
    x = -dn.z1; y = dn.dm_fwd1
    sl = np.polyfit(x, y, 1)[0]
    res = y - np.polyval(np.polyfit(x, y, 1), x)
    se = np.sqrt((res ** 2).sum() / (len(x) - 2) / ((x - x.mean()) ** 2).sum())
    out["slope dm fwd1 on -z1, down days"] = f"slope {sl:.5f} t {sl/se:.2f} n {len(x)}"
    # day-clustered t for z1<=-2
    b2 = Dd[Dd.z1 <= -2].copy()
    # use pos/window/coin can't group by date; use timestamp not available; approximate by w+pos
    out["z1<=-2 cases, distinct (w,pos)"] = int(b2.groupby(["w", "pos"]).ngroups)
    # weekday stability not checked (chance-prone)
    return out
