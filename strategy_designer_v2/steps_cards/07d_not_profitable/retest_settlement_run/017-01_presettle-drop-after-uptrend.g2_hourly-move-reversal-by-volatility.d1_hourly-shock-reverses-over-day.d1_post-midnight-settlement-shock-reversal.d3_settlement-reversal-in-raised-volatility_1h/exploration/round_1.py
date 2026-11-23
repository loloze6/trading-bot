def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # ---- book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["br"])
    v = (1 + B["br"]).cumprod().values
    peak = np.maximum.accumulate(v)
    dd = v / peak - 1
    B["dd"] = dd
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["by_window"] = B.groupby("wn").agg(n=("br", "size"), mean_br=("br", "mean"), sum_br=("br", "sum"), sum_cr=("cr", "sum"), mindd=("dd", "min"))
    out["by_year"] = B.groupby("year").agg(n=("br", "size"), mean_br=("br", "mean"), sd=("br", "std"), sum_cr=("cr", "sum"))
    # deepest fall location
    i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(v[:i_tr + 1]))
    seg = B.iloc[i_pk:i_tr + 1]
    out["deepest_fall"] = pd.Series({"depth": dd[i_tr], "days": len(seg), "windows": str(sorted(seg.wn.unique())),
                                     "year_start": int(seg.year.iloc[0]), "coin_sum_ret": seg.cr.sum(),
                                     "mean_book": seg.br.mean()})
    # ---- cases
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            r1 = pd.Series(cl).pct_change()
            s24 = r1.rolling(24).std()
            ratio = s24 / s24.rolling(720, min_periods=240).mean()
            fwd = pd.Series(cl).shift(-24) / pd.Series(cl) - 1
            r30 = pd.Series(cl) / pd.Series(cl).shift(720) - 1
            r7 = pd.Series(cl) / pd.Series(cl).shift(168) - 1
            r24 = pd.Series(cl) / pd.Series(cl).shift(24) - 1
            f = b["forecast"].values
            m = (ts.dt.hour.values == 0) & (f != 0)
            idx = np.where(m)[0]
            df = pd.DataFrame({"coin": c, "w": w, "f": f[idx], "fwd": fwd.values[idx], "ratio": ratio.values[idx],
                               "r30": r30.values[idx], "r7": r7.values[idx], "r24": r24.values[idx],
                               "s24": s24.values[idx], "year": ts.dt.year.values[idx]})
            cs.append(df)
    C = pd.concat(cs).dropna(subset=["fwd"])
    C["g"] = np.sign(C["f"]) * C["fwd"]
    C["side"] = np.where(C["f"] > 0, "long", "short")
    def agg(gb):
        r = gb["g"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r
    out["by_side"] = agg(C.groupby("side"))
    C["fq"] = pd.qcut(C["f"].abs(), 5, labels=False)
    out["by_absf_q"] = agg(C.groupby("fq"))
    C["rq"] = pd.qcut(C["ratio"], 5, labels=False)
    out["by_ratio_q"] = agg(C.groupby("rq"))
    C["sq"] = C.groupby("coin")["s24"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["by_s24_q_withincoin"] = agg(C.groupby("sq"))
    C["tr"] = np.sign(C["r30"]) * np.sign(C["f"])  # +1: fade direction with 30d trend
    out["by_with_trend30"] = agg(C.groupby("tr"))
    C["tr7"] = np.sign(C["r7"]) * np.sign(C["f"])
    out["by_with_trend7"] = agg(C.groupby("tr7"))
    out["by_coin"] = agg(C.groupby("coin"))
    out["by_year"] = agg(C.groupby("year"))
    # gain on fall days vs all: what share of cases in fall
    return out
