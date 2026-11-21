def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # portfolio daily series per window
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("coin", "count")).reset_index().sort_values(["wn", "day"])
    P = P.dropna(subset=["book"])
    P["pos"] = P.groupby("wn").cumcount()
    eq = (1 + P["book"]).cumprod()
    dd_ = eq / eq.cummax() - 1
    P["dd"] = dd_.values
    P["eq"] = eq.values
    out["deepest_fall"] = float(dd_.min())
    # per-window summary
    ws = P.groupby("wn").agg(book=("book", lambda x: (1 + x).prod() - 1), hold=("hold", lambda x: (1 + x).prod() - 1), mindd=("dd", "min"), ndays=("book", "size"))
    out["per_window"] = ws
    # locate the deepest fall: peak and trough windows
    i_tr = int(np.argmin(dd_.values))
    i_pk = int(np.argmax(eq.values[:i_tr + 1]))
    out["fall_peak_trough"] = pd.DataFrame({"wn": [P["wn"].iloc[i_pk], P["wn"].iloc[i_tr]], "pos": [P["pos"].iloc[i_pk], P["pos"].iloc[i_tr]]}, index=["peak", "trough"])
    # trade features
    tr = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            for _, r in t.iterrows():
                et = pd.to_datetime(r["entry_time"])
                idx = ts.searchsorted(et, side="right") - 1
                if idx < 0: continue
                f = {"coin": c, "w": w, "net": r["net_profit_loss_percent"], "ef": r["entry_forecast"]}
                f["r26"] = cl[idx] / cl[idx - 26] - 1 if idx >= 26 else np.nan
                f["r7"] = cl[idx] / cl[idx - 7] - 1 if idx >= 7 else np.nan
                f["r90"] = cl[idx] / cl[idx - 90] - 1 if idx >= 90 else np.nan
                if idx >= 30:
                    lr = np.diff(np.log(cl[idx - 30: idx + 1]))
                    f["vol30"] = lr.std() * np.sqrt(365)
                else:
                    f["vol30"] = np.nan
                if idx >= 100:
                    f["ma100"] = cl[idx] / cl[idx - 100: idx + 1].mean() - 1
                else:
                    f["ma100"] = np.nan
                f["dur"] = r["duration_minutes"] / 1440
                tr.append(f)
    T = pd.DataFrame(tr)
    out["n_trades"] = len(T)
    out["trade_net_desc"] = T["net"].describe()
    res = {}
    for col in ["r7", "r26", "r90", "vol30", "ma100", "ef"]:
        s = T.dropna(subset=[col])
        q = pd.qcut(s[col], 4, labels=False, duplicates="drop")
        g = s.groupby(q)["net"].agg(["mean", "count"])
        for k, v in g.iterrows():
            res[(col, int(k))] = (v["mean"], v["count"], s[col][q == k].median())
    out["net_by_quartile"] = pd.DataFrame(res, index=["mean_net", "n", "median_feat"]).T
    T["wn"] = T["w"].str[1:].astype(int)
    out["trades_by_window"] = T.groupby("wn")["net"].agg(["mean", "sum", "count"])
    # concurrent positions: share of coins long per day in fall vs not
    P["infall"] = P["dd"] < -0.15
    out["book_vs_hold_in_fall"] = P.groupby("infall")[["book", "hold"]].mean()
    return out
