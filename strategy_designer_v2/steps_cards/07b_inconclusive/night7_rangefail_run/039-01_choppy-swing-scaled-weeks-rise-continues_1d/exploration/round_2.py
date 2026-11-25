def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 15]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else 0.0
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r = pd.Series(cl).pct_change()
            sd30 = r.rolling(30).std()
            agit = sd30 > sd30.rolling(365, min_periods=60).median()
            raw = b.get("debug_info.components.swing_move.last_history_value")
            fc = b["forecast"].values
            for h in H:
                for i in range(0, len(cl), h):
                    if fc[i] == 0 or np.isnan(fc[i]):
                        continue
                    if i + h >= len(cl):
                        continue
                    rows.append({"coin": c, "win": w, "h": h, "fc": fc[i],
                                 "raw": raw.iloc[i] if raw is not None else np.nan,
                                 "agit": bool(agit.iloc[i]), "ts": b["timestamp"].iloc[i],
                                 "ex": cl[i + h] / cl[i] - 1 - drift[(c, h)]})
    df = pd.DataFrame(rows)
    df["side"] = np.sign(df["raw"].fillna(df["fc"]))

    def st(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        p = g.groupby("ts").agg(x=(x, "mean"), y=("ex", "mean"))
        if len(p) < 10:
            return pd.Series({"n_days": len(p), "cases": len(g), "t": np.nan, "dirmean": np.nan})
        res = stats.linregress(p["x"], p["y"])
        d = np.sign(g[x]) * g["ex"]
        dd = (np.sign(g[x]) * g["ex"]).groupby(g["ts"]).sum()
        return pd.Series({"n_days": len(p), "cases": len(g), "t": res.slope / res.stderr,
                          "dirmean": d.mean(), "dir_t_day": dd.mean() / dd.std(ddof=1) * np.sqrt(len(dd))})
    out = {}
    out["calm_by_h"] = df[~df.agit].groupby("h").apply(st)
    out["agit_by_h"] = df[df.agit].groupby("h").apply(st)
    out["raw_by_h"] = df.groupby("h").apply(lambda g: st(g, "raw"))
    out["calm_side_by_h"] = df[~df.agit].groupby(["h", "side"]).apply(st)
    out["calm_window_h5"] = df[(~df.agit) & (df.h == 5)].groupby("win").apply(st)
    out["share_agit_cases"] = df.groupby("h")["agit"].mean()
    return out
