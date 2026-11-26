def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30: continue
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l).replace(0, np.nan)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "pos": np.arange(len(b)),
                "cl": (c - l) / rng,
                "body": (c - o) / rng,
                "ret": r, "vol20": r.rolling(20).std(),
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "inprof": (b["regime"] != "chop").astype(int),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["day"] = df["ts"].dt.floor("D")
    df["sr"] = df["ret"] / df["vol20"]
    for k in ["nxt", "nxt3"]:
        df["u_" + k] = df[k] - df.groupby("coin")[k].transform("mean")
    def summ(g, col="u_nxt"):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 3: return pd.Series({"n": n})
        dd = g.groupby("day")[col].sum()
        t = dd.mean() / (dd.std() / np.sqrt(len(dd))) if len(dd) > 2 else np.nan
        return pd.Series({"n": n, "days": len(dd), "mean%": 100 * g[col].mean(), "t_day": t})
    out = {}
    p = df[df["inprof"] == 1].copy()
    p = p.dropna(subset=["sr", "cl"])
    p["srb"] = pd.cut(p["sr"], [-99, -1, 0, 0.5, 1, 1.5, 2.5, 99])
    out["prof_sr_bins_1d"] = p.groupby("srb").apply(summ)
    p3 = p[p["pos"] % 3 == 0]
    out["prof_sr_bins_3d_nonoverlap"] = p3.groupby("srb").apply(lambda g: summ(g, "u_nxt3"))
    p["clh"] = (p["cl"] >= 0.5).astype(int)
    p["up"] = (p["ret"] > 0).astype(int)
    out["prof_up_x_highclose"] = p.groupby(["up", "clh"]).apply(summ)
    up = p[p["ret"] > 0]
    out["prof_up_sr_x_cl"] = up.groupby([pd.cut(up["sr"], [0, 0.75, 1.5, 99]), pd.cut(up["cl"], [-0.01, 0.5, 0.75, 1.01])]).apply(summ)
    # graded: correlation on up days in profile
    gg = up.dropna(subset=["u_nxt"])
    out["prof_up_corr_sr_next"] = float(np.corrcoef(gg["sr"].clip(upper=4), gg["u_nxt"])[0, 1])
    out["prof_up_n"] = len(gg)
    # outside profile: high close fade by own trend
    q = df[(df["inprof"] == 0)].dropna(subset=["tr60", "cl"]).copy()
    q["trend"] = pd.cut(q["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    q["clq"] = pd.cut(q["cl"], [-0.01, 0.25, 0.75, 1.01], labels=["low", "mid", "high"])
    out["outprof_trend_x_cl"] = q.groupby(["trend", "clq"]).apply(summ)
    q["upb"] = pd.cut(q["sr"], [-99, 0, 0.5, 1, 1.5, 2.5, 99])
    out["outprof_trend_x_sr"] = q.groupby(["trend", "upb"]).apply(summ)
    out["prof_up_by_year"] = up[(up["sr"] > 0.5)].groupby(up["ts"].dt.year).apply(summ)
    out["prof_up_by_coin"] = up[(up["sr"] > 0.5)].groupby("coin").apply(summ)
    return out
