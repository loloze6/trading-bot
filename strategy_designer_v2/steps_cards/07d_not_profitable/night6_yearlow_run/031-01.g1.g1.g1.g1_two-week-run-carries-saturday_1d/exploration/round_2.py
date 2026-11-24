def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            b["ret_next"] = b["close"].shift(-1) / b["close"] - 1
            b["r14"] = b["close"] / b["close"].shift(14) - 1
            b["vol20"] = r.rolling(20).std()
            b["z14"] = b["r14"] / (b["vol20"] * np.sqrt(14))
            b["r60"] = b["close"] / b["close"].shift(60) - 1
            b["fc"] = b["debug_info.components.run14.post_pipeline_value"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["wn"] = int(w[1:])
            b["dow"] = b["ts"].dt.dayofweek
            b["sat"] = (b["ts"] + pd.Timedelta(days=1)).dt.normalize()
            cs.append(b[["coin","wn","dow","ts","sat","ret_next","z14","r60","fc","alloc","vol20"]])
    A = pd.concat(cs)
    cost = 0.0019
    F = A[(A["dow"] == 4) & A["fc"].notna() & A["ret_next"].notna()].copy()
    F["gross"] = F["alloc"] * F["ret_next"]
    F["net"] = F["gross"] - F["alloc"].abs() * cost
    F["net_long"] = np.where(F["alloc"] > 0, F["net"], 0.0)
    F["net_short"] = np.where(F["alloc"] < 0, F["net"], 0.0)
    # Saturday book approximations (mean over the 6 coins; coins without a case count 0)
    S = F.groupby(["wn", "sat"]).agg(all_=("net", "sum"), lo=("net_long", "sum"), sh=("net_short", "sum")) / 6.0
    S = S.reset_index().sort_values(["wn", "sat"])
    nd = 2921  # days per coin approx
    years = nd / 365.0
    res = {}
    for col in ["all_", "lo", "sh"]:
        v = (1 + S[col]).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (1 / years) - 1
        res[col] = {"yearly": yr, "maxdd": dd, "calmar": yr / abs(dd), "mean": S[col].mean(), "std": S[col].std()}
    out["approx_books"] = pd.DataFrame(res).T.round(5)
    # deepest dd of the full approx book: what sides lost there
    v = (1 + S["all_"]).cumprod(); ddv = v / v.cummax() - 1
    tr = int(np.argmin(ddv.values)); pk = int(np.argmax(v.values[:tr + 1]))
    seg = S.iloc[pk:tr + 1]
    out["dd_seg_long_short_sum"] = seg[["all_", "lo", "sh"]].sum().round(4)
    out["dd_seg_n_sats"] = len(seg)
    # long-only grading: sextiles of fc among longs
    L = F[F["fc"] > 0].copy()
    L["q"] = pd.qcut(L["fc"], 3, labels=False)
    out["long_terciles"] = L.groupby("q")["ret_next"].agg(["mean", "count"]).round(5)
    Sh = F[F["fc"] < 0].copy()
    Sh["q"] = pd.qcut(Sh["fc"], 3, labels=False)
    out["short_terciles_raw_ret"] = Sh.groupby("q")["ret_next"].agg(["mean", "count"]).round(5)
    # condition alone checks: Saturday drift unconditional, and other weekdays' next-day return for z14>0
    allD = A[A["ret_next"].notna() & A["z14"].notna()].copy()
    allD["pos"] = allD["z14"] > 0
    g = allD.groupby(["dow", "pos"])["ret_next"].agg(["mean", "count"])
    g["t"] = allD.groupby(["dow", "pos"])["ret_next"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["nextday_by_dow_z14pos"] = g.round(5)
    # r60 trend condition with longs: r60>0 alone on Fridays (no signal) vs both
    Fr = allD[allD["dow"] == 4].copy()
    Fr["r60p"] = Fr["r60"] > 0
    out["fri_r60_x_pos"] = Fr.groupby(["r60p", "pos"])["ret_next"].agg(["mean", "count"]).round(5)
    # long side by year
    F["year"] = F["ts"].dt.year
    out["long_by_year"] = F[F["fc"] > 0].groupby("year")["ret_next"].agg(["mean", "count"]).round(5)
    return out
