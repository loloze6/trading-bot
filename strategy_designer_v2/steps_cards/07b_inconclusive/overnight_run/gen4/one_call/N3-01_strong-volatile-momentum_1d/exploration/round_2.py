def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            h = df["high"].values.astype(float); l = df["low"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(c)
            fwd = np.full(n, np.nan); fwd[:-5] = c[5:] / c[:-5] - 1
            lr = np.r_[np.nan, np.diff(np.log(c))]
            s = pd.Series(c)
            r5 = s / s.shift(5) - 1
            r1 = s / s.shift(1) - 1
            vol20 = pd.Series(lr).rolling(20).std()
            vol100med = vol20.rolling(100, min_periods=40).median()
            hh20 = pd.Series(h).rolling(20).max()
            dd = s / hh20 - 1
            vr = pd.Series(v) / pd.Series(v).rolling(20).mean()
            ma50 = s.rolling(50).mean(); dist50 = s / ma50 - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 5):
                if np.isnan(fwd[i]): continue
                rows.append(dict(coin=coin, ts=ts.iloc[i], fc=df["forecast"].iloc[i], fwd=fwd[i],
                                 r5=r5.iloc[i], r1=r1.iloc[i], volrel=vol20.iloc[i] / vol100med.iloc[i] if vol100med.iloc[i] > 0 else np.nan,
                                 dd=dd.iloc[i], vr=vr.iloc[i], dist50=dist50.iloc[i],
                                 r20=df["debug_info.components.ret20.last_history_value"].iloc[i] if "debug_info.components.ret20.last_history_value" in df else np.nan))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["mkt"] = d.groupby("ts")["fwd"].transform("mean")
    btc = d[d.coin == "BTCUSD"].set_index("ts")["fwd"]
    d["btc"] = d.ts.map(btc)
    s = d[d.fc >= 10].copy()
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, hit=(x > 0).mean()))
    out = {}
    x = s.ex
    out["dist"] = pd.Series(dict(skew=x.skew(), p05=x.quantile(.05), p25=x.quantile(.25), p75=x.quantile(.75), p95=x.quantile(.95),
                                 trim5_mean=x[(x > x.quantile(.05)) & (x < x.quantile(.95))].mean(),
                                 wins_t=(lambda y: y.mean() / (y.std() / np.sqrt(len(y))))(x.clip(x.quantile(.05), x.quantile(.95)))))
    for col, q in [("r5", 3), ("r1", 3), ("volrel", 3), ("dd", 3), ("vr", 3), ("dist50", 3)]:
        ss = s.dropna(subset=[col]).copy()
        ss["b"] = pd.qcut(ss[col], q, labels=["low", "mid", "high"], duplicates="drop")
        out["by_" + col] = ss.groupby("b").apply(summ)
    s["btcup"] = np.where(s.coin == "BTCUSD", "self", np.where(s.btc > 0, "btc_up", "btc_dn"))
    out["by_btc_fwd_sign(not tradable)"] = s.groupby("btcup").apply(summ)
    # BTC own state: is BTC itself active at same ts
    bact = d[d.coin == "BTCUSD"].set_index("ts")["fc"]
    s["btc_act"] = s.ts.map(bact).fillna(0) >= 10
    out["alts_by_btc_active"] = s[s.coin != "BTCUSD"].groupby("btc_act").apply(summ)
    out["ex_corr_mkt"] = s[["ex", "mkt"]].corr().iloc[0, 1]
    out["share_var_mkt"] = 1 - (s.fwd - s.mkt).var() / s.fwd.var()
    return out
