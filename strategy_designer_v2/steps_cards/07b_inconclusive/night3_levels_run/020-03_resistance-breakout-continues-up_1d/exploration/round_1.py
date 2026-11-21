import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    H = [1, 3, 5, 10, 20]
    for coin, wins in data["bars"].items():
        # normal drift per horizon: non-overlapping over all windows
        drift = {}; usual = {}
        for h in H:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr); usual[h] = np.std(rr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            c = b["close"].values
            raw = b.get("debug_info.components.res_break.last_history_value")
            raw = raw.values if raw is not None else np.full(len(b), np.nan)
            # past 90-day return as regime
            p90 = pd.Series(c).pct_change(90).values
            p20 = pd.Series(c).pct_change(20).values
            lowest = 0.0; seen = set()
            for t in range(len(b)):
                if f[t] <= 0:
                    lowest = 0.0
                    continue
                lowest = min(lowest, f[t])
                if f[t] - lowest >= 2:
                    cell = t // 5
                    if cell in seen:
                        lowest = f[t]; continue
                    seen.add(cell)
                    r = {"coin": coin, "win": int(w[1:]), "f": f[t], "raw": raw[t],
                         "p90": p90[t], "p20": p20[t],
                         "year": pd.Timestamp(b["timestamp"].iloc[t]).year}
                    for h in H:
                        r[f"x{h}"] = (c[t + h] / c[t] - 1 - drift[h]) if t + h < len(c) else np.nan
                        r[f"tot{h}"] = (c[t + h] / c[t] - 1) if t + h < len(c) else np.nan
                    rows.append(r)
                    lowest = f[t]
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["x5"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "median": x.median(), "hit": (x > 0).mean()})
    out = {}
    out["all"] = summ(d)
    hz = {}
    for h in H:
        x = d[f"x{h}"].dropna(); hz[h] = {"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "tot": d[f"tot{h}"].mean()}
    out["by_horizon"] = pd.DataFrame(hz).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["rawq"] = pd.qcut(d["raw"].rank(method="first"), 5, labels=False)
    out["by_raw_quint"] = d.groupby("rawq").apply(summ).join(d.groupby("rawq")["raw"].median().rename("rawmed"))
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=False)
    out["by_fc_quart"] = d.groupby("fq").apply(summ).join(d.groupby("fq")["f"].median().rename("fmed"))
    d["p90q"] = pd.qcut(d["p90"].rank(method="first"), 4, labels=False)
    out["by_p90_quart"] = d.groupby("p90q").apply(summ).join(d.groupby("p90q")["p90"].median().rename("p90med"))
    d["p20q"] = pd.qcut(d["p20"].rank(method="first"), 4, labels=False)
    out["by_p20_quart"] = d.groupby("p20q").apply(summ).join(d.groupby("p20q")["p20"].median().rename("p20med"))
    out["by_window"] = d.groupby("win").apply(summ)
    return out
