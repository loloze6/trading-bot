import numpy as np, pandas as pd
from scipy import stats

def _ols_t(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 30: return (np.nan, np.nan, len(x))
    r = stats.linregress(x, y)
    return (r.slope, r.slope / r.stderr, len(x))

def explore(data):
    rows = []
    hour_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            ts = pd.to_datetime(b["timestamp"])
            hr = pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                               "r": np.r_[c[1:] / c[:-1] - 1, np.nan]})
            hour_rows.append(hr)
            n = len(c)
            for i in range(0, n, 72):
                if i < 72 or i + 72 >= n: continue
                past = c[i] / c[i - 72] - 1
                fwd = c[i + 72] / c[i] - 1
                vv = v[i - 71:i + 1]; rr = lr[i - 71:i + 1]
                med = np.median(vv)
                conc = np.log(vv.mean() / med) if med > 0 else np.nan
                sabs = np.nansum(np.abs(rr))
                eff = np.nansum(rr) / sabs if sabs > 0 else np.nan
                top = np.nanmax(np.abs(rr)) / sabs if sabs > 0 else np.nan
                top3 = np.sort(np.abs(rr[np.isfinite(rr)]))[-3:].sum() / sabs if sabs > 0 else np.nan
                vol = np.nanstd(rr)
                # volume share of top 3 hours
                vtop = np.sort(vv)[-3:].sum() / vv.sum() if vv.sum() > 0 else np.nan
                past24 = c[i] / c[i - 24] - 1
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, past=past, past24=past24, fwd=fwd,
                                 conc=conc, eff=eff, top=top, top3=top3, vol=vol, vtop=vtop))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    res = {}
    for name, sub in [("all", g), ("down", g[g.past < 0]), ("up", g[g.past > 0])]:
        for f in ["past", "past24", "conc", "eff", "top", "top3", "vol", "vtop"]:
            s, t, nn = _ols_t(sub[f].values, sub["ex"].values)
            res[(name, f)] = dict(slope=s, t=t, n=nn)
    out["slopes_ex72_on_feature"] = pd.DataFrame(res).T
    # quintiles of past return
    g["pq"] = g.groupby("coin")["past"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd_by_past_quintile"] = g.groupby("pq")["ex"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # within each past-quintile, grind (|eff| high) vs jumpy
    g["effq"] = g.groupby(["coin", "pq"])["top3"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["ex_by_pastq_x_top3tercile"] = g.pivot_table(index="pq", columns="effq", values="ex", aggfunc="mean")
    g["vq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex_by_volq"] = g.groupby("vq")["ex"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["signed_eff_x_past_down_by_coin"] = pd.DataFrame({c: dict(zip(["slope", "t", "n"], _ols_t(s["past"].values, s["ex"].values))) for c, s in g.groupby("coin")}).T
    H = pd.concat(hour_rows)
    out["hour_mean_r_t"] = H.groupby("hour")["r"].agg(lambda s: s.mean() / s.std() * np.sqrt(s.count())).round(2)
    out["wd_mean_r_t"] = H.groupby("wd")["r"].agg(["mean", lambda s: s.mean() / s.std() * np.sqrt(s.count())])
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = coin; dd["w"] = w
            D.append(dd)
    D = pd.concat(D)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    daily = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean()
    out["book_by_window_sharpe"] = daily.groupby("w")["book_return"].agg(lambda s: s.mean() / s.std() * np.sqrt(365)).round(2)
    out["book_coin_corr"] = float(daily.corr().iloc[0, 1])
    return out
