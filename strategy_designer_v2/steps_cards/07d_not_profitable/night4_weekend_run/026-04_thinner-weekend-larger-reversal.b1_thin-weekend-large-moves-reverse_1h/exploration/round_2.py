def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = (24, 48, 96)
    # coin normal drift and usual move per horizon, non-overlapping grid over all windows
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rr = []
            for w, b in wins.items():
                c = b["close"].values; g = np.arange(0, len(c) - h, h)
                rr.append(c[g + h] / c[g] - 1)
            rr = np.concatenate(rr); drift[(coin, h)] = rr.mean(); usual[(coin, h)] = rr.std()
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values; n = len(b)
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            idx = np.where((hr == 23) & np.isin(wd, [6, 2]))[0]
            for i in idx:
                if i < 168: continue
                past = c[i] / c[i - 48] - 1
                vr = np.log(v[i-47:i+1].mean() / max(v[i-167:i-47].mean(), 1e-12))
                r = dict(coin=coin, w=w, wd=wd[i], year=ts.iloc[i].year, past=past, vr=vr,
                         pz=past / usual[(coin, 48)])
                for h in H:
                    if i + h < n:
                        f = c[i + h] / c[i] - 1
                        r[f"tot{h}"] = -np.sign(past) * f
                        r[f"unu{h}"] = -np.sign(past) * (f - drift[(coin, h)])
                rows.append(r)
    d = pd.DataFrame(rows)
    d["apz"] = d["pz"].abs()
    out = {}
    def summ(sub):
        o = {"n": len(sub)}
        for h in H:
            x = sub[f"unu{h}"].dropna(); y = sub[f"tot{h}"].dropna()
            o[f"unu{h}%"] = round(100 * x.mean(), 3); o[f"t{h}"] = round(x.mean() / (x.std() / np.sqrt(len(x))), 2)
            o[f"tot{h}%"] = round(100 * y.mean(), 3)
        return pd.Series(o)
    for name, sub in [("sun_thin", d[(d.wd == 6) & (d.vr < 0)]), ("wed", d[d.wd == 2])]:
        sub = sub.copy(); sub["q"] = pd.qcut(sub["apz"], 5, labels=False)
        out[f"{name}_by_abs_move_quint"] = sub.groupby("q").apply(summ)
        out[f"{name}_by_side"] = sub.groupby(np.sign(sub["past"])).apply(summ)
        out[f"{name}_by_year"] = sub.groupby("year").apply(summ)
    # trades per case and by entry forecast size
    tr = pd.concat([t.assign(coin=c) for c, wins in data["trades"].items() for t in wins.values()])
    tr["af"] = tr["entry_forecast"].abs()
    tr["q"] = pd.qcut(tr["af"].rank(method="first"), 4, labels=False)
    out["trades_by_forecast_q"] = tr.groupby("q").agg(n=("af", "count"), af=("af", "mean"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda x: x.mean() / 60))
    out["trades_by_entry_regime"] = tr.groupby("entry_regime").agg(n=("af", "count"),
        gross=("profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    out["drift48_by_coin_%"] = pd.Series({c: round(100 * drift[(c, 48)], 3) for c in data["bars"]})
    return out
