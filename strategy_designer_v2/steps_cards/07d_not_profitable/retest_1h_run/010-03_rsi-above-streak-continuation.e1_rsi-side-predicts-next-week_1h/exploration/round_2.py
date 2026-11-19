def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; cases = []; tv = []
    for coin, wins in data["bars"].items():
        allr = []
        tmp = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            d = c.diff(); up = d.clip(lower=0); dn = (-d).clip(lower=0)
            au = up.ewm(alpha=1/336, adjust=False).mean(); ad = dn.ewm(alpha=1/336, adjust=False).mean()
            rsi = 100 - 100 / (1 + au / ad)
            dist = rsi - 50
            chg = rsi - rsi.shift(168)
            f = b["forecast"]
            ok = dist.notna() & chg.notna() & f.notna()
            if ok.sum() > 100:
                X = np.column_stack([np.ones(ok.sum()), dist[ok] / dist[ok].std(), chg[ok] / chg[ok].std()])
                beta = np.linalg.lstsq(X, f[ok].values, rcond=None)[0]
                rows.append(dict(coin=coin, b_level=beta[1], b_change14d=beta[2],
                                 corr_f_level=np.corrcoef(f[ok], dist[ok])[0, 1],
                                 corr_f_change=np.corrcoef(f[ok], chg[ok])[0, 1]))
            idx = np.arange(0, len(b) - 168, 168)
            for i in idx:
                fr = c.iloc[i + 168] / c.iloc[i] - 1
                tmp.append(dict(coin=coin, w=w, dist=dist.iloc[i], chg=chg.iloc[i], f=f.iloc[i], fr=fr))
            a = b["postRebalance_current_allocation"].fillna(0)
            dA = (a - b["previous_allocation"].fillna(0)).abs()
            tv.append(dict(coin=coin, share_turn_small=dA[dA < 0.05].sum() / dA.sum(),
                           share_turn_signflip=dA[np.sign(a) != np.sign(b["previous_allocation"].fillna(0))].sum() / dA.sum(),
                           bars_traded=(dA > 0).mean()))
        T = pd.DataFrame(tmp); T["ex"] = T["fr"] - T["fr"].mean()
        cases.append(T)
    out["forecast vs RSI level and 7d change"] = pd.DataFrame(rows).groupby("coin").mean()
    C = pd.concat(cases).dropna()
    res = {}
    for name, s in [("forecast/10", C["f"] / 10), ("rsi-50 scaled", C["dist"] / C["dist"].std()),
                    ("rsi 7d change scaled", C["chg"] / C["chg"].std())]:
        p = s * C["ex"]
        res[name] = dict(mean=p.mean(), t=p.mean() / (p.std() / np.sqrt(len(p))), n=len(p))
    out["168h product by signal"] = pd.DataFrame(res).T
    C["q"] = pd.qcut(C["dist"], 5, labels=False)
    out["168h excess by RSI-50 quintile"] = C.groupby("q").agg(dist=("dist", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    out["turnover"] = pd.DataFrame(tv).groupby("coin").mean()
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin))
    D = pd.concat(dd)
    out["daily"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    return out
