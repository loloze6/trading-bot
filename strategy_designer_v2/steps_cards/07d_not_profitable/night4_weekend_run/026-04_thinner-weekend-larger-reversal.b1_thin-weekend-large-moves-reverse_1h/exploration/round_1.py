def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values
            n = len(b)
            # usual 48h move on grid
            g = np.arange(0, n - 48, 48)
            r48 = c[g + 48] / c[g] - 1
            for i in range(168, n):
                wd = ts.iloc[i].weekday(); hr = ts.iloc[i].hour
                if hr != 23 or wd not in (6, 2, 3):
                    continue
                past = c[i] / c[i - 48] - 1
                vr = np.log(v[i-47:i+1].mean() / max(v[i-167:i-47].mean(), 1e-12))
                f = {}
                for h in (12, 24, 48, 96):
                    f[h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(dict(coin=coin, w=w, wd=wd, past=past, vr=vr,
                                 f12=f[12], f24=f[24], f48=f[48], f96=f[96],
                                 sd=np.std(r48), mu=np.mean(r48), year=ts.iloc[i].year))
    d = pd.DataFrame(rows)
    d["pz"] = d["past"] / d["sd"]
    out = {}
    def reg(sub, col):
        s = sub.dropna(subset=[col])
        y = s[col] / s["sd"]
        if len(s) < 20: return (len(s), np.nan, np.nan)
        lr = stats.linregress(s["pz"], y)
        return (len(s), round(lr.slope, 4), round(lr.slope / lr.stderr, 2))
    res = []
    for name, sub in [("sun_all", d[d.wd == 6]), ("sun_thin", d[(d.wd == 6) & (d.vr < 0)]),
                      ("sun_heavy", d[(d.wd == 6) & (d.vr >= 0)]),
                      ("wed", d[d.wd == 2]), ("thu", d[d.wd == 3])]:
        for col in ("f12", "f24", "f48", "f96"):
            n_, sl, t = reg(sub, col)
            res.append(dict(group=name, h=col, n=n_, slope_on_pastz=sl, t=t))
    out["slope_future_on_past_z"] = pd.DataFrame(res)
    s = d[d.wd == 6].copy()
    s["qp"] = pd.qcut(s["pz"], 5, labels=False)
    s["dir_f48"] = -np.sign(s["past"]) * (s["f48"] - s["mu"])
    out["sun_by_pastz_quint"] = s.groupby("qp").agg(n=("f48", "count"), pz=("pz", "mean"),
        rev48=("dir_f48", "mean"), f48=("f48", "mean"), vr=("vr", "mean"))
    s["qv"] = pd.qcut(s["vr"], 4, labels=False)
    out["sun_by_volratio_q"] = s.groupby("qv").agg(n=("f48", "count"), vr=("vr", "mean"),
        rev48=("dir_f48", "mean"))
    pc = []
    for coin, sub in s.groupby("coin"):
        n_, sl, t = reg(sub, "f48"); pc.append(dict(coin=coin, n=n_, slope=sl, t=t))
    out["sun_by_coin"] = pd.DataFrame(pc)
    py = []
    for y, sub in s.groupby("year"):
        n_, sl, t = reg(sub, "f48"); py.append(dict(year=y, n=n_, slope=sl, t=t))
    out["sun_by_year"] = pd.DataFrame(py)
    # trades
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series({"n": len(tr), "gross_mean": tr["profit_loss_percent"].mean(),
        "net_mean": tr["net_profit_loss_percent"].mean(),
        "win_gross": (tr["profit_loss_percent"] > 0).mean(),
        "dur_h_mean": tr["duration_minutes"].mean() / 60})
    out["trades_by_side"] = tr.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    return out
