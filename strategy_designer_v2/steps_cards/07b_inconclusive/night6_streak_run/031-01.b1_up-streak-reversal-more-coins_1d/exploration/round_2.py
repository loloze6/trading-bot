def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in (1, 5):
            v = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    v.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(v)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r1).rolling(60, min_periods=20).std().shift(1).values
            st = np.zeros(n, int); sd = np.zeros(n, int)
            for i in range(1, n):
                st[i] = st[i-1] + 1 if r1[i] > 0 else 0
                sd[i] = sd[i-1] + 1 if r1[i] < 0 else 0
            day = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d").values
            for i in range(1, n):
                rec = dict(coin=coin, w=w, day=day[i], st=st[i], sd=sd[i], r1=r1[i],
                           z=r1[i] / vol[i] if vol[i] and not np.isnan(vol[i]) else np.nan,
                           g5=(i % 5 == 0))
                if i + 1 < n:
                    rec["u1"] = c[i+1] / c[i] - 1 - drift[(coin, 1)]
                if i + 5 < n:
                    rec["u5"] = c[i+5] / c[i] - 1 - drift[(coin, 5)]
                rows.append(rec)
    d = pd.DataFrame(rows)
    def tday(x, col):
        x = x.dropna(subset=[col])
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(x) if G > 1 else np.nan
        return pd.Series(dict(mean=m, t=m / se, days=G, n=len(x)))
    out = {}
    d["stb"] = d["st"].clip(upper=6)
    d["sdb"] = d["sd"].clip(upper=6)
    out["up_streak_u1_allbars"] = d[d.st > 0].groupby("stb").apply(lambda x: tday(x, "u1"))
    out["up_streak_u5_grid5"] = d[(d.st > 0) & d.g5].groupby("stb").apply(lambda x: tday(x, "u5"))
    out["down_streak_u1_allbars"] = d[d.sd > 0].groupby("sdb").apply(lambda x: tday(x, "u1"))
    out["down_streak_u5_grid5"] = d[(d.sd > 0) & d.g5].groupby("sdb").apply(lambda x: tday(x, "u5"))
    e = d.dropna(subset=["z", "u1"]).copy()
    e["zq"] = pd.qcut(e["z"].rank(method="first"), 10, labels=False)
    out["u1_by_today_z_decile"] = e.groupby("zq").apply(lambda x: tday(x, "u1").combine_first(pd.Series({"z": x["z"].mean()})))
    up = e[e.r1 > 0].copy()
    up["zq"] = pd.qcut(up["z"].rank(method="first"), 5, labels=False)
    out["u1_upday_by_z_quint_by_bigcoin"] = up.assign(big=up.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])).groupby(["big","zq"]).apply(lambda x: tday(x, "u1"))
    return out
