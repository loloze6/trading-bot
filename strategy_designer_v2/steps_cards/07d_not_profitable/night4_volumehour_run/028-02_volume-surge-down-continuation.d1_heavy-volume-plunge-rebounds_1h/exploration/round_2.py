def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = [4, 12, 24, 48]
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
    recs = {h: [] for h in H}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            v = pd.Series(b["volume"].values.astype(float))
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(720, min_periods=200).std().shift(1)
            vr = v / v.rolling(720, min_periods=200).mean().shift(1)
            z = (r1 / sd).values
            vrv = vr.values
            sdv = sd.values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                fr = c[idx + h] / c[idx] - 1
                for k, t in enumerate(idx):
                    if not np.isfinite(z[t]) or not np.isfinite(vrv[t]) or z[t] >= 0:
                        continue
                    recs[h].append((coin, w, -z[t], vrv[t], -z[t] * vrv[t], sdv[t], fr[k], fr[k] - drift[(coin, h)][0], drift[(coin, h)][1]))
    def tt(x):
        x = np.asarray(x); x = x[np.isfinite(x)]
        return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    res = []
    vrres = []
    volres = []
    for h in H:
        df = pd.DataFrame(recs[h], columns=["coin", "w", "fz", "vr", "s", "sd", "tot", "u", "usual"])
        df["sq"] = pd.qcut(df["s"].rank(method="first"), [0, .5, .8, .9, .95, .98, .995, 1], labels=["<50", "50-80", "80-90", "90-95", "95-98", "98-99.5", ">99.5"])
        for q, g in df.groupby("sq", observed=True):
            res.append({"h": h, "score_pct": q, "n": len(g), "s_mean": g["s"].mean(), "tot%": g["tot"].mean() * 100, "u%": g["u"].mean() * 100,
                        "t_u": tt(g["u"]), "strength": (g["u"] / g["usual"]).mean()})
        big = df[df["fz"] >= 2]
        big = big.assign(vq=pd.qcut(big["vr"].rank(method="first"), 3, labels=["lowvol", "midvol", "highvol"]))
        for q, g in big.groupby("vq", observed=True):
            vrres.append({"h": h, "fall>=2sd volume": q, "n": len(g), "vr": g["vr"].mean(), "tot%": g["tot"].mean() * 100, "t_u": tt(g["u"])})
        top = df[df["s"] >= df["s"].quantile(0.95)]
        top = top.assign(dq=top.groupby("coin")["sd"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False)))
        for q, g in top.groupby("dq"):
            volres.append({"h": h, "top5% score, 30d vol tercile": q, "n": len(g), "tot%": g["tot"].mean() * 100, "t_u": tt(g["u"])})
    out["by_score_pct"] = pd.DataFrame(res)
    out["big_falls_by_volume"] = pd.DataFrame(vrres)
    out["top5_by_vol_regime"] = pd.DataFrame(volres)
    tr = pd.concat([t.assign(coin=c) for c, wins in data["trades"].items() for t in wins.values() if len(t)])
    tr["fb"] = pd.cut(tr["entry_forecast"], [-0.01, 0.01, 0.5, 2, 5, 10, 20.01])
    g = tr.groupby("fb", observed=True)
    out["trades_by_entry_forecast"] = pd.DataFrame({"n": g.size(), "gross%": g["profit_loss_percent"].mean(), "net%": g["net_profit_loss_percent"].mean(), "dur_h": g["duration_minutes"].mean() / 60})
    return out
