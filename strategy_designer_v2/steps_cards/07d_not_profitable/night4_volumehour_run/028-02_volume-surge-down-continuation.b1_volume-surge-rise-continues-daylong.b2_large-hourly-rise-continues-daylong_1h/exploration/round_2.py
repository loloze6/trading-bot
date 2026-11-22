def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coins = list(data["bars"].keys())
    H = 24
    # drift per coin: non-overlapping 24-bar grid returns over all windows
    drift, usual = {}, {}
    for c in coins:
        r = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            r.append(cl[idx + H] / cl[idx] - 1)
        r = np.concatenate(r); drift[c] = r.mean(); usual[c] = r.std()
    C = []; BB = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            f = b["forecast"].fillna(0).values
            fwd = cl.shift(-H) / cl - 1
            past30 = cl / cl.shift(720) - 1
            past7 = cl / cl.shift(168) - 1
            past1 = cl / cl.shift(24) - 1
            hr = cl.pct_change()
            vol7 = hr.rolling(168).std()
            vol30 = hr.rolling(720).std()
            # cases: first forecast rise >=2 from lowest long level since last flat, once per 24-bar grid cell
            low = 0.0; taken = set()
            for i in range(len(b)):
                if f[i] <= 0: low = 0.0; continue
                low = min(low, f[i]) if low > 0 else low
                if f[i] - low >= 2:
                    cell = i // H
                    if cell not in taken and not np.isnan(fwd.iloc[i]):
                        taken.add(cell)
                        C.append({"coin": c, "window": w, "ex": fwd.iloc[i] - drift[c], "tot": fwd.iloc[i],
                                  "f": f[i], "p30": past30.iloc[i], "p7": past7.iloc[i], "p1": past1.iloc[i],
                                  "vr": vol7.iloc[i] / vol30.iloc[i]})
                    low = f[i]
            # bar-level book: position x next return, by trailing 30d return state
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos * (cl.shift(-1) / cl - 1)
            BB.append(pd.DataFrame({"g": g, "pos": pos, "p30": past30, "p7": past7, "vr": vol7 / vol30}))
    C = pd.DataFrame(C); BB = pd.concat(BB, ignore_index=True).dropna()
    def summ(g):
        return pd.Series({"n": len(g), "ex": g.ex.mean(), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                          "tot": g.tot.mean()})
    out = {}
    out["cases_all"] = summ(C)
    out["cases_by_p30_q"] = C.dropna(subset=["p30"]).groupby(pd.qcut(C.p30.dropna(), 5, labels=False)).apply(summ)
    out["cases_by_p7_q"] = C.dropna(subset=["p7"]).groupby(pd.qcut(C.p7.dropna(), 5, labels=False)).apply(summ)
    out["cases_by_volratio_q"] = C.dropna(subset=["vr"]).groupby(pd.qcut(C.vr.dropna(), 5, labels=False)).apply(summ)
    out["cases_by_forecast_q"] = C.groupby(pd.qcut(C.f, 5, labels=False, duplicates="drop")).apply(summ)
    def bs(g):
        return pd.Series({"bars": len(g), "share_long": (g.pos > 0).mean(), "mean_pos": g.pos.mean(),
                          "gain_per_bar_bp": g.g.mean() * 1e4, "share_of_total_gain": g.g.sum()})
    q = pd.qcut(BB.p30, 5, labels=False)
    r = BB.groupby(q).apply(bs); r["share_of_total_gain"] /= BB.g.sum()
    out["book_bars_by_p30_q"] = r
    q = pd.qcut(BB.vr, 5, labels=False)
    r = BB.groupby(q).apply(bs); r["share_of_total_gain"] /= BB.g.sum()
    out["book_bars_by_volratio_q"] = r
    out["drift_usual"] = pd.DataFrame({"drift": drift, "usual": usual})
    return out
