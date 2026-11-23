import pandas as pd, numpy as np
from scipy import stats

def tt(x):
    x = pd.Series(x).dropna()
    if len(x) < 3:
        return pd.Series({"mean_bp": np.nan, "t": np.nan, "n": len(x)})
    return pd.Series({"mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x))), "n": len(x)})

def explore(data):
    out = {}
    rows = []
    hr = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values; n = len(b)
            hours = ts.dt.hour.values; wds = ts.dt.weekday.values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # past 24h rolling abs vol for regime
            s = pd.Series(r1)
            vol24 = s.abs().rolling(24).mean().values
            vol720 = s.abs().rolling(720).mean().values
            hr.append(pd.DataFrame({"coin": coin, "window": w, "hour": hours, "wd": wds,
                                    "year": ts.dt.year.values, "r1": r1,
                                    "vreg": vol24 / vol720}))
            # case per day: bar starting 20:00 (closing 21:00) -> forward 2h (bars 21:00 and 22:00)
            idx = np.where(hours == 20)[0]
            for i in idx:
                if i < 720 or i + 2 >= n or i - 7 < 0:
                    continue
                # US session move: close at 21:00 vs close at 13:00 (bar starting 13 closes 14) -> i-7
                us = c[i] / c[i - 7] - 1
                d24 = c[i] / c[i - 24] - 1
                past = c[i - 720:i + 1]
                pr = past[24::24] / past[:-24:24] - 1
                sd24 = np.std(pr, ddof=1)
                fwd = c[i + 2] / c[i] - 1
                vv = v[i - 6:i + 1].mean() / max(v[i - 720:i + 1].mean(), 1e-12)
                rows.append(dict(coin=coin, window=w, wd=wds[i], year=ts.iloc[i].year,
                                 us=us, d24=d24, z24=d24 / sd24 if sd24 > 0 else np.nan,
                                 fwd=fwd, vv=vv, vreg=vol24[i] / vol720[i]))
    H = pd.concat(hr).dropna(subset=["r1"])
    E = H[H.hour.isin([21, 22])]
    out["21-22h hourly ret by year"] = E.groupby("year")["r1"].apply(tt).unstack()
    out["21-22h by coin"] = E.groupby("coin")["r1"].apply(tt).unstack()
    out["21-22h by weekday"] = E.groupby("wd")["r1"].apply(tt).unstack()
    H["vq"] = pd.qcut(H.vreg, 4, labels=False)
    out["21-22h by vol regime quartile"] = H[H.hour.isin([21, 22])].groupby("vq")["r1"].apply(tt).unstack()
    out["saturday by hour block"] = H[H.wd == 5].groupby(H.hour // 4)["r1"].apply(tt).unstack()
    D = pd.DataFrame(rows)
    D["fu"] = D.fwd - D.groupby("coin").fwd.transform("mean")
    out["2h fwd (21-23h) all days, raw"] = tt(D.fwd).to_frame().T
    D["usq"] = D.groupby("coin").us.transform(lambda x: pd.qcut(x, 5, labels=False))
    out["2h fwd by US-session(14-21h) return quintile"] = D.groupby("usq")["fwd"].apply(tt).unstack()
    D["zq"] = pd.qcut(D.z24, 5, labels=False)
    out["2h fwd by 24h z quintile"] = D.groupby("zq")["fwd"].apply(tt).unstack()
    D["vvq"] = D.groupby("coin").vv.transform(lambda x: pd.qcut(x, 5, labels=False))
    out["2h fwd by session volume quintile"] = D.groupby("vvq")["fwd"].apply(tt).unstack()
    out["spearman fwd vs us, z24, vv"] = pd.Series({
        "us": stats.spearmanr(D.us, D.fwd, nan_policy="omit")[0],
        "z24": stats.spearmanr(D.z24, D.fwd, nan_policy="omit")[0],
        "vv": stats.spearmanr(D.vv, D.fwd, nan_policy="omit")[0],
        "n": len(D)})
    # book largest days
    Ds = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()])
    Ds["day"] = pd.to_datetime(Ds["day"])
    Ds["wd"] = Ds.day.dt.weekday
    act = Ds[Ds.book_return.abs() > 0]
    out["book active days by weekday"] = act.groupby("wd")["book_return"].apply(tt).unstack()
    return out
