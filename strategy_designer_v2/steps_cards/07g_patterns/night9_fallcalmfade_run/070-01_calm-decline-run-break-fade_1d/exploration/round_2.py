def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            down = (r < 0).values
            drun = np.zeros(len(b))
            for i in range(1, len(b)):
                drun[i] = drun[i-1] + 1 if down[i] else 0
            pdrun = pd.Series(drun).shift(1)
            ts = pd.to_datetime(b["timestamp"])
            tr60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            vol20 = r.rolling(20).std()
            rng = (b["high"] - b["low"]) / c.shift(1)
            clpos = (c - b["low"]) / (b["high"] - b["low"])
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt, "pdrun": pdrun,
                               "tr60": tr60, "vol30": vol30, "z": r / vol20,
                               "infc": (b["regime"] != "chop").values, "year": ts.dt.year,
                               "clpos": clpos, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r"])
    A["un"] = A["nxt"] - A.groupby("coin")["nxt"].transform("mean")
    med = A.groupby("coin")["vol30"].transform("median")
    A["agit"] = np.where(A["vol30"] > med, "agitated", "calm")
    A["trend"] = np.where(A["tr60"].isna(), "na", np.where(A["tr60"] > 0.10, "rising", np.where(A["tr60"] < -0.10, "falling", "choppy")))
    def dayt(g):
        x = g["un"]
        if len(x) < 5: return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean_un%": 100*x.mean(), "t_day": np.nan})
        dev = (x - x.mean()).groupby(g["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev**2).sum() * D/(D-1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean_un%": 100*x.mean(), "t_day": x.mean()/se})
    out = {}
    rb = A[(A["r"] > 0) & (A["pdrun"] >= 1)].copy()
    rb["g"] = np.where(rb["pdrun"] >= 2, "run2+", "run1")
    out["runbreak by trend/agit/runs"] = rb.groupby(["trend", "agit", "g"]).apply(dayt)
    out["runbreak run2+ by year"] = rb[rb["g"] == "run2+"].groupby("year").apply(dayt)
    out["runbreak run2+ by window"] = rb[rb["g"] == "run2+"].groupby("w").apply(dayt)
    out["runbreak run2+ by coin"] = rb[rb["g"] == "run2+"].groupby("coin").apply(dayt)
    out["runbreak all by run"] = rb.assign(rb5=rb["pdrun"].clip(upper=5)).groupby("rb5").apply(dayt)
    # graded: correlation run length vs un
    s = rb.dropna(subset=["un"])
    out["runbreak spearman run vs un (all)"] = float(stats.spearmanr(s["pdrun"], s["un"])[0])
    out["runbreak spearman run vs un (outside fc)"] = float(stats.spearmanr(s[~s["infc"]]["pdrun"], s[~s["infc"]]["un"])[0])
    # does the size of the up day or its close position matter
    rb2 = rb[rb["g"] == "run2+"].copy()
    rb2["zq"] = pd.qcut(rb2["z"], 3, labels=["small", "mid", "big"])
    out["run2+ by up-day size"] = rb2.groupby("zq").apply(dayt)
    rb2["cq"] = pd.qcut(rb2["clpos"], 3, labels=["low", "mid", "high"])
    out["run2+ by close pos"] = rb2.groupby("cq").apply(dayt)
    # low-close rebound and big-fall rebound by trend/agit (to see if held)
    lc = A[A["clpos"] < A["clpos"].quantile(0.2)]
    out["low close nxt by trend/agit"] = lc.groupby(["trend", "agit"]).apply(dayt)
    # weekday by year
    A["wd"] = A["day"].dt.weekday
    out["thu+fri nxt by year"] = A[A["wd"].isin([3, 4])].groupby("year").apply(dayt)
    return out
