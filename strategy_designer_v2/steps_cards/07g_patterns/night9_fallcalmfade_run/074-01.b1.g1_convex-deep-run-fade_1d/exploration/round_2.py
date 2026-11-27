import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            run = np.zeros(len(b)); cnt = 0
            runloss = np.zeros(len(b)); acc = 0.0
            for i in range(len(b)):
                run[i] = cnt; runloss[i] = acc
                if r.iloc[i] < 0:
                    cnt += 1; acc += -np.log(1 + r.iloc[i])
                else:
                    cnt = 0; acc = 0.0
            sd30 = r.rolling(30, min_periods=20).std().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "r": r, "nxt": nxt, "run": run,
                "depth": runloss / sd30, "sd30": sd30,
                "falling": (b["regime"] != "chop").astype(int),
                "ret60": c / c.shift(60) - 1,
                "wd": ts.dt.weekday, "dkey": ts.dt.normalize().astype("int64"),
                "rz": r / sd30,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["agit"] = (d.groupby("coin")["sd30"].rank(pct=True) > 0.5).astype(int)
    d["trend"] = np.where(d.falling == 1, "falling",
                  np.where(d.ret60 > 0.10, "rising", np.where(d.ret60.notna(), "choppy", "unk")))

    def summ(g):
        g = g.dropna(subset=["ex"])
        x = g["ex"]; n = len(x)
        if n < 3: return pd.Series({"n": n, "mean_ex%": np.nan, "t_day": np.nan, "days": np.nan})
        dev = (x - x.mean()).groupby(g["dkey"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "mean_ex%": 100 * x.mean(), "t_day": x.mean() / se, "days": len(dev)})

    out = {}
    brk = d[(d.r > 0) & (d.run >= 1)].copy()
    brk["runb"] = pd.cut(brk["run"], [0, 1, 2, 4, 30], labels=["1", "2", "3-4", "5+"])
    out["break_by_trend"] = brk.groupby("trend").apply(summ)
    out["break_by_trend_agit"] = brk.groupby(["trend", "agit"]).apply(summ)
    out["break_by_trend_runb"] = brk.groupby(["trend", "runb"]).apply(summ)
    nf = brk[brk.trend.isin(["choppy", "rising"])].copy()
    nf["depthq"] = pd.qcut(nf["depth"], 4, labels=False, duplicates="drop")
    out["break_choppyrising_depthq"] = nf.groupby(["trend", "depthq"]).apply(summ)
    # weekday: falling breaks vs falling other days vs non-falling breaks
    d["isbrk"] = ((d.r > 0) & (d.run >= 1)).astype(int)
    out["falling_alldays_wd_nonbreak"] = d[(d.falling == 1) & (d.isbrk == 0)].groupby("wd").apply(summ)
    out["nonfalling_break_wd"] = brk[brk.falling == 0].groupby("wd").apply(summ)
    out["falling_break_wkend_vs_mid"] = brk[brk.falling == 1].assign(
        g=lambda x: np.where(x.wd.isin([0, 1, 5]), "MonTueSat", "other")).groupby("g").apply(summ)
    # large-down rebound by trend & agit (check held)
    big = d[d.rz < -2]
    out["bigdown_by_trend_agit"] = big.groupby(["trend", "agit"]).apply(summ)
    # moderate up days (0,1] sd in falling: break vs not
    mu = d[(d.rz > 0)]
    mu = mu.assign(rzb=pd.cut(mu.rz, [0, 1, 2, 99]))
    out["falling_up_by_isbrk_size"] = mu[mu.falling == 1].groupby(["isbrk", "rzb"]).apply(summ)
    # book's largest days: weekday share
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    act = dd[dd.book_return.abs() > 1e-9]
    out["book_active_by_wd"] = act.groupby("wd")["book_return"].agg(["count", "mean", "sum"])
    return out
