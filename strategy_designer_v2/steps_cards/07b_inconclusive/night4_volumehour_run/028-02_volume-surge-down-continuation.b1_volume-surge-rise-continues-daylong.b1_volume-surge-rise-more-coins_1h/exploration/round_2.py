def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [2, 24]
    rows = []
    drift = {}
    fpos = []
    for coin, wins in bars.items():
        for h in H:
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.nanmean(np.concatenate(allr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r = df["close"].pct_change()
            sd = r.rolling(720, min_periods=120).std()
            vr = (df["volume"] / df["volume"].rolling(720, min_periods=120).mean()).values
            z = (r / sd).values
            f = df["forecast"].values
            fpos.append(pd.Series({"coin": coin, "n": len(f), "pos": np.sum(f > 0), "ge2": np.sum(f >= 2)}))
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for h in H:
                fwd = np.full(n, np.nan)
                fwd[: n - h] = c[h:] / c[: n - h] - 1
                cell = np.arange(n) // h
                ev = (np.abs(z) >= 2.5) & np.isfinite(vr) & np.isfinite(fwd)
                e = pd.DataFrame({"cell": cell[ev], "side": np.sign(z[ev]), "z": np.abs(z[ev]),
                                  "vr": vr[ev], "fwd": fwd[ev], "yr": yr[ev], "f": f[ev]})
                e = e.groupby(["cell", "side"]).first().reset_index()
                e["coin"] = coin; e["h"] = h; e["w"] = w
                rows.append(e)
    E = pd.concat(rows)
    E["dr"] = [drift[(a, b)] for a, b in zip(E.coin, E.h)]
    E["u"] = (E.fwd - E.dr) * E.side
    def agg(g):
        return pd.Series({"n": len(g), "mean_u_%": 100 * g.u.mean(),
                          "t": g.u.mean() / (g.u.std() / np.sqrt(len(g)))})
    up24 = E[(E.h == 24) & (E.side > 0) & (E.vr > 3)]
    dn2 = E[(E.h == 2) & (E.side < 0) & (E.vr > 3)]
    dn24 = E[(E.h == 24) & (E.side < 0) & (E.vr > 3)]
    def corr_t(g, x):
        rr = np.corrcoef(np.log(g[x]), g.u)[0, 1]; m = len(g)
        return pd.Series({"n": m, "corr": rr, "t": rr * np.sqrt((m - 2) / (1 - rr ** 2))})
    up24all = E[(E.h == 24) & (E.side > 0)]
    dn2all = E[(E.h == 2) & (E.side < 0)]
    FP = pd.DataFrame(fpos).groupby("coin")[["n", "pos", "ge2"]].sum()
    FP["share_pos"] = FP.pos / FP.n; FP["share_ge2"] = FP.ge2 / FP.n
    return {
        "forecast_share": FP,
        "up24_vr3_coin": up24.groupby("coin").apply(agg).reset_index(),
        "up24_vr3_year": up24.groupby("yr").apply(agg).reset_index(),
        "dn2_vr3_coin": dn2.groupby("coin").apply(agg).reset_index(),
        "dn2_vr3_year": dn2.groupby("yr").apply(agg).reset_index(),
        "dn24_vr3_coin": dn24.groupby("coin").apply(agg).reset_index(),
        "grade_up24_logvr": corr_t(up24all, "vr"),
        "grade_dn2_logvr": corr_t(dn2all, "vr"),
        "up24_by_forecast_zero": up24.assign(fz=(up24.f > 0)).groupby("fz").apply(agg).reset_index(),
    }
