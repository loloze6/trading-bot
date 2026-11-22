import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; trades = data["trades"]
    H = [5, 10]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            s = pd.Series(cl)
            r30 = (s / s.shift(30) - 1).values
            r10 = (s / s.shift(10) - 1).values
            ma50 = (s / s.rolling(50).mean() - 1).values
            f90 = b["debug_info.components.fall90.last_history_value"].values
            f = b["forecast"].values
            n = len(b)
            for start in range(0, n, 5):
                sel = [i for i in range(start, min(start + 5, n)) if f[i] <= -2]
                if not sel: continue
                i = sel[0]
                d = {"r30": r30[i], "r10": r10[i], "ma50": ma50[i], "f90": f90[i]}
                for h in H:
                    if i + h < n:
                        d[f"tot{h}"] = -(cl[i + h] / cl[i] - 1)
                        d[f"unu{h}"] = d[f"tot{h}"] + drift[(c, h)]
                rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g):
        o = {"n": len(g)}
        for h in H:
            x = g[f"tot{h}"].dropna(); o[f"tot{h}"] = x.mean(); o[f"t_tot{h}"] = x.mean() / (x.std() / np.sqrt(len(x)))
        x = g["unu5"].dropna(); o["unu5"] = x.mean()
        return pd.Series(o)
    res = {}
    for col in ["r30", "r10", "ma50"]:
        d2 = df.dropna(subset=[col]).copy()
        d2["q"] = pd.qcut(d2[col], 5, labels=False, duplicates="drop")
        t = d2.groupby("q").apply(summ)
        t["lo"] = d2.groupby("q")[col].min(); t["hi"] = d2.groupby("q")[col].max()
        res[f"cases_by_{col}_quintile"] = t
    # slope of total 5d move on r30
    d2 = df.dropna(subset=["r30", "tot5"])
    sl = np.polyfit(d2["r30"], d2["tot5"], 1)
    res["slope_tot5_on_r30"] = float(sl[0])
    res["corr_tot5_r30"] = float(d2[["r30", "tot5"]].corr().iloc[0, 1])
    # trades by duration
    tr = pd.concat([t for c in trades for t in trades[c].values()])
    tr["dur_d"] = tr["duration_minutes"] / 1440
    tr["db"] = pd.cut(tr["dur_d"], [-1, 4.5, 5.5, 10.5, 20.5, 1000])
    res["trades_by_duration"] = tr.groupby("db")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # position held on bars with forecast 0 vs negative
    rows2 = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            r = b["close"].pct_change().shift(-1)
            rows2.append(pd.DataFrame({"fneg": b["forecast"] < 0, "pos": b["postRebalance_current_allocation"], "g": b["postRebalance_current_allocation"] * r, "reg": b["regime"]}))
    bb = pd.concat(rows2); bb = bb[bb.pos < 0]
    res["short_bars_by_forecast_and_regime"] = bb.groupby(["fneg", "reg"])["g"].agg(["count", "mean", "sum"])
    res["mean_short_size"] = float(bb.pos.mean())
    return res
