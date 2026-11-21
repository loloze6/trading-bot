def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [18, 36]
    rows = []; base = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            hi, lo, c = df["high"], df["low"], df["close"]
            ph = hi.shift(1).rolling(12).max()
            pl = lo.shift(1).rolling(12).min()
            brk = ((c - ph).clip(lower=0) / c * 100)
            mom = c / c.shift(180) - 1
            year = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"].values
            n = len(df); cv = c.values
            for start in range(0, n - 18, 18):
                # baseline: every grid-start bar
                t0 = start
                if not np.isnan(mom.iloc[t0]) and t0 + 18 < n:
                    rb = {"coin": coin, "mom": mom.iloc[t0], "year": year.iloc[t0]}
                    for h in H:
                        rb[f"u{h}"] = cv[t0 + h] / cv[t0] - 1 - drift[(coin, h)][0] if t0 + h < n else np.nan
                    base.append(rb)
                pick = None
                for t in range(start, min(start + 18, n)):
                    if fc[t] >= 2 and (t == 0 or fc[t - 1] < fc[t] - 2 + 1e-9):
                        pick = t; break
                if pick is None: continue
                t = pick
                r = {"coin": coin, "year": year.iloc[t], "brk": brk.iloc[t], "mom": mom.iloc[t]}
                for h in H:
                    r[f"u{h}"] = cv[t + h] / cv[t] - 1 - drift[(coin, h)][0] if t + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows).dropna(subset=["mom"]); b = pd.DataFrame(base)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    edges = d["mom"].quantile([0, .2, .4, .6, .8, 1]).values; edges[0] = -9; edges[-1] = 99
    d["mq"] = pd.cut(d["mom"], edges, labels=False); b["mq"] = pd.cut(b["mom"], edges, labels=False)
    out = {}
    out["brk_vs_all_by_momq_18"] = d.groupby("mq").apply(summ).join(b.groupby("mq").apply(summ), rsuffix="_all")
    out["brk_vs_all_by_momq_36"] = d.groupby("mq").apply(lambda g: summ(g, "u36")).join(b.groupby("mq").apply(lambda g: summ(g, "u36")), rsuffix="_all")
    d["up"] = d["mom"] > 0
    d["bq"] = pd.qcut(d["brk"].rank(method="first"), 3, labels=False)
    out["mom_sign_x_brk_tercile_18"] = d.groupby(["up", "bq"]).apply(summ)
    up = d[d["up"]]
    out["mom_up_by_year_18"] = up.groupby("year").apply(summ)
    out["mom_up_by_coin_18"] = up.groupby("coin").apply(summ)
    out["corr_mom_u18_brk_vs_all"] = pd.Series({"breakouts": d[["mom", "u18"]].corr().iloc[0, 1], "all_bars": b[["mom", "u18"]].corr().iloc[0, 1]})
    return out
