def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            rs.append(cl[idx + 24] / cl[idx] - 1)
        drift[c] = np.concatenate(rs).mean()
    cases = []; ctrl = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            s_cl = pd.Series(cl)
            r1 = s_cl.pct_change()
            vol24 = r1.rolling(24).std()
            vol30 = r1.rolling(720).std()
            tr1 = s_cl / s_cl.shift(24) - 1
            ts = pd.to_datetime(b["timestamp"])
            hr = ts.dt.hour.values
            m = (b["regime"] == "mean_reversion") & (b["forecast"] != 0)
            day = ts.dt.floor("D")
            sel = b[m].groupby(day[m]).head(1).index
            for i in sel:
                if i + 24 >= n: continue
                f = b["forecast"].iat[i]; s = np.sign(f)
                fwd = cl[i + 24] / cl[i] - 1
                cases.append(dict(coin=c, w=int(w[1:]), day=day.iat[i], f=f, s=s, fwd=fwd,
                                  ex=s * (fwd - drift[c]), tr1=tr1.iat[i], r1=r1.iat[i],
                                  v24=vol24.iat[i], vr=vol24.iat[i] / vol30.iat[i] if vol30.iat[i] > 0 else np.nan))
            # control: hour-13 bars, position against the 24h move, no settlement signal
            idx = np.where(hr == 13)[0]
            for i in idx:
                if i + 24 >= n or np.isnan(tr1.iat[i]) or np.isnan(vol24.iat[i]): continue
                fwd = cl[i + 24] / cl[i] - 1
                s = -np.sign(tr1.iat[i])
                ctrl.append(dict(coin=c, z=abs(tr1.iat[i]) / (vol24.iat[i] * np.sqrt(24)), ex=s * (fwd - drift[c])))
    d = pd.DataFrame(cases); k = pd.DataFrame(ctrl)
    d["z24"] = d.s * d.tr1 / (d.v24 * np.sqrt(24))
    def g(df, col):
        x = df.groupby(col, observed=True)["ex"].agg(["count", "mean", "std"])
        x["t"] = x["mean"] / (x["std"] / np.sqrt(x["count"])); return x
    # condition alone: fade the 24h move at 13:00, graded
    k["zq"] = pd.qcut(k.z, 5)
    out["ctrl_fade24h_at13h_by_z"] = g(k, "zq")
    # condition alone at 01:00: position against 24h move (ignoring hour sign)
    d["s24"] = -np.sign(d.tr1)
    d["agree"] = np.where(d.s24 == d.s, "signal_also_against_24h", "signal_with_24h")
    d["fb"] = np.where(d.f.abs() >= 10, "big", "small")
    out["by_agree_x_size"] = g(d, ["agree", "fb"])
    # 01:00 control: excess return of fading 24h move over the 24h move only (prior 23h excl. shock hour)
    d["tr23"] = (1 + d.tr1) / (1 + d.r1) - 1
    d["agree23"] = np.where(-np.sign(d.tr23) == d.s, "against_prior23h", "with_prior23h")
    out["by_agree23_x_size"] = g(d, ["agree23", "fb"])
    d["vrq"] = pd.qcut(d.vr, 3, labels=["lowvr", "midvr", "hivr"])
    out["by_vr_x_size"] = g(d, ["vrq", "fb"])
    # simulated daily books: per case return w*s*fwd - cost*|w|, mean over coins per day
    cost = 0.0019
    def book(wcol):
        x = d.copy(); x["w_"] = wcol
        x["r"] = x.w_ * x.s * x.fwd - cost * x.w_.abs()
        bk = x.groupby(["w", "day"])["r"].mean().reset_index().sort_values(["w", "day"])
        r = bk.r.values; v = np.cumprod(1 + r); dd = (v / np.maximum.accumulate(v) - 1).min()
        yr = v[-1] ** (365 / len(r)) - 1
        return pd.Series({"mean_bp": r.mean() * 1e4, "sharpe": r.mean() / r.std() * np.sqrt(365),
                          "yearly": yr, "maxdd": dd, "calmar": yr / -dd})
    base = 0.5 / (d.v24 * np.sqrt(24)).clip(lower=0.005) * 0.02  # vol scaled
    res = {}
    res["all_flat"] = book(pd.Series(1.0, index=d.index))
    res["all_volscaled"] = book(base.clip(upper=2))
    res["size_by_absf"] = book(d.f.abs() / 10)
    res["big_only"] = book((d.f.abs() >= 10).astype(float))
    res["agree24_only"] = book((d.agree == "signal_also_against_24h").astype(float))
    res["agree24_x_absf"] = book((d.agree == "signal_also_against_24h") * d.f.abs() / 10)
    res["agree24_big_volscaled"] = book(((d.agree == "signal_also_against_24h") & (d.fb == "big")) * base.clip(upper=2))
    res["lowhi_vr_out"] = book((d.vrq != "hivr").astype(float))
    out["sim_books"] = pd.DataFrame(res).T
    # deepest-fall window w12: case breakdown
    w12 = d[d.w == 12]
    out["w12_by_agree"] = g(w12, "agree")
    out["w12_by_fb"] = g(w12, "fb")
    return out
