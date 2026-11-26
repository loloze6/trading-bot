def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        g5 = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for i in range(0, n - 5, 5):
                g5.append(c[i + 5] / c[i] - 1)
        drift[coin] = np.mean(g5) if g5 else np.nan
        usual[coin] = np.std(g5) if g5 else np.nan
    # per-coin per-horizon drift from all-bar forward returns (grid)
    driftH = {}
    for coin, wins in bars.items():
        for h in H:
            v = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    v.append(c[i + h] / c[i] - 1)
            driftH[(coin, h)] = np.mean(v) if v else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            up = np.r_[False, c[1:] > c[:-1]]
            dn = np.r_[False, c[1:] < c[:-1]]
            st = np.zeros(n, int); sd = np.zeros(n, int)
            for i in range(1, n):
                st[i] = st[i - 1] + 1 if up[i] else 0
                sd[i] = sd[i - 1] + 1 if dn[i] else 0
            r5past = np.full(n, np.nan)
            r5past[5:] = c[5:] / c[:-5] - 1
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            # cases: approx step5: first bar per 5-cell where forecast drops by >=2 from min since last bet / from 0
            lowest = 0.0
            last_cell = -1
            for i in range(n):
                cell = i // 5
                if f[i] >= 0:
                    lowest = 0.0
                    continue
                if f[i] <= lowest - 2 and cell != last_cell:
                    last_cell = cell
                    lowest = f[i]
                    rec = dict(coin=coin, w=w, i=i, year=year[i], streak=st[i], f=f[i],
                               r5past=r5past[i], day=str(df["timestamp"].iloc[i])[:10])
                    for h in H:
                        if i + h < n:
                            rec[f"u{h}"] = -(c[i + h] / c[i] - 1 - driftH[(coin, h)])
                            rec[f"t{h}"] = -(c[i + h] / c[i] - 1)
                    rows.append(rec)
                else:
                    lowest = min(lowest, f[i])
    d = pd.DataFrame(rows)
    out = {}
    def tday(x, col):
        x = x.dropna(subset=[col])
        s = x.groupby("day")[col].sum()
        cnt = x.groupby("day")[col].count()
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(x) if G > 1 else np.nan
        return m, m / se if se else np.nan, G
    s = {}
    for h in H:
        m, t, G = tday(d, f"u{h}")
        s[f"h{h}"] = dict(mean=m, t=t, days=G, n=d[f"u{h}"].notna().sum())
    out["by_horizon_unusual_short"] = pd.DataFrame(s).T
    d["sb"] = d["streak"].clip(upper=6)
    out["by_streak_len_u5"] = d.groupby("sb").apply(lambda x: pd.Series(dict(zip(["mean", "t", "days"], tday(x, "u5"))) | {"n": len(x)}))
    d["fq"] = pd.qcut(d["f"].abs().rank(method="first"), 5, labels=False)
    out["by_absf_quint_u5"] = d.groupby("fq").apply(lambda x: pd.Series(dict(zip(["mean", "t", "days"], tday(x, "u5"))) | {"n": len(x), "absf": x["f"].abs().mean()}))
    out["by_coin_u5"] = d.groupby("coin").apply(lambda x: pd.Series(dict(zip(["mean", "t", "days"], tday(x, "u5"))) | {"n": len(x)}))
    out["by_year_u5"] = d.groupby("year").apply(lambda x: pd.Series(dict(zip(["mean", "t", "days"], tday(x, "u5"))) | {"n": len(x)}))
    d["pq"] = pd.qcut(d["r5past"].rank(method="first"), 5, labels=False)
    out["by_past5ret_quint_u5"] = d.groupby("pq").apply(lambda x: pd.Series(dict(zip(["mean", "t", "days"], tday(x, "u5"))) | {"n": len(x), "r5": x["r5past"].mean()}))
    out["by_streak_len_u10"] = d.groupby("sb").apply(lambda x: pd.Series(dict(zip(["mean", "t", "days"], tday(x, "u10")))))
    return out
