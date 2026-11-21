def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}
    for coin, ws in data["bars"].items():
        rs = [np.diff(np.log(b["close"].values.astype(float))) for b in ws.values()]
        drift[coin] = np.mean(np.concatenate(rs))
    # book decomposition: market part vs timing, per coin daily
    dec = []
    for coin, ws in data["bars"].items():
        mu = drift[coin]
        for w, b in ws.items():
            c = b["close"].astype(float).values
            pos = b["postRebalance_current_allocation"].astype(float).values
            g = pos[:-1] * (c[1:] / c[:-1] - 1)
            mk = pos[:-1] * mu
            dec.append({"coin": coin, "gross_hourly_bps": g.mean() * 1e4, "market_hourly_bps": mk.mean() * 1e4,
                        "mean_pos": pos.mean(), "share_bars_short": (pos < -1e-6).mean(),
                        "turnover_per_day": np.abs(np.diff(pos)).sum() / (len(pos) / 24)})
    dd = pd.DataFrame(dec)
    out["book_decomp_by_coin"] = dd.groupby("coin").mean()
    # thinned cases: down crossings z<=-1, at most one per 120h per coin-window, graded by z and by 30d return
    rows = []
    for coin, ws in data["bars"].items():
        mu = drift[coin]
        for w, b in ws.items():
            c = b["close"].astype(float).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / scale
            r30 = c / c.shift(720) - 1
            r30s = r30 / (r24.abs().rolling(720, min_periods=120).mean() * np.sqrt(30))
            cond = z <= -1.0
            first = cond & ~cond.shift(1, fill_value=False)
            last = -10**9
            for i in np.where(first.values)[0]:
                if i - last < 120:
                    continue
                last = i
                rec = {"coin": coin, "z": z[i], "r30s": r30s[i]}
                for h in (24, 72, 120, 240):
                    if i + h < len(c):
                        rec[f"x{h}"] = (c[i + h] / c[i] - 1) - ((1 + mu) ** h - 1)
                rows.append(rec)
    df = pd.DataFrame(rows).dropna(subset=["r30s"])
    df["zbin"] = pd.cut(-df["z"], [1, 1.5, 2.5, 100])
    df["r30bin"] = pd.qcut(df["r30s"], 4, labels=["q1_down", "q2", "q3", "q4_up"])
    def summ(g):
        d = {}
        for h in (24, 72, 120, 240):
            x = g[f"x{h}"].dropna()
            d[f"m{h}_bps"] = x.mean() * 1e4
            d[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        d["n"] = len(g)
        return pd.Series(d)
    out["thin_by_zbin"] = df.groupby("zbin", observed=True).apply(summ)
    out["thin_by_r30q"] = df.groupby("r30bin", observed=True).apply(summ)
    out["thin_r30q_x_zbin"] = df.groupby(["r30bin", "zbin"], observed=True).apply(summ)
    out["corr_r30s_x120"] = df[["r30s", "x120"]].corr().iloc[0, 1]
    out["corr_z_x72"] = df[["z", "x72"]].corr().iloc[0, 1]
    return out
