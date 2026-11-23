def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}; drift48 = {}
    for c, ws in data["bars"].items():
        rs = []; rs48 = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24); rs.append(cl[idx + 24] / cl[idx] - 1)
            idx = np.arange(0, len(cl) - 48, 48); rs48.append(cl[idx + 48] / cl[idx] - 1)
        drift[c] = np.concatenate(rs).mean(); drift48[c] = np.concatenate(rs48).mean()
    cases = []; ctrl = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl); s_cl = pd.Series(cl)
            r1 = s_cl.pct_change(); vol24 = r1.rolling(24).std(); vol30 = r1.rolling(720).std()
            ts = pd.to_datetime(b["timestamp"]); hr = ts.dt.hour.values; day = ts.dt.floor("D")
            m = (b["regime"] == "mean_reversion") & (b["forecast"] != 0)
            sel = b[m].groupby(day[m]).head(1).index
            for i in sel:
                if i + 48 >= n: continue
                f = b["forecast"].iat[i]; s = np.sign(f)
                cases.append(dict(coin=c, w=int(w[1:]), day=day.iat[i], f=f, s=s,
                    fwd=cl[i+24]/cl[i]-1, ex=s*(cl[i+24]/cl[i]-1-drift[c]),
                    ex48=s*(cl[i+48]/cl[i]-1-drift48[c]), v24=vol24.iat[i],
                    vr=vol24.iat[i]/vol30.iat[i] if vol30.iat[i] > 0 else np.nan,
                    alloc=b["postRebalance_current_allocation"].iat[i]))
            for i in np.where(hr == 13)[0]:
                if i + 24 >= n or np.isnan(vol24.iat[i]) or not vol30.iat[i] > 0: continue
                z = r1.iat[i] / vol24.iat[i]
                ctrl.append(dict(z=abs(z), vr=vol24.iat[i]/vol30.iat[i],
                                 ex=-np.sign(z)*(cl[i+24]/cl[i]-1-drift[c])))
    d = pd.DataFrame(cases).dropna(subset=["v24", "vr"]); k = pd.DataFrame(ctrl)
    def g(df, col):
        x = df.groupby(col, observed=True)["ex"].agg(["count", "mean", "std"])
        x["t"] = x["mean"] / (x["std"] / np.sqrt(x["count"])); return x
    k["zb"] = np.where(k.z >= 1, "big", "small"); k["vrq"] = pd.qcut(k.vr, 3, labels=["lowvr","midvr","hivr"])
    out["ctrl_fade1h_at13h_vr_x_size"] = g(k, ["vrq", "zb"])
    d["fb"] = np.where(d.f.abs() >= 10, "big", "small")
    x = d.groupby("fb")[["ex", "ex48"]].agg(["mean", "count"]); out["h24_vs_h48"] = x
    d["absalloc"] = d.alloc.abs()
    out["alloc_by_fb"] = d.groupby("fb")["absalloc"].mean()
    cost = 0.0019
    tgt = 0.382099 / np.sqrt(8760)
    vs = (tgt / d.v24.clip(lower=1e-4)).clip(upper=2)
    def book(wcol, hcol="fwd"):
        x = d.copy(); x["w_"] = wcol.values
        x["r"] = x.w_ * x.s * x[hcol] - cost * x.w_.abs()
        bk = x.groupby(["w", "day"])["r"].mean().reset_index().sort_values(["w", "day"])
        r = bk.r.values; v = np.cumprod(1 + r); dd = (v / np.maximum.accumulate(v) - 1).min()
        yr = v[-1] ** (365 / len(r)) - 1
        return pd.Series({"mean_bp": r.mean()*1e4, "sharpe": r.mean()/r.std()*np.sqrt(365),
                          "yearly": yr, "maxdd": dd, "calmar": yr / -dd})
    big = (d.fb == "big").astype(float)
    res = {}
    res["volscaled_all"] = book(vs)
    res["volscaled_x_absf"] = book(vs * d.f.abs() / 10)
    res["volscaled_big_only"] = book(vs * big)
    res["volscaled_big_x_absf"] = book(vs * big * d.f.abs() / 10)
    res["volscaled_x_excess_over10"] = book(vs * ((d.f.abs() - 10).clip(lower=0) / 10))
    out["sim_books"] = pd.DataFrame(res).T
    # actual book: deepest fall location
    dd_ = []
    for c, ws in data["days"].items():
        for w, xx in ws.items():
            xx = xx.copy(); xx["w"] = int(w[1:]); dd_.append(xx)
    dd_ = pd.concat(dd_)
    bk = dd_.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index().dropna().sort_values(["w","day"]).reset_index(drop=True)
    v = (1 + bk.book_return).cumprod(); peak = v.cummax(); ddv = v / peak - 1
    trough = ddv.idxmin(); pk = v[:trough+1].idxmax()
    seg = bk.loc[pk:trough]
    out["deepest_fall"] = pd.Series({"depth": ddv.min(), "days": len(seg), "w_start": seg.w.iat[0], "w_end": seg.w.iat[-1],
        "coin_mean_bp": seg.coin_return.mean()*1e4, "coin_absmean_bp": seg.coin_return.abs().mean()*1e4,
        "book_mean_bp": seg.book_return.mean()*1e4})
    seg_cases = d[(d.w >= seg.w.iat[0]) & (d.w <= seg.w.iat[-1])]
    out["fall_window_cases"] = g(seg_cases, "fb")
    return out
