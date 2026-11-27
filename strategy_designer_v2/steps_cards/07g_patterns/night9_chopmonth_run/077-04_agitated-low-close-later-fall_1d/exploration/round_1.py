def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            n = len(b)
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            rng = h - l
            cl = np.where(rng > 0, (c - l) / rng, np.nan)  # 1 at high, 0 at low
            r1 = pd.Series(c).pct_change().values
            def fwd(a, k):
                out = np.full(n, np.nan)
                if n > a + k:
                    out[:n - a - k] = c[a + k:] / c[:n - a - k] - 1 if a == 0 else c[a + k:][:n-a-k] / c[a:][:n-a-k] - 1
                return out
            f1 = fwd(0, 1); f6 = fwd(0, 6); f7 = fwd(0, 7)
            # next-day close to day7 close
            f1to7 = np.full(n, np.nan)
            if n > 7:
                f1to7[:n - 7] = c[7:] / c[1:n - 6] - 1
            ret5 = np.full(n, np.nan); ret5[5:] = c[5:] / c[:-5] - 1
            ret20 = np.full(n, np.nan); ret20[20:] = c[20:] / c[:-20] - 1
            ret60 = np.full(n, np.nan); ret60[60:] = c[60:] / c[:-60] - 1
            vol20 = pd.Series(r1).rolling(20).std().values
            relrng = rng / c
            relrng20 = pd.Series(relrng).rolling(20).median().values
            reg = b["regime"].astype(str).values
            # regime on bar t+1 reflects agitation at t+1; use bar's own regime as agitation proxy
            agit = reg != "chop"
            wd = pd.to_datetime(b["timestamp"]).dt.weekday.values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            pos = np.arange(n)
            for i in range(n):
                rows.append((coin, w, pos[i], cl[i], r1[i], f1[i], f6[i], f7[i], f1to7[i], ret5[i], ret20[i], ret60[i],
                             vol20[i], relrng[i] / relrng20[i] if relrng20[i] and not np.isnan(relrng20[i]) else np.nan,
                             agit[i], wd[i], yr[i], b["postRebalance_current_allocation"].values[i]))
    df = pd.DataFrame(rows, columns=["coin","w","pos","cl","r1","f1","f6","f7","f1to7","ret5","ret20","ret60","vol20","rngratio","agit","wd","yr","alloc"])
    # drift per coin for horizons on grid
    out = {}
    def grid(d, h):
        return d[d["pos"] % h == 0]
    for h, col in [(1, "f1"), (6, "f6")]:
        g = grid(df, h)
        dr = g.groupby("coin")[col].mean()
        df[col + "_x"] = df[col] - df["coin"].map(dr)
    g7 = grid(df, 7); dr7 = g7.groupby("coin")["f1to7"].mean()
    df["f1to7_x"] = df["f1to7"] - df["coin"].map(dr7)
    def tab(d, by, col, h):
        g = grid(d, h).dropna(subset=[col])
        res = g.groupby(by)[col].agg(["mean", "count", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res.round(4)
    df["clq"] = pd.cut(df["cl"], [-0.01, .2, .4, .6, .8, 1.01], labels=["q0low", "q1", "q2", "q3", "q4high"])
    out["f6x_by_cl_agit"] = tab(df, ["agit", "clq"], "f6_x", 6)
    out["f1x_by_cl_agit"] = tab(df, ["agit", "clq"], "f1_x", 1)
    out["f1to7x_by_cl_agit"] = tab(df, ["agit", "clq"], "f1to7_x", 7)
    # big moves
    df["r1q"] = df.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["f6x_by_r1q_agit"] = tab(df, ["agit", "r1q"], "f6_x", 6)
    out["f1x_by_r1q_agit"] = tab(df, ["agit", "r1q"], "f1_x", 1)
    df["r20q"] = df.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["f6x_by_r20q_agit"] = tab(df, ["agit", "r20q"], "f6_x", 6)
    df["rrq"] = df.groupby("coin")["rngratio"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["f6x_by_rangeratio_agit"] = tab(df, ["agit", "rrq"], "f6_x", 6)
    out["f1x_by_wd"] = tab(df, ["wd"], "f1_x", 1)
    # trend60 known
    df["tr"] = np.where(df["ret60"] > .1, "rising", np.where(df["ret60"] < -.1, "falling", np.where(df["ret60"].notna(), "choppy", "na")))
    out["f6x_by_trend_agit_clq"] = tab(df[df["tr"] != "na"], ["tr", "agit", "clq"], "f6_x", 6)
    # book daily returns: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    out["share_days_agit"] = float(df["agit"].mean())
    out["book_ret_by_window"] = D.groupby("w")["book_return"].agg(["mean", "count"]).round(5)
    return out
