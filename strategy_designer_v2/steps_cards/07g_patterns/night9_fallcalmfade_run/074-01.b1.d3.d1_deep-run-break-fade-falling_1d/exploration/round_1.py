import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            up = r > 0
            dn = r < 0
            # run of down closes before today
            run = np.zeros(len(b), dtype=int)
            cnt = 0
            prevrun = np.zeros(len(b), dtype=int)
            for i in range(len(b)):
                prevrun[i] = cnt
                if dn.iloc[i]:
                    cnt += 1
                else:
                    cnt = 0
                run[i] = cnt
            uprun = np.zeros(len(b), dtype=int); cnt = 0; prevup = np.zeros(len(b), dtype=int)
            for i in range(len(b)):
                prevup[i] = cnt
                cnt = cnt + 1 if up.iloc[i] else 0
            tr60 = c / c.shift(60) - 1
            sd30 = r.rolling(30).std()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"])
            df = pd.DataFrame({
                "coin": coin, "w": w, "r": r, "nxt": nxt, "up": up, "dn": dn,
                "prevdown": prevrun, "prevup": prevup, "tr60": tr60, "z": r / sd30,
                "sd30": sd30, "rng": rng / sd30, "clpos": clpos,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fc": b["forecast"], "pos": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["un"] = d["nxt"] - d["coin"].map(drift)
    d["trend"] = np.where(d.tr60 > 0.10, "rising", np.where(d.tr60 < -0.10, "falling", np.where(d.tr60.notna(), "choppy", "na")))

    def summ(g):
        x = g["un"].dropna()
        n = len(x)
        if n < 5:
            return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        # day clustered t
        s = g.dropna(subset=["un"]).groupby("day")["un"].sum()
        nd = len(s)
        t = x.mean() / (s.std(ddof=1) * np.sqrt(nd) / x.sum() * x.mean()) if x.sum() != 0 else np.nan
        tc = s.sum() / (np.sqrt(nd) * s.std(ddof=1)) if nd > 2 else np.nan
        return pd.Series({"n": n, "days": nd, "mean_pct": 100 * x.mean(), "t_day": tc})

    out = {}
    # run-break up day by trend and run length
    rb = d[d.up & (d.prevdown >= 1)].copy()
    rb["runb"] = rb.prevdown.clip(upper=4)
    out["runbreak_by_trend_run"] = rb.groupby(["trend", "runb"]).apply(summ)
    # mirror: first down day after up run, next-day unusual move (long side positive = un)
    db = d[d.dn & (d.prevup >= 1)].copy()
    db["runb"] = db.prevup.clip(upper=4)
    out["downbreak_by_trend_run"] = db.groupby(["trend", "runb"]).apply(summ)
    # after large moves by z quintile, by trend
    d["zq"] = pd.qcut(d.z, 5, labels=False)
    out["z_quint_by_trend"] = d[d.trend != "na"].groupby(["trend", "zq"]).apply(summ)
    # weekday
    out["weekday"] = d.groupby("wd").apply(summ)
    # range quintile x close position
    d["rq"] = pd.qcut(d.rng, 3, labels=False)
    d["cq"] = pd.qcut(d.clpos, 3, labels=False)
    out["range_x_closepos"] = d.groupby(["rq", "cq"]).apply(summ)
    # book's position days
    act = d[d.pos.fillna(0) != 0]
    out["active_by_year"] = act.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "mean_short_pct": -100 * g.nxt.mean()}))
    return out
