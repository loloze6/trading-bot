def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily returns
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w; rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["br"])
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1 + B["br"]).cumprod().values
    peak = np.maximum.accumulate(v)
    dd = v / peak - 1
    B["dd"] = dd
    i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(v[:i_tr + 1]))
    seg = B.iloc[i_pk:i_tr + 1]
    out["deepest_fall"] = pd.Series({"depth": dd[i_tr], "days": len(seg), "start_w": seg["wn"].iloc[0], "end_w": seg["wn"].iloc[-1],
                                     "start_year": seg["year"].iloc[0], "end_year": seg["year"].iloc[-1],
                                     "coin_ret_chain_during": float((1 + seg["cr"].fillna(0)).prod() - 1)})
    # top 5 distinct falls (episodes)
    eps = []; inep = False
    for k in range(len(dd)):
        if dd[k] < 0 and not inep: inep = True; s = k
        if inep and (dd[k] == 0 or k == len(dd) - 1):
            e = s + int(np.argmin(dd[s:k + 1])); eps.append((dd[e], s, e, k)); inep = False
    eps = sorted(eps)[:6]
    out["falls"] = pd.DataFrame([{"depth": a, "days_to_trough": e - s, "w_start": B["wn"].iloc[s], "year": B["year"].iloc[s],
                                  "coin_chain": float((1 + B["cr"].iloc[s:e + 1].fillna(0)).prod() - 1)} for a, s, e, k in eps])
    out["book_by_year"] = B.groupby("year").agg(mean=("br", "mean"), sd=("br", "std"), n=("br", "size"), mindd=("dd", "min"))
    # ---- cases
    cr = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            vol30 = r1.rolling(720, min_periods=200).std()
            idx = np.where(b["forecast"].values != 0)[0]
            for i in idx:
                if i + 48 >= len(b): continue
                f = b["forecast"].iloc[i]
                fwd = cl[i + 48] / cl[i] - 1
                # path: min along the way in direction
                path = cl[i + 1:i + 49] / cl[i] - 1
                sat = cl[i - 24] / cl[i - 48] - 1 if i >= 48 else np.nan
                sun = cl[i] / cl[i - 24] - 1 if i >= 24 else np.nan
                r7 = cl[i - 24] / cl[i - 192] - 1 if i >= 192 else np.nan
                r30 = cl[i] / cl[i - 720] - 1 if i >= 720 else np.nan
                cr.append(dict(coin=c, wn=int(w[1:]), year=ts.iloc[i].year, f=f, s=np.sign(f), fwd=fwd,
                               adv=np.min(np.sign(f) * path), alloc=b["postRebalance_current_allocation"].iloc[i],
                               sat=sat, sun=sun, r7=r7, r30=r30, vol=vol30.iloc[i]))
    C = pd.DataFrame(cr)
    mu = C.groupby("coin")["fwd"].transform("mean")
    C["ex"] = C["s"] * (C["fwd"])
    C["pnl"] = C["alloc"] * C["fwd"]
    C["af"] = C["f"].abs()
    def g(df, key):
        r = df.groupby(key).agg(n=("ex", "size"), mean_dir=("ex", "mean"), pnl=("pnl", "mean"), pnl_sd=("pnl", "std"),
                                worst_adv=("adv", lambda x: x.quantile(0.05)))
        r["t"] = df.groupby(key)["ex"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
        return r
    out["by_side"] = g(C, "s")
    C["fq"] = pd.qcut(C["af"], 5, labels=False, duplicates="drop")
    out["by_absforecast_q"] = g(C, "fq")
    out["by_year"] = g(C, "year")
    C["vq"] = C.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["by_vol_tercile"] = g(C, "vq")
    C["agree30"] = np.sign(C["r30"]) == C["s"]
    out["by_agree_30d_trend"] = g(C, "agree30")
    C["sun_agree"] = np.sign(C["sun"]) == C["s"]
    out["by_sunday_agrees"] = g(C, "sun_agree")
    out["by_coin"] = g(C, "coin")
    # pnl contribution of worst cases
    C2 = C.sort_values("pnl")
    out["pnl_share"] = pd.Series({"total_pnl": C["pnl"].sum(), "worst20_pnl": C2["pnl"].head(20).sum(),
                                  "best20_pnl": C2["pnl"].tail(20).sum(), "n": len(C), "mean_abs_alloc": C["alloc"].abs().mean()})
    return out
