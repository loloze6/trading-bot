def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]
    allb = []
    for c in bars:
        drifts = []; per = {}
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].values
            for h in [1, 2, 3, 5]:
                x = np.full(len(b), np.nan); x[:-h] = cl[h:] / cl[:-h] - 1; b[f"f{h}"] = x
            drifts += list(b["f5"].values[::5][~np.isnan(b["f5"].values[::5])])
            b["loc"] = (b["close"] - b["low"]) / (b["high"] - b["low"])
            b["ret5"] = b["close"].pct_change(5)
            b["ret1"] = b["close"].pct_change()
            hl = b["high"] - b["low"]
            b["rm"] = hl / hl.rolling(20).mean()
            b["vol20"] = b["ret1"].rolling(20).std()
            b["inprof"] = b["regime"] != "chop"
            b["g"] = np.arange(len(b)) % 5 == 0
            b["coin"] = c; b["w"] = w
            b["day"] = b["timestamp"].astype(str).str[:10]
            per[w] = b
        drift = np.mean(drifts)
        for w, b in per.items():
            b["drift"] = drift; allb.append(b)
    A = pd.concat(allb)
    A["sit"] = A["inprof"] & (A["loc"] >= 0.5) & (A["ret5"] < 0)
    def tt(s, d):
        s = s.dropna(); d = d.loc[s.index]
        m = s.mean(); dev = (s - m).groupby(d.values).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"um": m, "t": m / se, "n": len(s), "days": G})
    A = A.reset_index(drop=True)
    A["um5"] = -(A["f5"] - A["drift"])
    # all bars (overlapping) by group, informative only, day-clustered
    A["wide"] = A["rm"] > 1.3
    grp = {}
    P = A[A["inprof"]].dropna(subset=["rm", "loc", "ret5"])
    for name, m in {"sit_wide": P["sit"] & P["wide"], "sit_narrow": P["sit"] & ~P["wide"],
                    "wide_not_sit": ~P["sit"] & P["wide"], "notsit_notwide": ~P["sit"] & ~P["wide"],
                    "wide_lowclose": P["wide"] & (P["loc"] < 0.5), "wide_up_ret5pos": P["wide"] & (P["loc"] >= 0.5) & (P["ret5"] >= 0)}.items():
        sub = P[m]; grp[name] = tt(sub["um5"], sub["day"])
    out["in-profile all bars, 5d short unusual (clustered by day)"] = pd.DataFrame(grp).T
    gs = P[P["g"]]
    grp2 = {}
    for name, m in {"sit_wide": gs["sit"] & gs["wide"], "sit_narrow": gs["sit"] & ~gs["wide"],
                    "wide_not_sit": ~gs["sit"] & gs["wide"]}.items():
        sub = gs[m]; grp2[name] = tt(sub["um5"], sub["day"])
    out["grid only"] = pd.DataFrame(grp2).T
    # horizon profile on sit bars, all bars
    S = P[P["sit"]]
    hz = {}
    for h in [1, 2, 3, 5]:
        hz[f"h{h}"] = tt(-S[f"f{h}"], S["day"])
    out["sit horizons all bars (raw short)"] = pd.DataFrame(hz).T
    # trades: entry features, path
    T = []
    for c in trades:
        for w, t in trades[c].items():
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T).reset_index(drop=True)
    T["eday"] = pd.to_datetime(T["entry_time"]).dt.strftime("%Y-%m-%d")
    key = A.set_index(["coin", "w", "day"])
    feats = []
    for i, r in T.iterrows():
        try:
            row = key.loc[(r["coin"], r["w"], r["eday"])]
            if isinstance(row, pd.DataFrame): row = row.iloc[0]
            feats.append({"rm": row["rm"], "loc": row["loc"], "ret5": row["ret5"], "ret1": row["ret1"], "vol20": row["vol20"],
                          "s1": -row["f1"], "s2": -row["f2"], "s3": -row["f3"]})
        except KeyError:
            feats.append({})
    F = pd.DataFrame(feats); T = pd.concat([T, F], axis=1)
    T["net"] = T["net_profit_loss_percent"]
    out["trade feature match"] = T["rm"].notna().mean()
    for col in ["rm", "ret5", "ret1", "loc", "vol20"]:
        q = pd.qcut(T[col], 3, labels=["lo", "mid", "hi"], duplicates="drop")
        out[f"trades by {col} tercile"] = T.groupby(q, observed=True).agg(net=("net", "mean"), med=("net", "median"),
                                                                          win=("net", lambda x: (x > 0).mean()), n=("net", "size"),
                                                                          s1=("s1", "mean"), s2=("s2", "mean"))
    out["trade path means %"] = (T[["s1", "s2", "s3"]].mean() * 100).to_frame("short ret").assign(gross5=T["profit_loss_percent"].mean())
    out["trades by year"] = T.groupby(pd.to_datetime(T["entry_time"]).dt.year)["net"].agg(["mean", "sum", "count"])
    out["trades by window"] = T.groupby("w")["net"].agg(["mean", "sum", "count"])
    # loss after day1 against: if day1 goes against, what do days 2-5 do
    T["after1"] = (1 - T["profit_loss_percent"] / 100) / (1 - T["s1"]) - 1  # approx coin move days1->5
    T["d1adverse"] = T["s1"] < 0
    out["day1 adverse vs rest"] = T.groupby("d1adverse").agg(n=("net", "size"), net=("net", "mean"),
                                                             rest_coin_move=("after1", "mean"))
    return out
