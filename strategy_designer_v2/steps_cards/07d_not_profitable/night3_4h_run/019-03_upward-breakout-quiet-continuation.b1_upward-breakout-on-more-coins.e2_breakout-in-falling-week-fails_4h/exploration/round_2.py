def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets.extend(list(c[idx + H] / c[idx] - 1))
        drift = np.mean(rets); sd = np.std(rets)
        # per-bar drift and 42-bar sd for depth scaling
        r42 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 42, 42)
            r42.extend(list(c[idx + 42] / c[idx] - 1))
        sd42 = np.std(r42)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            a = b["postRebalance_current_allocation"].fillna(0).values
            f = b["forecast"].fillna(0).values
            g = np.zeros(n); g[:-1] = a[:-1] * (c[1:] / c[:-1] - 1)
            past7 = pd.Series(c).pct_change(42).values
            # attribute each bar's position gain to the episode's entry depth
            ent_depth = np.nan; ent_f = np.nan
            for t in range(n):
                if abs(a[t]) > 1e-6:
                    if t == 0 or abs(a[t-1]) <= 1e-6:
                        ent_depth = past7[t] / sd42 if past7[t] == past7[t] else np.nan
                        ent_f = f[t]
                    rows.append(dict(coin=coin, wnum=int(w[1:]), gain=g[t], alloc=a[t],
                                     depth=ent_depth, ef=ent_f,
                                     barsin=None))
    df = pd.DataFrame(rows).dropna(subset=["depth"])
    df["dq"] = pd.qcut(df.depth, 5)
    out["book_gain_by_entry_depth_in_sd"] = df.groupby("dq").agg(
        bars=("gain", "size"), sum_gain=("gain", "sum"), mean_abs_alloc=("alloc", lambda x: x.abs().mean()),
        mean_fc=("ef", "mean"))
    out["fc_vs_depth_corr"] = float(df[["depth", "ef"]].corr().iloc[0, 1])
    # cases by depth in usual-move units (one per cell)
    rows2 = []
    for coin, wins in data["bars"].items():
        rets = []; r42 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H); rets.extend(list(c[idx + H] / c[idx] - 1))
            idx = np.arange(0, len(c) - 42, 42); r42.extend(list(c[idx + 42] / c[idx] - 1))
        drift = np.mean(rets); sd = np.std(rets); sd42 = np.std(r42)
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"].values; n = len(c)
            f = b["forecast"].fillna(0).values
            past7 = pd.Series(c).pct_change(42).values
            seen = set(); prev = 0
            for t in range(n):
                if f[t] < 0 and prev >= 0 and t // H not in seen and t + H < n:
                    seen.add(t // H)
                    r = c[t + H] / c[t] - 1
                    rows2.append(dict(depth=past7[t] / sd42, total=-r, unusual=-(r - drift),
                                      strength=-(r - drift) / sd, fc=f[t]))
                prev = f[t]
    d2 = pd.DataFrame(rows2).dropna()
    def summ(g):
        return pd.Series(dict(n=len(g), total=g.total.mean(), unusual=g.unusual.mean(),
                              strength=g.strength.mean(),
                              t=g.total.mean() / (g.total.std() / np.sqrt(len(g)))))
    out["cases_by_depth_sd"] = d2.groupby(pd.qcut(d2.depth, 5)).apply(summ)
    out["cases_by_fc"] = d2.groupby(pd.qcut(d2.fc, 5, duplicates="drop")).apply(summ)
    return out
