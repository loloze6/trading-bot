def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            rs += list(c[idx + 48] / c[idx] - 1)
        d48 = np.mean(rs)
        allsd = np.std(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            fc = b["forecast"].values
            for i in np.where((ts.dt.weekday == 6) & (ts.dt.hour == 23))[0]:
                if i < 168 or i + 96 >= len(c): continue
                r = {"coin": coin, "year": ts[i].year, "fc": fc[i],
                     "wk": c[i] / c[i - 48] - 1, "prev5": c[i - 48] / c[i - 168] - 1,
                     "vr": v[i - 47:i + 1].mean() / v[i - 167:i - 47].mean(),
                     "f48": c[i + 48] / c[i] - 1, "f96": c[i + 96] / c[i] - 1,
                     "d48": d48, "sd": allsd,
                     "alloc_mean_48": a[i:i + 48].mean(),
                     "n_changes_48": (np.abs(np.diff(a[i:i + 49])) > 1e-9).sum()}
                rows.append(r)
    df = pd.DataFrame(rows)
    df["short_tot"] = -df["f48"]; df["short_unus"] = -(df["f48"] - df["d48"])
    df["short_tot96"] = -df["f96"]
    rise = df[df["wk"] > 0].copy()
    def s(g):
        x = g["short_tot"]; u = g["short_unus"]; y = g["short_tot96"]
        return pd.Series({"n": len(x), "tot48": x.mean(), "t48": x.mean() / (x.std() / np.sqrt(len(x))),
                          "unus48": u.mean(), "tot96": y.mean(), "t96": y.mean() / (y.std() / np.sqrt(len(y)))})
    rise["wkfell"] = np.where(rise["prev5"] < 0, "week_fell", "week_rose")
    out["rise_by_weekdir"] = rise.groupby("wkfell").apply(s)
    out["rise_weekfell_by_year"] = rise[rise["wkfell"] == "week_fell"].groupby("year").apply(s)
    out["rise_weekrose_by_year"] = rise[rise["wkfell"] == "week_rose"].groupby("year").apply(s)
    wf = rise[rise["wkfell"] == "week_fell"].copy()
    wf["q_fall"] = pd.qcut((wf["prev5"] / wf["sd"]).rank(method="first"), 3, labels=["big_fall", "mid", "small_fall"])
    out["rise_weekfell_by_fall_size"] = wf.groupby("q_fall").apply(s)
    wf["q_share"] = pd.qcut((wf["wk"] / wf["prev5"].abs()).rank(method="first"), 3, labels=["small_retrace", "mid", "big_retrace"])
    out["rise_weekfell_by_retrace_share"] = wf.groupby("q_share").apply(s)
    act = df[df["fc"] < 0]
    out["active_position_use"] = pd.Series({"mean_alloc_48": act["alloc_mean_48"].mean(),
        "mean_changes_48": act["n_changes_48"].mean(), "n": len(act)})
    return out
