def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily returns pooled, mark deepest fall periods (falls deeper than 15% from peak)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"]).dropna(subset=["br"])
    v = (1 + B["br"]).cumprod().values
    ddv = v / np.maximum.accumulate(v) - 1
    B["dd"] = ddv
    B["infall"] = ddv < -0.25
    fallkeys = set(zip(B.loc[B.infall, "wn"], B.loc[B.infall, "day"].astype(str)))
    # cases
    cs = []
    allh0 = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = pd.Series(b["close"].values)
            r1 = cl.pct_change()
            s24 = r1.rolling(24).std()
            ratio = s24 / s24.rolling(720, min_periods=240).mean()
            fwd = cl.shift(-24) / cl - 1
            r7 = cl / cl.shift(168) - 1
            hr = ts.dt.hour.values
            f = b["forecast"].values
            alloc = b["postRebalance_current_allocation"].values
            idx = np.where(hr == 0)[0]
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "f": f[idx], "r1": r1.values[idx], "fwd": fwd.values[idx],
                               "ratio": ratio.values[idx], "r7": r7.values[idx],
                               "alloc": alloc[idx], "day": ts.dt.strftime("%Y-%m-%d").values[idx]})
            allh0.append(df)
    A = pd.concat(allh0).dropna(subset=["fwd"])
    A["infall"] = [ (wn, d) in fallkeys for wn, d in zip(A.wn, A.day)]
    C = A[A.f != 0].copy()
    C["g"] = np.sign(C.f) * C.fwd
    C["side"] = np.where(C.f > 0, "long", "short")
    def agg(gb, col="g"):
        r = gb[col].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r
    out["fall_share_days"] = pd.Series({"share_days_in_fall": B.infall.mean(), "mean_br_fall": B.loc[B.infall, "br"].mean(),
                                        "mean_cr_fall": B.loc[B.infall, "cr"].mean(), "mean_br_out": B.loc[~B.infall, "br"].mean()})
    out["cases_infall_side"] = agg(C.groupby(["infall", "side"]))
    out["cases_infall_ratio_hi"] = agg(C.assign(hi=C.ratio > C.ratio.median()).groupby(["infall", "hi"]))
    # |alloc| vs |f|: position size used
    C["fq"] = pd.qcut(C.f.abs(), 5, labels=False)
    out["alloc_by_fq"] = C.groupby("fq").agg(abs_alloc=("alloc", lambda x: np.abs(x).mean()), mean_g=("g", "mean"))
    # side x 7d trend
    C["with7"] = np.sign(C.r7) * np.sign(C.f)
    out["side_x_trend7"] = agg(C.groupby(["side", "with7"]))
    # condition alone: 7d-trend direction over next 24h on hour-0 bars (all), and on bars with small |r1|
    A["trend_g"] = np.sign(A.r7) * A.fwd
    A["z"] = (A.r1.abs() / A.groupby("coin").r1.transform(lambda x: x.abs().median()))
    A["zq"] = pd.qcut(A.z, 3, labels=False)
    out["trend7_alone_by_zq"] = agg(A.groupby("zq"), "trend_g")
    # ratio alone: does high ratio predict anything without direction? mean |fwd| by ratio hi
    A["hi"] = A.ratio > A.ratio.median()
    out["fade_by_zq_hi"] = agg(A.assign(g=-np.sign(A.r1) * A.fwd).groupby(["zq", "hi"]))
    # book daily by window mean |alloc|
    return out
