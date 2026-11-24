def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily series
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("coin", "count")).reset_index().dropna()
    B = B.sort_values(["wn", "day"]).reset_index(drop=True)
    B["val"] = (1 + B["book"]).cumprod()
    B["peak"] = B["val"].cummax()
    B["dd"] = B["val"] / B["peak"] - 1
    B["hval"] = (1 + B["hold"]).cumprod()
    B["hdd"] = B["hval"] / B["hval"].cummax() - 1
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["max_dd_book"] = float(B["dd"].min())
    out["max_dd_hold"] = float(B["hdd"].min())
    # per window stats
    pw = B.groupby("wn").agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"), book_min_dd=("dd", "min"), year=("year", "first"))
    out["per_window"] = pw
    # deepest fall episode: trough and its peak
    i_tr = B["dd"].idxmin()
    pk = B.loc[:i_tr, "val"].idxmax()
    ep = B.loc[pk:i_tr]
    out["dd_episode"] = pd.Series({"windows": str(sorted(ep["wn"].unique())), "days": len(ep), "book_chain": float(ep["val"].iloc[-1] / ep["val"].iloc[0] - 1),
                                   "hold_chain": float((1 + ep["hold"]).prod() - 1), "year": int(ep["year"].iloc[0])})
    # bar-level: features
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            f = pd.DataFrame({"coin": c, "wn": int(w[1:]), "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "r0": r, "next": cl.shift(-1) / cl - 1,
                              "ret20": cl / cl.shift(20) - 1, "ret60": cl / cl.shift(60) - 1,
                              "ma50": cl / cl.rolling(50, min_periods=30).mean() - 1,
                              "vol20": r.rolling(20, min_periods=15).std(), "vol60": r.rolling(60, min_periods=40).std()})
            f["gain"] = f["alloc"] * f["next"]
            f["volratio"] = f["vol20"] / f["vol60"]
            f["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            recs.append(f)
    F = pd.concat(recs, ignore_index=True)
    drift = F.groupby("coin")["next"].mean()
    F["ex"] = F["next"] - F["coin"].map(drift)
    F = F.dropna(subset=["next"])
    F["sig"] = F["fc"] > 0
    out["alloc_share_on_sig_vs_not"] = pd.Series({"held_when_sig": float((F.loc[F.sig, "alloc"] > 0).mean()), "held_when_nosig": float((F.loc[~F.sig, "alloc"] > 0).mean()),
                                                   "gain_sig": float(F.loc[F.sig, "gain"].mean()), "gain_nosig": float(F.loc[~F.sig, "gain"].mean())})
    # gain on bars in deepest episode window
    epw = ep["wn"].unique()
    E = F[F["wn"].isin(epw)]
    out["episode_bar_state"] = pd.Series({"mean_ret60": float(E["ret60"].mean()), "share_ma50_neg": float((E["ma50"] < 0).mean()),
                                          "mean_alloc": float(E["alloc"].mean()), "gain_sig": float(E.loc[E.sig, "gain"].mean()), "gain_nosig": float(E.loc[~E.sig, "gain"].mean())})
    def grp(df, key, q):
        g = df.dropna(subset=[key]).copy()
        g["bin"] = pd.qcut(g[key], q, labels=False, duplicates="drop")
        return g.groupby("bin").agg(lo=(key, "min"), hi=(key, "max"), n=("ex", "size"), ex=("ex", "mean"), nxt=("next", "mean"),
                                    gain=("gain", "mean"), t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    S = F[F.sig]; N = F[~F.sig]
    out["sig_by_ma50"] = grp(S, "ma50", 5)
    out["nosig_by_ma50"] = grp(N, "ma50", 5)
    out["sig_by_ret60"] = grp(S, "ret60", 5)
    out["nosig_by_ret60"] = grp(N, "ret60", 5)
    out["sig_by_fc"] = grp(S, "fc", 5)
    out["sig_by_volratio"] = grp(S, "volratio", 5)
    out["sig_by_r0"] = grp(S, "r0", 5)
    return out
