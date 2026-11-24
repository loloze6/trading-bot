def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    HS = (3, 5, 7, 10, 14)
    drift = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in HS}
        for w, df in wins.items():
            c = df["close"].values
            for h in HS:
                for i in range(0, len(c) - h, h):
                    rets[h].append(c[i + h] / c[i] - 1)
        drift[coin] = {h: np.mean(v) if v else np.nan for h, v in rets.items()}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            prev = np.r_[0.0, f[:-1]]
            used = set()
            for i in range(len(f)):
                s = np.sign(f[i])
                if s == 0:
                    continue
                pa = prev[i] * s if np.sign(prev[i]) == s else 0.0
                if abs(f[i]) - pa < 2:
                    continue
                cell = i // 14
                if cell in used:
                    continue
                used.add(cell)
                if i + 14 >= len(c):
                    continue
                r = dict(coin=coin, day=ts[i].normalize(), year=ts[i].year, side=s, absf=abs(f[i]))
                for h in HS:
                    r["u%d" % h] = s * (c[i + h] / c[i] - 1 - drift[coin][h])
                r["u7_14"] = s * (c[i + 14] / c[i + 7] - 1 - (drift[coin][14] - drift[coin][7]))
                rows.append(r)
    d = pd.DataFrame(rows)

    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5:
            return pd.Series(dict(n=len(x), mean=np.nan, t=np.nan, days=0))
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return pd.Series(dict(n=len(x), mean=m, t=m / se if se > 0 else np.nan, days=x["day"].nunique()))

    out = {}
    cols = ["u%d" % h for h in HS] + ["u7_14"]
    out["all_h"] = pd.DataFrame({k: ct(d, k) for k in cols}).T
    out["u7_by_side"] = d.groupby("side").apply(lambda x: ct(x, "u7"))
    out["u7_by_year"] = d.groupby("year").apply(lambda x: ct(x, "u7"))
    med = d["absf"].median()
    d["hi"] = (d["absf"] >= med).astype(int)
    out["u7_by_hi"] = d.groupby("hi").apply(lambda x: ct(x, "u7"))
    d["fq"] = pd.qcut(d["absf"], 4, labels=False, duplicates="drop")
    out["u7_by_fq"] = d.groupby("fq").apply(lambda x: ct(x, "u7"))
    out["u7_coins_pos_share"] = float((d.groupby("coin")["u7"].mean() > 0).mean())
    return out
