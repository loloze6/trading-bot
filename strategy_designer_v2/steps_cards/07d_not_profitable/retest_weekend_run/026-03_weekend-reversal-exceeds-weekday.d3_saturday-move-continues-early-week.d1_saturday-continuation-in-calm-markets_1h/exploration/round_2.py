def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; c_side = 0.00095
    cases = []; grid = []; daily = {k: [] for k in ["full", "long_only", "long_only_7d", "full_7d"]}
    for c in bars:
        # drift on grid
        rets = []
        for w, b in bars[c].items():
            cl = b["close"].values
            rets += list(cl[48::48] / cl[:-48:48] - 1) if len(cl) > 48 else []
        drift = np.nanmean(rets)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values; n = len(cl)
            f = b["forecast"].fillna(0).values
            reg = b["regime"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            sun23 = (ts.dt.weekday.values == 6) & (ts.dt.hour.values == 23)
            keep_long = np.ones(n); keep_7 = np.ones(n)
            for j in np.where(sun23)[0]:
                if j < 168 or j + 48 >= n: continue
                fut = cl[j+48] / cl[j] - 1 - drift
                sat = cl[j-24] / cl[j-48] - 1
                p7 = cl[j] / cl[j-168] - 1
                calm = reg[j] == "trending"
                cases.append(dict(coin=c, calm=calm, sig=f[j] != 0, side=np.sign(f[j]) if f[j] != 0 else np.sign(sat),
                                  fut=fut, p7=p7, sat=sat, year=ts.iloc[j].year))
                if f[j] != 0:
                    s = np.sign(f[j])
                    if s * p7 < 0: keep_7[j:j+49] = 0
            # momentum alone on grid
            for j in range(168, n - 48, 48):
                p7 = cl[j] / cl[j-168] - 1
                grid.append(dict(dirret=np.sign(p7) * (cl[j+48] / cl[j] - 1 - drift), calm=reg[j] == "trending"))
            r1 = np.concatenate([cl[1:] / cl[:-1] - 1, [0]])
            for name, aa in [("full", a), ("long_only", np.clip(a, 0, None)),
                             ("long_only_7d", np.clip(a, 0, None) * keep_7), ("full_7d", a * keep_7)]:
                prev = np.concatenate([[aa[0]], aa[:-1]])
                g = aa * r1 - np.abs(aa - prev) * c_side
                v = np.cumprod(1 + g)
                dser = pd.Series(v, index=ts.dt.floor("D").values).groupby(level=0).last()
                dr = dser.pct_change().dropna()
                daily[name].append(pd.DataFrame({"wn": int(w[1:]), "day": dr.index, "r": dr.values}))
    C = pd.DataFrame(cases)
    S = C[C.sig].copy(); S["d"] = S.side * S.fut
    def tt(x): return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 1 else np.nan})
    out["cases by side (dir de-drifted 48h)"] = S.groupby("side")["d"].apply(tt).unstack()
    out["cases by side and year"] = S.groupby(["year", "side"])["d"].mean().unstack()
    # long-only check: calm Sundays regardless of Saturday sign, raw long
    calm = C[C.calm]
    out["calm sundays: long de-drifted, by saturday sign"] = calm.groupby(np.sign(calm.sat))["fut"].apply(tt).unstack()
    out["all calm sundays long"] = tt(calm["fut"])
    out["non-calm sundays: long, by sat sign"] = C[~C.calm].groupby(np.sign(C[~C.calm].sat))["fut"].apply(tt).unstack()
    # 7d condition
    S["p7agree"] = np.sign(S.p7) == S.side
    out["cases by side & 7d agrees"] = S.groupby(["side", "p7agree"])["d"].apply(tt).unstack()
    G = pd.DataFrame(grid)
    out["7d momentum alone, 48h grid"] = G.groupby("calm")["dirret"].apply(tt).unstack()
    res = {}
    for name, L in daily.items():
        Dd = pd.concat(L); P = Dd.groupby(["wn", "day"])["r"].mean().reset_index().sort_values(["wn", "day"])
        eq = (1 + P.r).cumprod(); mdd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(P)) - 1
        res[name] = dict(sharpe=P.r.mean() / P.r.std() * np.sqrt(365), yearly=yr, mdd=mdd, calmar=yr / -mdd,
                         worst_w=P.assign(dd=(eq / eq.cummax() - 1).values).groupby("wn").dd.min().idxmin())
    out["rebuilt books"] = pd.DataFrame(res).T
    return out
