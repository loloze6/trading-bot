def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            rets.append(c[1:]/c[:-1]-1)
        drift[coin] = np.concatenate(rets).mean() if rets else 0.0
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            for t in range(n):
                if not (f[t] < 0): continue
                if t+1 >= n: continue
                # run length of down closes before t
                r = 0; k = t-1
                while k >= 1 and c[k] < c[k-1]:
                    r += 1; k -= 1
                ret20 = c[t]/c[t-20]-1 if t >= 20 else np.nan
                d = {"coin": coin, "window": w, "year": ts[t].year, "day": ts[t].normalize(),
                     "f": abs(f[t]), "run": r, "ret20": ret20, "upday": c[t]/c[t-1]-1 if t>=1 else np.nan}
                for h in (1, 2, 3, 5):
                    d[f"u{h}"] = -(c[t+h]/c[t]-1 - h*drift[coin]) if t+h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g, col="u1"):
        x = g[col].dropna()
        if len(x) < 2: return pd.Series({"n": len(x), "mean": x.mean() if len(x) else np.nan, "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "share_pos": (x>0).mean()})
    out = {}
    out["all_by_h"] = pd.DataFrame({h: summ(df, f"u{h}") for h in ("u1","u2","u3","u5")}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_window"] = df.groupby("window").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["runb"] = df["run"].clip(upper=5)
    out["by_run"] = df.groupby("runb").apply(summ)
    df["fq"] = pd.qcut(df["f"].rank(method="first"), 4, labels=False)
    out["by_f_quartile"] = df.groupby("fq").apply(summ)
    df["r20q"] = pd.qcut(df["ret20"].rank(method="first"), 4, labels=False)
    out["by_ret20_quartile_low_is_deep"] = df.groupby("r20q").apply(summ)
    df["upq"] = pd.qcut(df["upday"].rank(method="first"), 4, labels=False)
    out["by_upday_quartile"] = df.groupby("upq").apply(summ)
    out["by_run_h3"] = df.groupby("runb").apply(lambda g: summ(g, "u3"))
    return out
