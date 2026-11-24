import pandas as pd, numpy as np
from scipy import stats

def tstat(s):
    s = s.dropna()
    return s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan

def explore(data):
    allrows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            rets.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(rets))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            nxt = c.shift(-1)/c - 1
            nxt2 = c.shift(-2)/c - 1
            r20 = c/c.shift(20) - 1
            raw = b.get("debug_info.components.gain20.last_history_value")
            allrows.append(pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday, "yr": ts.dt.year,
                "nxt": nxt, "ex": nxt - mu, "ex2": nxt2 - 2*mu, "r20": r20, "fc": b["forecast"], "raw": raw,
                "day": ts.dt.floor("D")}))
    A = pd.concat(allrows).dropna(subset=["nxt"])
    P = A[(A.wd == 4) & (A.fc > 0)].copy()
    out = {}
    # step-5-like top fifth per coin
    def top(g):
        k = int(np.ceil(0.2*len(g)))
        g = g.sort_values("fc", ascending=False, kind="stable")
        return pd.Series({"top_mean": g.ex.iloc[:k].mean(), "rest_mean": g.ex.iloc[k:].mean(),
                          "top_median": g.ex.iloc[:k].median(), "rest_median": g.ex.iloc[k:].median(), "k": k})
    out["top_vs_rest_by_coin"] = P.groupby("coin").apply(top)
    P["q"] = P.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    g = P.groupby("q")["ex"]
    clip = P.ex.clip(P.ex.quantile(0.02), P.ex.quantile(0.98))
    P["exw"] = clip
    out["quintile_robust"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "median": g.median(),
        "winsor_mean": P.groupby("q")["exw"].mean(), "std": g.std(), "max": g.max(), "min": g.min()})
    # weighted by forecast vs equal-weight
    out["fc_weighted_mean_ex"] = float((P.fc*P.ex).sum()/P.fc.sum())
    out["equal_mean_ex"] = float(P.ex.mean())
    # first half years vs second half
    P["half"] = np.where(P.yr <= 2021, "2018-2021", "2022-2025")
    g = P.groupby(["half", "q"])["ex"]
    out["quintile_by_half"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.apply(tstat)})
    # horizon 2 days (Fri close -> Sun close), Friday r20 > 0 vs <= 0
    F = A[A.wd == 4].dropna(subset=["r20", "ex2"])
    F = F.assign(up=F.r20 > 0)
    g = F.groupby("up")["ex2"]
    out["fri_2day_by_up"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.apply(tstat)})
    # Friday r20 quintiles (all Fridays, signed, per coin) next-day excess
    F1 = A[A.wd == 4].dropna(subset=["r20"]).copy()
    F1["rq"] = F1.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    g = F1.groupby("rq")
    out["fri_r20_quintiles_all"] = pd.DataFrame({"n": g.size(), "r20_mean": g.r20.mean(), "mean_ex": g.ex.mean(),
        "median_ex": g.ex.median(), "t": g.ex.apply(tstat)})
    out["spearman_r20_ex_allfri"] = float(stats.spearmanr(F1.r20, F1.ex).correlation)
    # day-clustered t for up20 Fridays
    U = F1[F1.r20 > 0]
    d = U.groupby("day")["ex"].sum()
    out["up20_day_clustered"] = pd.Series({"n_cases": len(U), "days": len(d),
        "mean": U.ex.mean(), "t_cluster": d.mean()/(d.std()/np.sqrt(len(d)))*1.0 * (len(U)/len(d))**0 })
    return out
