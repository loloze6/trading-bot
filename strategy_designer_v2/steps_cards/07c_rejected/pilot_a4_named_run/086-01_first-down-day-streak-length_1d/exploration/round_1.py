import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r).rolling(30, min_periods=10).std().values
            inprof = (b["regime"] != "chop").values
            up = 0; runret = 0.0
            for t in range(1, len(c)):
                if r[t] > 0:
                    up += 1; runret = (1 + runret) * (1 + r[t]) - 1
                    continue
                if r[t] < 0 and up >= 1:
                    d = dict(coin=coin, win=w, t=t, run=up, runret=runret,
                             runz=runret / vol[t] if vol[t] > 0 else np.nan,
                             downz=r[t] / vol[t] if vol[t] > 0 else np.nan,
                             prof=inprof[t], fc=b["forecast"].iloc[t],
                             year=pd.Timestamp(b["timestamp"].iloc[t]).year)
                    for h in H:
                        if t + h < len(c):
                            dm, ds = drift[(coin, h)] if (coin, h) in drift else (0, 1)
                            d[f"u{h}"] = -(c[t + h] / c[t] - 1 - dm)  # short direction unusual
                            d[f"s{h}"] = d[f"u{h}"] / ds
                        else:
                            d[f"u{h}"] = np.nan; d[f"s{h}"] = np.nan
                    rows.append(d)
                up = 0; runret = 0.0
    df = pd.DataFrame(rows)
    # drift is computed lazily per coin before windows; fine
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"mean_u{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["drift"] = pd.Series({f"{k[0]}_{k[1]}": v[0] for k, v in drift.items()})
    df["runb"] = df["run"].clip(upper=5)
    res["by_prof_run"] = df[df.run >= 2].groupby(["prof", "runb"]).apply(summ)
    res["prof_run1_vs_2plus"] = df.groupby(["prof", df.run >= 2]).apply(summ)
    p = df[(df.prof) & (df.run >= 2)].copy()
    res["prof_by_coin"] = p.groupby("coin").apply(summ)
    res["prof_by_year"] = p.groupby("year").apply(summ)
    p["runzq"] = pd.qcut(p["runz"], 3, labels=False, duplicates="drop")
    p["downzq"] = pd.qcut(p["downz"], 3, labels=False, duplicates="drop")
    res["prof_by_runz_tercile"] = p.groupby("runzq").apply(summ)
    res["prof_by_downz_tercile(0=deepest)"] = p.groupby("downzq").apply(summ)
    allp = df[df.prof].copy()
    for v in ["run", "runz", "downz"]:
        for h in [3, 5]:
            x = allp[[v, f"u{h}"]].dropna()
            s = stats.linregress(x[v], x[f"u{h}"])
            res.setdefault("slopes_inprof_all_runs", {})[f"{v}_u{h}"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(x)}"
    res["slopes_inprof_all_runs"] = pd.Series(res["slopes_inprof_all_runs"])
    return res
