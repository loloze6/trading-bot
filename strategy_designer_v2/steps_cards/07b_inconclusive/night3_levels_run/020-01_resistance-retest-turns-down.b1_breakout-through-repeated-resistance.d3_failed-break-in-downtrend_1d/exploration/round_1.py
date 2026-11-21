def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 10
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rets); usual[coin] = np.std(rets)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            prev = np.r_[0, f[:-1]]
            sig = (f < 0) & ((-f) - np.maximum(-prev, 0) >= 2)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            taken = set()
            for t in np.where(sig)[0]:
                cell = t // H
                if cell in taken: continue
                if t + 20 >= n:
                    if t + H >= n: continue
                taken.add(cell)
                r = {}
                for h in (1, 3, 5, 10, 20):
                    r["r%d" % h] = (-(c[t + h] / c[t] - 1 - drift[coin] * h / 10)) if t + h < n else np.nan
                rows.append(dict(coin=coin, win=w, year=yr[t], absf=-f[t],
                                 fall=df.get("debug_info.components.fall20.last_history_value", pd.Series(np.nan, index=df.index)).iloc[t],
                                 brk=df.get("debug_info.components.break.last_history_value", pd.Series(np.nan, index=df.index)).iloc[t],
                                 ret20=c[t] / c[t - 20] - 1 if t >= 20 else np.nan,
                                 **r))
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["r10"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all_horizons"] = pd.DataFrame({h: [d[h].dropna().mean(), d[h].dropna().mean() / (d[h].dropna().std() / np.sqrt(d[h].notna().sum())), d[h].notna().sum()] for h in ["r1", "r3", "r5", "r10", "r20"]}, index=["mean", "t", "n"])
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["q_absf"] = pd.qcut(d["absf"], 4, labels=False, duplicates="drop")
    out["by_absf_q"] = d.groupby("q_absf").apply(summ)
    d["q_ret20"] = pd.qcut(d["ret20"], 4, labels=False, duplicates="drop")
    out["by_ret20_q(0=deepest)"] = d.groupby("q_ret20").apply(summ)
    d["q_brk"] = pd.qcut(d["brk"].rank(method="first"), 4, labels=False)
    out["by_break_q"] = d.groupby("q_brk").apply(summ)
    out["brk_desc"] = d["brk"].describe()
    out["ret20_desc"] = d["ret20"].describe()
    # coin's own recent trend: 90-day return
    return out
