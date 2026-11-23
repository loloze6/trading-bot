def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    H = pd.Timedelta(hours=1)
    rows = []      # day-level cases
    hourly = []
    for coin in bars:
        # coin drift on 48h grid
        g48 = []
        for w, df in bars[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48 += list(c[idx + 48] / c[idx] - 1)
        drift = np.mean(g48)
        usual = np.std(g48, ddof=1)
        # vol median of coin for calm split
        vols = []
        prepared = {}
        for w, df in bars[coin].items():
            d = df[["timestamp", "close", "regime"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d["t_end"] = d["timestamp"] + H
            r = d["close"].pct_change()
            d["vol"] = r.rolling(720, min_periods=500).std()
            d["hr"] = d["timestamp"].dt.hour
            d["wd"] = d["timestamp"].dt.weekday
            hourly.append(pd.DataFrame({"coin": coin, "hr": d["hr"], "wd": d["wd"], "r": r}))
            vols.append(d["vol"])
            prepared[w] = d.set_index("t_end")
        vmed = pd.concat(vols).median()
        for w, d in prepared.items():
            px = d["close"]; vol = d["vol"]
            mids = px.index[px.index.hour == 0]
            for T in mids:
                Tp = T - pd.Timedelta(days=1)
                if Tp not in px.index: continue
                rd = px[T] / px[Tp] - 1
                v = vol.get(T, np.nan)
                if not np.isfinite(v) or v <= 0: continue
                z = rd / (v * np.sqrt(24))
                rec = {"coin": coin, "w": w, "wd": Tp.weekday(), "year": Tp.year, "rd": rd, "z": z,
                       "calm": v <= vmed, "drift": drift, "usual": usual}
                for k in (0, 1):
                    t0 = T + pd.Timedelta(days=k); t1 = t0 + pd.Timedelta(hours=48)
                    if t0 in px.index and t1 in px.index:
                        rec[f"f{k}"] = px[t1] / px[t0] - 1 - drift
                    else:
                        rec[f"f{k}"] = np.nan
                t1 = T + pd.Timedelta(hours=24)
                rec["f24"] = px[t1] / px[T] - 1 - drift / 2 if t1 in px.index else np.nan
                rows.append(rec)
    D = pd.DataFrame(rows)
    out = {}
    def summ(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 30: return pd.Series({"n": len(s)})
        dirr = np.sign(s["z"]) * s[col]
        sl = stats.linregress(s["z"], s[col])
        return pd.Series({"n": len(s), "dir_mean%": 100 * dirr.mean(),
                          "dir_t": dirr.mean() / (dirr.std(ddof=1) / np.sqrt(len(s))),
                          "slope_t": sl.slope / sl.stderr, "corr": sl.rvalue})
    # weekday day-return -> next 48h starting skip k days
    for col in ["f0", "f1", "f24"]:
        out[f"day_move_to_{col}_by_weekday"] = D.groupby("wd").apply(lambda s: summ(s, col))
        out[f"day_move_to_{col}_by_weekday_calm"] = D[D.calm].groupby("wd").apply(lambda s: summ(s, col))
        out[f"day_move_to_{col}_by_weekday_hot"] = D[~D.calm].groupby("wd").apply(lambda s: summ(s, col))
    # large vs small Saturday moves
    sat = D[D.wd == 5].copy()
    sat["q"] = pd.qcut(sat["z"].abs(), 4, labels=False)
    out["sat_absz_quartile_f1"] = sat.groupby("q").apply(lambda s: summ(s, "f1"))
    out["sat_by_year_f1"] = sat.groupby("year").apply(lambda s: summ(s, "f1"))
    out["sat_by_coin_f1"] = sat.groupby("coin").apply(lambda s: summ(s, "f1"))
    allw = D.copy(); allw["q"] = pd.qcut(allw["z"].abs(), 5, labels=False)
    out["anyday_absz_quintile_f0"] = allw.groupby("q").apply(lambda s: summ(s, "f0"))
    # hourly / weekday returns
    Hh = pd.concat(hourly).dropna()
    hg = Hh.groupby("hr")["r"].agg(["mean", "std", "count"])
    hg["t"] = hg["mean"] / (hg["std"] / np.sqrt(hg["count"])); hg["mean_bp"] = hg["mean"] * 1e4
    out["hour_of_day"] = hg[["mean_bp", "t", "count"]]
    wg = Hh.groupby("wd")["r"].agg(["mean", "std", "count"])
    wg["t"] = wg["mean"] / (wg["std"] / np.sqrt(wg["count"])); wg["mean_bp"] = wg["mean"] * 1e4
    out["weekday_hourly"] = wg[["mean_bp", "t", "count"]]
    # book days
    dd = []
    for coin in days:
        for w, df in days[coin].items():
            x = df.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    DD = pd.concat(dd)
    DD["day"] = pd.to_datetime(DD["day"])
    book = DD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    book["wd"] = book["day"].dt.weekday; book["year"] = book["day"].dt.year
    out["book_by_weekday_bp"] = book.groupby("wd")[["book_return", "coin_return"]].mean() * 1e4
    out["book_by_year"] = book.groupby("year").agg(mean_bp=("book_return", lambda x: 1e4 * x.mean()),
                                                   sd_bp=("book_return", lambda x: 1e4 * x.std()), n=("book_return", "size"))
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "std", "count"])
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("year")["net_profit_loss_percent"].agg(["mean", "count"])
    return out
