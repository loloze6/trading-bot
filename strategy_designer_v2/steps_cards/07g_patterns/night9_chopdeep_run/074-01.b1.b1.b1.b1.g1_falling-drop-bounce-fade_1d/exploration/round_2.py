import pandas as pd, numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r1 = c.pct_change()
            rng = (h - l) / c.shift(1)
            rr = rng / rng.rolling(20).mean()
            sd20 = r1.rolling(20).std()
            sd30 = r1.rolling(30).std()
            ag = sd30.rolling(365, min_periods=200).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            f5 = (c.shift(1) / c.shift(6) - 1) / (sd20 * np.sqrt(5))
            r60 = c / c.shift(60) - 1
            nxt = c.shift(-1) / c - 1
            hl = (h - l).replace(0, np.nan)
            upw = (h - np.maximum(o, c)) / hl
            lw = (np.minimum(o, c) - l) / hl
            body = (c - o).abs() / hl
            df = pd.DataFrame({"coin": coin, "win": w, "day": b["timestamp"].astype(str).str[:10],
                               "r1": r1, "z1": r1 / sd20, "rr": rr, "f5": f5, "r60": r60, "ag": ag,
                               "upw": upw, "lw": lw, "body": body, "sd": sd20, "nxt": nxt,
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["u"] = D["nxt"] - D["coin"].map(drift)
    D["uz"] = D["u"] / D["sd"]
    D["trend"] = np.where(D["r60"] < -0.10, "falling", np.where(D["r60"] > 0.10, "rising", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = np.nan
    D["agit"] = np.where(D["ag"] > 0.5, "agitated", "calm"); D.loc[D["ag"].isna(), "agit"] = np.nan

    def ct(sub, col="u"):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": 0, "mean": np.nan, "t": np.nan})
        m = s[col].mean()
        g = s.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": len(g), "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    E = D.dropna(subset=["trend", "rr", "r1", "u", "upw"])
    F = E[E.trend == "falling"]
    # falling, all days with wide range: by upper-wick share tercile (wide = rr>1)
    Fw = F[F.rr > 1]
    out["falling_wide_by_upperwick_tercile"] = Fw.assign(q=pd.qcut(Fw.upw, 3, labels=False)).groupby("q").apply(ct).round(4)
    out["falling_wide_by_lowerwick_tercile"] = Fw.assign(q=pd.qcut(Fw.lw, 3, labels=False)).groupby("q").apply(ct).round(4)
    out["falling_wide_by_body_tercile"] = Fw.assign(q=pd.qcut(Fw.body, 3, labels=False)).groupby("q").apply(ct).round(4)
    # same for choppy and rising (upper wick)
    for tr in ["choppy", "rising"]:
        S = E[(E.trend == tr) & (E.rr > 1)]
        out[tr + "_wide_by_upperwick_tercile"] = S.assign(q=pd.qcut(S.upw, 3, labels=False)).groupby("q").apply(ct).round(4)
    # falling wide up days split by agitation
    Fu = F[(F.r1 > 0) & (F.rr > 1)].dropna(subset=["agit"])
    out["falling_wide_up_by_agitation"] = Fu.groupby("agit").apply(ct).round(4)
    # falling up-wide with f5 quartile x agitation
    Fu2 = Fu.dropna(subset=["f5"])
    Fu2 = Fu2.assign(q=pd.qcut(Fu2.f5, 2, labels=["deep", "shallow"]))
    out["falling_wide_up_f5half_x_agit"] = Fu2.groupby(["agit", "q"]).apply(ct).round(4)
    # choppy agitated short: wide up days next
    CA = E[(E.trend == "choppy") & (E.agit == "agitated") & (E.r1 > 0)]
    out["choppy_agitated_up_by_rr_half"] = CA.assign(q=pd.qcut(CA.rr, 2, labels=False)).groupby("q").apply(ct).round(4)
    # falling: next day by range ratio quartile, all days
    out["falling_all_by_rr_quartile_uz"] = F.assign(q=pd.qcut(F.rr, 4, labels=False)).groupby("q").apply(lambda s: ct(s, "uz")).round(3)
    # falling, upper wick graded: correlation within wide days
    out["falling_wide_corr_upw_u"] = float(Fw[["upw", "uz"]].corr().iloc[0, 1])
    out["falling_wide_n"] = len(Fw)
    # book: largest gain/loss days by f5 and upw
    A = D[D.alloc < 0].dropna(subset=["u"]).assign(sh=lambda s: -s.u)
    out["book_active_by_upperwick_half"] = A.assign(q=pd.qcut(A.upw, 2, labels=False)).groupby("q").apply(lambda s: ct(s, "sh")).round(4)
    return out
