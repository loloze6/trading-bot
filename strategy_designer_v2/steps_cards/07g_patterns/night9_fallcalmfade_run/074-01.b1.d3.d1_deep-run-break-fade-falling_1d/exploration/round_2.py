import pandas as pd, numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            n = len(b)
            prevdown = np.zeros(n, int); prevup = np.zeros(n, int)
            runloss = np.zeros(n); rungain = np.zeros(n)
            cd = cu = 0; ld = lu = 0.0
            for i in range(n):
                prevdown[i] = cd; prevup[i] = cu; runloss[i] = ld; rungain[i] = lu
                ri = r.iloc[i]
                if ri < 0:
                    cd += 1; ld += ri; cu = 0; lu = 0.0
                elif ri > 0:
                    cu += 1; lu += ri; cd = 0; ld = 0.0
                else:
                    cd = cu = 0; ld = lu = 0.0
            sd30 = r.rolling(30).std()
            agit = sd30 > sd30.expanding(30).median()
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt,
                "prevdown": prevdown, "prevup": prevup,
                "depth": -runloss / sd30.shift(1), "upd": rungain / sd30.shift(1),
                "tr60": c / c.shift(60) - 1, "agit": np.where(sd30.notna(), np.where(agit, "agit", "calm"), "na"),
                "tr20": c / c.shift(20) - 1,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "pos": b["postRebalance_current_allocation"].fillna(0)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["un"] = d["nxt"] - d["coin"].map(drift)
    d["trend"] = np.where(d.tr60 > 0.10, "rising", np.where(d.tr60 < -0.10, "falling", np.where(d.tr60.notna(), "choppy", "na")))
    d["tr20c"] = np.where(d.tr20 > 0.05, "up20", np.where(d.tr20 < -0.05, "dn20", np.where(d.tr20.notna(), "flat20", "na")))

    def summ(g):
        g = g.dropna(subset=["un"])
        x = g["un"]; s = g.groupby("day")["un"].sum(); nd = len(s)
        if len(x) < 8: return pd.Series({"n": len(x), "mean_pct": np.nan, "t_day": np.nan})
        return pd.Series({"n": len(x), "days": nd, "mean_pct": 100 * x.mean(),
                          "t_day": s.sum() / (np.sqrt(nd) * s.std(ddof=1))})
    out = {}
    rb = d[(d.r > 0) & (d.prevdown >= 2)].copy()
    rb = rb[rb.depth.notna()]
    rb["dq"] = pd.qcut(rb.depth, 3, labels=False)
    out["runbreak_trend_agit"] = rb.groupby(["trend", "agit"]).apply(summ)
    out["runbreak_trend_depthtercile"] = rb.groupby(["trend", "dq"]).apply(summ)
    out["runbreak_tr20_depthtercile"] = rb.groupby(["tr20c", "dq"]).apply(summ)
    # mirror: down day ending up run >=2
    db = d[(d.r < 0) & (d.prevup >= 2)].copy()
    db = db[db.upd.notna()]
    db["uq"] = pd.qcut(db.upd, 3, labels=False)
    out["upbreak_trend_upq"] = db.groupby(["trend", "uq"]).apply(summ)
    out["upbreak_tr20_upq"] = db.groupby(["tr20c", "uq"]).apply(summ)
    out["upbreak_trend_agit"] = db.groupby(["trend", "agit"]).apply(summ)
    # book: active days by agit and trend, short-side unusual
    act = d[d.pos != 0]
    out["active_trend_agit"] = act.groupby(["trend", "agit"]).apply(
        lambda g: pd.Series({"n": len(g), "short_un_pct": -100 * g.un.mean()}))
    out["n_trend_na_share"] = float((d.trend == "na").mean())
    return out
