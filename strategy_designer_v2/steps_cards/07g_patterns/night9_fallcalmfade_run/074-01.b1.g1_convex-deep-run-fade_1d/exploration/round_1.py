import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            down = (r < 0).astype(int)
            # run length of down closes ending at previous bar
            run = np.zeros(len(b)); cnt = 0
            runloss = np.zeros(len(b)); acc = 0.0
            for i in range(len(b)):
                run[i] = cnt; runloss[i] = acc
                if r.iloc[i] < 0:
                    cnt += 1; acc += -np.log(1 + r.iloc[i])
                else:
                    cnt = 0; acc = 0.0
            sd30 = r.rolling(30, min_periods=20).std().shift(1)
            df = pd.DataFrame({
                "coin": coin, "win": w, "r": r, "nxt": nxt, "nxt2": nxt2,
                "run": run, "depth": runloss / sd30, "sd30": sd30,
                "falling": (b["regime"] != "chop").astype(int),
                "regime": b["regime"], "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "rz": r / sd30,
                "rng": (b["high"] - b["low"]) / c / sd30,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["sdcoin"] = d["coin"].map(d.groupby("coin")["r"].std())
    d["exz"] = d["ex"] / d["sdcoin"]
    # agitation proxy: sd30 rank within coin
    d["agit"] = (d.groupby("coin")["sd30"].rank(pct=True) > 0.5).astype(int)
    out = {}

    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    brk = d[(d["r"] > 0) & (d["run"] >= 1)].copy()
    brk["runb"] = pd.cut(brk["run"], [0, 1, 2, 3, 5, 30], labels=["1", "2", "3", "4-5", "6+"])
    out["break_by_falling_run"] = brk.groupby(["falling", "runb"]).apply(summ)
    brk["depthq"] = brk.groupby("falling")["depth"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["break_by_falling_depthq"] = brk.groupby(["falling", "depthq"]).apply(summ)
    brk["upq"] = brk.groupby("falling")["rz"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["break_by_falling_upsize"] = brk.groupby(["falling", "upq"]).apply(summ)
    out["break_by_falling_agit"] = brk.groupby(["falling", "agit"]).apply(summ)
    brk["clq"] = pd.cut(brk["clpos"], [0, .5, .8, 1.01])
    out["break_falling_closepos"] = brk[brk.falling == 1].groupby("clq").apply(summ)
    # all days: next-day after a large move by profile
    d["rzq"] = pd.cut(d["rz"], [-99, -2, -1, 0, 1, 2, 99])
    out["all_by_falling_rz"] = d.groupby(["falling", "rzq"]).apply(summ)
    out["all_by_falling_agit"] = d.groupby(["falling", "agit"]).apply(summ)
    # up days not breaking a run (run==0) in falling
    up0 = d[(d.r > 0) & (d.run == 0)].copy()
    up0["upq"] = up0.groupby("falling")["rz"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["upday_norun_by_falling_upsize"] = up0.groupby(["falling", "upq"]).apply(summ)
    out["break_falling_weekday"] = brk[brk.falling == 1].groupby("wd").apply(summ)
    out["break_falling_by_win"] = brk[brk.falling == 1].groupby("win").apply(summ)
    # two-day outcome
    b2 = brk[brk.falling == 1]
    out["break_falling_day2_runb"] = b2.groupby("runb")["nxt2"].agg(["count", "mean"])
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["book_by_coin"] = dd.groupby("coin")["book_return"].agg(["count", "mean", "std"])
    return out
