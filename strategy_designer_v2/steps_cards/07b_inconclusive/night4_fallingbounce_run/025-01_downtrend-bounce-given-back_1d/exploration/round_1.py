def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # drift per horizon: non-overlapping returns over all windows
        dd = {}
        for h in [1, 2, 3, 5, 10]:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            dd[h] = np.mean(rs)
        drift[coin] = dd
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            r1 = pd.Series(c).pct_change()
            sd20 = r1.rolling(20, min_periods=10).std()
            z = (r1 / sd20).values
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            reg = b["regime"].values
            raw = b.get("debug_info.components.bounce.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            # cases: fall of forecast >=2 vs previous bar, first per 5-bar cell
            seen = set()
            for t in range(1, n):
                if f[t] - f[t - 1] <= -2 and f[t] < 0:
                    cell = t // 5
                    if cell in seen: continue
                    seen.add(cell)
                    rec = dict(coin=coin, win=w, year=yr[t], f=f[t], z=z[t], raw=raw[t], kind="case")
                    for h in [1, 2, 3, 5, 10]:
                        rec[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                    rows.append(rec)
            # all big-z rises on grid (regime vs not), non-overlapping 5-bar grid
            for t in range(0, n - 5, 5):
                if np.isfinite(z[t]) and z[t] > 1.5:
                    rec = dict(coin=coin, win=w, year=yr[t], f=f[t], z=z[t], raw=np.nan,
                               kind="bigrise_" + ("fall" if reg[t] == "mean_reversion" else "other"))
                    for h in [1, 2, 3, 5, 10]:
                        rec[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                    rows.append(rec)
    df = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in [1, 2, 3, 5, 10]:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    cs = df[df.kind == "case"].copy()
    res = {}
    res["cases_all"] = summ(cs).to_frame().T
    res["by_coin"] = cs.groupby("coin").apply(summ)
    res["by_year"] = cs.groupby("year").apply(summ)
    cs["fq"] = pd.qcut(cs["f"].abs().rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    res["by_absforecast_quartile"] = cs.groupby("fq").apply(summ)
    cs["zq"] = pd.qcut(cs["z"].rank(method="first"), 4, labels=["z1", "z2", "z3", "z4"])
    res["by_rawz_quartile"] = cs.groupby("zq").apply(summ)
    res["zq_mean_z"] = cs.groupby("zq")["z"].mean()
    res["bigrise_fall_vs_other"] = df[df.kind != "case"].groupby("kind").apply(summ)
    return res
