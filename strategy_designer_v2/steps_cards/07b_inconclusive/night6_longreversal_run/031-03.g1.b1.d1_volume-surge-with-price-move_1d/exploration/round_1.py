def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 14
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in (7, 14, 28)}
        for w, df in wins.items():
            c = df["close"].values
            for h in rets:
                for i in range(0, len(c) - h, h):
                    rets[h].append(c[i + h] / c[i] - 1)
        drift[coin] = {h: np.mean(v) if v else np.nan for h, v in rets.items()}
        usual[coin] = np.std(rets[14], ddof=1) if len(rets[14]) > 2 else np.nan
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
                cell = i // H
                if cell in used:
                    continue
                used.add(cell)
                if i + H >= len(c):
                    continue
                r = {}
                for h in (7, 14, 28):
                    r[h] = (s * (c[i + h] / c[i] - 1 - drift[coin][h])) if i + h < len(c) else np.nan
                ret14p = c[i] / c[i - 14] - 1 if i >= 14 else np.nan
                rows.append(dict(coin=coin, win=w, day=ts[i].normalize(), year=ts[i].year, side=s,
                                 absf=abs(f[i]), u7=r[7], u14=r[14], u28=r[28],
                                 tot14=s * (c[i + H] / c[i] - 1), absret14=abs(ret14p) if ret14p == ret14p else np.nan))
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
    out["all"] = pd.DataFrame({k: ct(d, k) for k in ["u7", "u14", "u28", "tot14"]}).T
    out["by_side"] = d.groupby("side").apply(lambda x: ct(x, "u14"))
    out["by_side_u28"] = d.groupby("side").apply(lambda x: ct(x, "u28"))
    out["by_year"] = d.groupby("year").apply(lambda x: ct(x, "u14"))
    out["by_coin"] = d.groupby("coin").apply(lambda x: ct(x, "u14"))
    d["fq"] = pd.qcut(d["absf"], 4, labels=False, duplicates="drop")
    out["by_absf_q"] = d.groupby(["side", "fq"]).apply(lambda x: ct(x, "u14"))
    d["rq"] = pd.qcut(d["absret14"], 4, labels=False, duplicates="drop")
    out["by_absret14_q"] = d.groupby(["side", "rq"]).apply(lambda x: ct(x, "u14"))
    out["usual14_mean"] = float(np.nanmean(list(usual.values())))
    return out
