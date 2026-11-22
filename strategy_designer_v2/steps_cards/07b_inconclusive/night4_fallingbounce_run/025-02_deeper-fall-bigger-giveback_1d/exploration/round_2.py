def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [5, 10, 20]
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            r = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                r += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(r), np.std(r))
    recs = {h: [] for h in H}
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            jump = r1 / r1.rolling(20, min_periods=10).std()
            raw = df.get("debug_info.components.fall_depth.last_history_value")
            r90 = c / c.shift(90) - 1
            if raw is not None:
                r90 = r90.where(raw.isna(), raw / 100.0)
            sel = (jump >= 2)
            for h in H:
                seen = set()
                for i in np.where(sel.values)[0]:
                    if i + h >= len(c) or pd.isna(r90.iloc[i]):
                        continue
                    cell = i // h
                    key = (cell, r90.iloc[i] < 0)
                    if key in seen:
                        continue
                    seen.add(key)
                    f = c.iloc[i + h] / c.iloc[i] - 1
                    m, s = drift[(coin, h)]
                    recs[h].append({"coin": coin, "fall": r90.iloc[i] < 0, "r90": r90.iloc[i],
                                    "jump": jump.iloc[i], "u": f - m, "z": (f - m) / s, "f": f})
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    for h in H:
        ev = pd.DataFrame(recs[h])
        out[f"h{h}_fall_vs_rise"] = ev.groupby("fall")["u"].apply(summ).unstack()
        a = ev[ev.fall]["u"]; b = ev[~ev.fall]["u"]
        out[f"h{h}_welch_fall_minus_rise"] = pd.Series({"diff": a.mean() - b.mean(), "t": stats.ttest_ind(a, b, equal_var=False).statistic})
        out[f"h{h}_fall_strength"] = float(ev[ev.fall]["z"].mean())
        fe = ev[ev.fall].copy()
        fe["jq"] = pd.qcut(fe["jump"].rank(method="first"), 3, labels=["small", "mid", "big"])
        out[f"h{h}_fall_by_jump"] = fe.groupby("jq")["u"].apply(summ).unstack()
        fe["rq"] = pd.qcut(fe["r90"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
        out[f"h{h}_fall_by_depth"] = fe.groupby("rq")["u"].apply(summ).unstack()
        sl = stats.linregress(fe["jump"], fe["u"])
        out[f"h{h}_fall_slope_u_on_jump"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr})
        if h == 10:
            out["h10_fall_by_coin"] = fe.groupby("coin")["u"].apply(summ).unstack()
    return out
