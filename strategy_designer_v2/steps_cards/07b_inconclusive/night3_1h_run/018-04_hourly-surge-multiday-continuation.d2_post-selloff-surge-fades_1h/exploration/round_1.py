def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [24, 72, 120, 240]
    rows = []
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
            c = df["close"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            f = df["forecast"].fillna(0).values
            s = pd.Series(c)
            r24 = s / s.shift(24) - 1
            surge = (r24 / r24.abs().rolling(720, min_periods=720).mean()).values
            p7 = (s.shift(24) / s.shift(192) - 1).values
            # cases by forecast rule
            ref = 0.0; seen = set()
            for t in range(n):
                if f[t] == 0:
                    ref = 0.0; continue
                if f[t] <= ref - 2:
                    ref = f[t]
                    cell = t // 120
                    if cell not in seen:
                        seen.add(cell)
                        rec = dict(coin=coin, w=w, yr=yr[t], kind="case", depth=abs(f[t]), p7=p7[t], surge=surge[t])
                        for h in H:
                            rec[f"r{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)][0]) if t + h < n else np.nan
                        rows.append(rec)
                elif f[t] > ref:
                    ref = max(ref, f[t]) if ref < 0 else ref
            # surge events (any prior7 sign), first bar of a run, once per 120-grid cell
            on = (surge >= 3)
            seen2 = set()
            for t in range(1, n):
                if on[t] and not on[t - 1] and not np.isnan(p7[t]):
                    cell = t // 120
                    if cell in seen2: continue
                    seen2.add(cell)
                    rec = dict(coin=coin, w=w, yr=yr[t], kind="up_after_fall" if p7[t] < 0 else "up_after_rise",
                               depth=np.nan, p7=p7[t], surge=surge[t])
                    for h in H:
                        rec[f"r{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)][0]) if t + h < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"r{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    cases = d[d.kind == "case"].copy()
    cases["s120"] = -cases["r120"]
    cases["dq"] = pd.qcut(cases["depth"], 4, labels=False, duplicates="drop")
    cases["p7q"] = pd.qcut(cases["p7"], 4, labels=False, duplicates="drop")
    cases["sq"] = pd.qcut(cases["surge"], 3, labels=False, duplicates="drop")
    ev = d[d.kind != "case"].copy()
    ev["p7q"] = pd.qcut(ev["p7"], 5, labels=False, duplicates="drop")
    return {
        "cases_overall_long_dir": summ(cases).to_frame().T,
        "cases_by_coin_long_dir": cases.groupby("coin").apply(summ),
        "cases_by_year_long_dir": cases.groupby("yr").apply(summ),
        "cases_by_depth_q": cases.groupby("dq").apply(summ),
        "cases_by_p7_q": cases.groupby("p7q").apply(summ),
        "cases_by_surge_q": cases.groupby("sq").apply(summ),
        "events_by_kind": ev.groupby("kind").apply(summ),
        "events_by_p7_quintile": ev.groupby("p7q").apply(summ),
        "events_p7q_mean": ev.groupby("p7q")["p7"].mean(),
        "events_upfall_by_coin": ev[ev.kind=="up_after_fall"].groupby("coin").apply(summ),
        "events_upfall_by_year": ev[ev.kind=="up_after_fall"].groupby("yr").apply(summ),
    }
