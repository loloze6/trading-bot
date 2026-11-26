import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []; allrows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
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
            r20 = c/c.shift(20) - 1
            wd = ts.dt.weekday
            yr = ts.dt.year
            raw = b.get("debug_info.components.gain20.last_history_value")
            df = pd.DataFrame({"coin": coin, "w": w, "wd": wd, "yr": yr, "nxt": nxt, "ex": nxt - mu,
                               "r20": r20, "fc": b["forecast"], "raw": raw,
                               "day": ts.dt.floor("D")})
            allrows.append(df)
    A = pd.concat(allrows).dropna(subset=["nxt"])
    F = A[(A.wd == 4)]
    P = F[F.fc > 0].copy()
    out = {}
    out["n_fri_pos"] = len(P)
    # forecast quintile per coin
    P["q"] = P.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    g = P.groupby("q")["ex"]
    out["by_fc_quintile"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size())), "share_up": P.groupby("q")["nxt"].apply(lambda s: (s>0).mean())})
    g = P.groupby("coin")["ex"]
    out["by_coin"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    g = P.groupby("yr")["ex"]
    out["by_year"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # Friday negative-gain cases (forecast 0) using raw r20 within window
    Fz = F.dropna(subset=["r20"])
    Fz = Fz.assign(side=np.where(Fz.r20 > 0, "up20", "down20"))
    g = Fz.groupby("side")["ex"]
    out["fri_by_r20_sign"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # Every weekday: r20 up vs down next-day excess
    Az = A.dropna(subset=["r20"])
    Az = Az.assign(up=Az.r20 > 0)
    g = Az.groupby(["wd", "up"])["ex"]
    out["weekday_x_r20up"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # Saturday unconditional
    g = A.groupby("wd")["ex"]
    out["by_weekday_all"] = pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # raw scaled gain deciles on Fridays (positive)
    Pr = P.dropna(subset=["raw"])
    if len(Pr) > 50:
        Pr = Pr.assign(rq=pd.qcut(Pr.raw.rank(method="first"), 5, labels=False))
        g = Pr.groupby("rq")
        out["by_raw_quintile"] = pd.DataFrame({"n": g.size(), "raw_mean": g.raw.mean(), "mean_ex": g.ex.mean(), "t": g.ex.mean()/(g.ex.std()/np.sqrt(g.size()))})
        out["corr_raw_ex_spearman"] = float(stats.spearmanr(Pr.raw, Pr.ex).correlation)
    out["corr_fc_ex_spearman"] = float(stats.spearmanr(P.fc, P.ex).correlation)
    return out
