def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            hi = df["high"].rolling(20, min_periods=20).max().values
            lo = df["low"].rolling(20, min_periods=20).min().values
            rp = np.where(hi > lo, 40 * (c - lo) / (hi - lo) - 20, np.nan)
            f = df["forecast"].values
            raw = df.get("debug_info.components.range_pos.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            r60 = pd.Series(c).pct_change(60).values
            n = len(c)
            for h in [3, 5]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], rp=rp[i], reg=reg[i],
                                     ret=c[i + h] / c[i] - 1, r60=r60[i], day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mu"]

    def tstat(g, val, wt=None):
        g = g.dropna(subset=[val])
        if wt is None:
            g = g.assign(_w=1.0)
            wt = "_w"
        dd = g.groupby("day").apply(lambda x: pd.Series({"num": (x[val] * x[wt]).sum(), "den": x[wt].sum()}))
        m = dd.num.sum() / dd.den.sum()
        res = dd.num - m * dd.den
        k = len(dd)
        se = np.sqrt((res ** 2).sum()) / dd.den.sum() * np.sqrt(k / max(k - 1, 1))
        return pd.Series({"mean": m, "t": m / se if se > 0 else np.nan, "n": len(g), "days": k})

    out = {}
    d5 = d[(d.h == 5) & d.rp.notna()].copy()
    d5["calm"] = np.where(d5.reg == "chop", "agitated", "calm")
    d5["sx"] = np.sign(d5.rp) * d5.ex
    d5["rpbin"] = pd.cut(d5.rp, [-20.01, -16, -10, -4, 4, 10, 16, 20.01])
    out["h5_signed_excess_by_rawpos_calm"] = d5[d5.calm == "calm"].groupby("rpbin").apply(lambda g: tstat(g, "ex"))
    out["h5_signed_excess_by_rawpos_agitated"] = d5[d5.calm == "agitated"].groupby("rpbin").apply(lambda g: tstat(g, "ex"))
    d5["absrp"] = d5.rp.abs()
    out["h5_sx_weighted_absrp_by_profile"] = d5.groupby("calm").apply(lambda g: tstat(g, "sx", "absrp"))
    d5["absrp2"] = d5.rp ** 2
    out["h5_sx_weighted_rp2_by_profile"] = d5.groupby("calm").apply(lambda g: tstat(g, "sx", "absrp2"))
    a = d5[(d5.f != 0) & d5.f.notna()].copy()
    a["sxf"] = np.sign(a.f) * a.ex
    a["f2"] = a.f ** 2
    a["af"] = a.f.abs()
    out["calm_active_weight_f_vs_f2"] = pd.DataFrame({"w_absf": tstat(a, "sxf", "af"),
                                                     "w_f2": tstat(a, "sxf", "f2"),
                                                     "w_absraw": tstat(a.assign(ar=a.raw.abs()), "sxf", "ar")})
    a["agree"] = np.sign(a.f) == np.sign(a.rp)
    out["forecast_sign_agrees_raw_share"] = float(a.agree.mean())
    out["calm_by_agree"] = a.groupby("agree").apply(lambda g: tstat(g, "sxf", "af"))
    return out
