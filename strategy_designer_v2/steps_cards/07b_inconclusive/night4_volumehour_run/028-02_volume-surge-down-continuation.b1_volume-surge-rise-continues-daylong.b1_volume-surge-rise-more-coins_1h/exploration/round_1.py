def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [2, 6, 12, 24]
    rows = []      # recomputed events
    frows = []     # recorded forecast cases
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr)
            drift[(coin, h)] = (np.nanmean(allr), np.nanstd(allr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r = df["close"].pct_change()
            sd = r.rolling(720, min_periods=120).std()
            vr = df["volume"] / df["volume"].rolling(720, min_periods=120).mean()
            z = r / sd
            s = z * vr
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            f = df["forecast"].values
            for h in H:
                fwd = np.full(n, np.nan)
                fwd[: n - h] = c[h:] / c[: n - h] - 1
                cell = np.arange(n) // h
                # recomputed events: |z|>=2.5
                ev = (np.abs(z.values) >= 2.5) & np.isfinite(vr.values) & np.isfinite(fwd)
                e = pd.DataFrame({"cell": cell[ev], "side": np.sign(z.values[ev]),
                                  "z": np.abs(z.values[ev]), "vr": vr.values[ev],
                                  "s": np.abs(s.values[ev]), "fwd": fwd[ev], "yr": yr[ev]})
                e = e.groupby(["cell", "side"]).first().reset_index()
                e["coin"] = coin; e["h"] = h; e["w"] = w
                rows.append(e)
                fe = (f > 0) & np.isfinite(fwd)
                fd = pd.DataFrame({"cell": cell[fe], "f": f[fe], "fwd": fwd[fe], "yr": yr[fe]})
                fd = fd.groupby("cell").first().reset_index()
                fd["coin"] = coin; fd["h"] = h; fd["w"] = w
                frows.append(fd)
    E = pd.concat(rows); F = pd.concat(frows)
    E["dr"] = [drift[(a, b)][0] for a, b in zip(E.coin, E.h)]
    E["u"] = (E.fwd - E.dr) * E.side
    F["dr"] = [drift[(a, b)][0] for a, b in zip(F.coin, F.h)]
    F["u"] = F.fwd - F.dr
    def agg(g):
        return pd.Series({"n": len(g), "mean_u_%": 100 * g.u.mean(),
                          "t": g.u.mean() / (g.u.std() / np.sqrt(len(g)))})
    E["vol"] = pd.cut(E.vr, [0, 1.5, 3, 6, np.inf], labels=["<1.5", "1.5-3", "3-6", ">6"])
    E["zb"] = pd.cut(E.z, [2.5, 4, 6, np.inf], labels=["2.5-4", "4-6", ">6"])
    F["fq"] = F.groupby(["h"])["f"].transform(lambda x: pd.qcut(x.rank(method="first"), 4, labels=False))
    out = {
        "events_h_side_vol": E.groupby(["h", "side", "vol"]).apply(agg).reset_index(),
        "events_h_side_zb_highvol(vr>3)": E[E.vr > 3].groupby(["h", "side", "zb"]).apply(agg).reset_index(),
        "fcast_cases_h": F.groupby("h").apply(agg).reset_index(),
        "fcast_h_quartile": F.groupby(["h", "fq"]).apply(agg).reset_index(),
        "fcast24_coin": F[F.h == 24].groupby("coin").apply(agg).reset_index(),
        "fcast24_year": F[F.h == 24].groupby("yr").apply(agg).reset_index(),
        "fcast6_coin": F[F.h == 6].groupby("coin").apply(agg).reset_index(),
    }
    return out
