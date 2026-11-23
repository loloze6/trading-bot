def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = pd.Timedelta(hours=1)
    rows = []; ev = []
    for coin in bars:
        g48 = []; g24 = []
        for w, df in bars[coin].items():
            c = df["close"].values
            i = np.arange(0, len(c) - 48, 48); g48 += list(c[i + 48] / c[i] - 1)
            i = np.arange(0, len(c) - 24, 24); g24 += list(c[i + 24] / c[i] - 1)
        d48 = np.mean(g48); d24 = np.mean(g24)
        vols = []; prep = {}
        for w, df in bars[coin].items():
            d = df[["timestamp", "close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            r = d["close"].pct_change()
            d["vol"] = r.rolling(720, min_periods=500).std()
            d["vol7"] = r.rolling(168, min_periods=120).std()
            d["t_end"] = d["timestamp"] + H
            vols.append(d["vol"]); prep[w] = d.set_index("t_end")
            # evening 21-22h return vs prior 24h return
            dd = d.set_index("t_end")["close"]
            for T in dd.index[dd.index.hour == 21]:
                a = T - pd.Timedelta(hours=24); b = T + pd.Timedelta(hours=2)
                if a in dd.index and b in dd.index:
                    ev.append({"coin": coin, "wd": T.weekday(), "prior": dd[T] / dd[a] - 1,
                               "eve": dd[b] / dd[T] - 1})
        vq = pd.concat(vols).dropna().quantile([1/3, 2/3]).values
        for w, d in prep.items():
            px = d["close"]; vol = d["vol"]; v7 = d["vol7"]
            for T in px.index[px.index.hour == 0]:
                ts = T - pd.Timedelta(days=1); t1 = T + pd.Timedelta(hours=24); t2 = T + pd.Timedelta(hours=48)
                if not all(x in px.index for x in (ts, t1, t2)): continue
                v = vol.get(T, np.nan)
                if not np.isfinite(v) or v <= 0: continue
                m = px[T] / px[ts] - 1
                rows.append({"coin": coin, "wd": ts.weekday(), "z": m / (v * np.sqrt(24)), "m": m,
                             "vt": int(np.searchsorted(vq, v)), "vlog": np.log(v),
                             "f24": px[t1] / px[T] - 1 - d24, "f48": px[t2] / px[T] - 1 - d48})
    D = pd.DataFrame(rows)
    out = {}
    def summ(s, col):
        if len(s) < 30: return pd.Series({"n": len(s)})
        dr = -np.sign(s["m"]) * s[col]
        sl = stats.linregress(s["m"], s[col])
        return pd.Series({"n": len(s), "rev%": 100 * dr.mean(),
                          "rev_t": dr.mean() / (dr.std(ddof=1) / np.sqrt(len(s))), "slope_raw_t": sl.slope / sl.stderr})
    S = D[D.wd == 6].copy()
    hv = S[S.vt >= 1].copy()
    hv["q"] = pd.qcut(hv["m"].abs(), 4, labels=False)
    out["sun_highvol_by_absmove_q_f48"] = hv.groupby("q").apply(lambda s: summ(s, "f48"))
    S["q"] = pd.qcut(S["m"].abs(), 4, labels=False)
    out["sun_by_rawabsmove_q_f48"] = S.groupby("q").apply(lambda s: summ(s, "f48"))
    out["sun_by_vt_raw_slope"] = S.groupby("vt").apply(lambda s: summ(s, "f48"))
    # all days, next-24h reversal of raw day move, by vol tercile
    out["allday_f24_by_vt"] = D.groupby("vt").apply(lambda s: summ(s, "f24"))
    out["weekday_only_f24_by_vt"] = D[D.wd <= 4].groupby("vt").apply(lambda s: summ(s, "f24"))
    out["sun_f48_by_vt_again"] = S.groupby("vt").apply(lambda s: summ(s, "f48"))
    E = pd.DataFrame(ev)
    E["q"] = pd.qcut(E["prior"], 5, labels=False)
    g = E.groupby("q")["eve"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["mean_bp"] = 1e4 * g["mean"]
    out["eve2h_by_prior24_quintile"] = g[["mean_bp", "t", "count"]]
    g = E.groupby("wd")["eve"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["mean_bp"] = 1e4 * g["mean"]
    out["eve2h_by_weekday"] = g[["mean_bp", "t", "count"]]
    return out
