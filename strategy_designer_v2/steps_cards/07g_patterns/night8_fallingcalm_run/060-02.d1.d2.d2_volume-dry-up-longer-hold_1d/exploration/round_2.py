def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            m30 = v.rolling(30).mean()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "ret20": c / c.shift(20) - 1, "ret60": c / c.shift(60) - 1,
                "vr": np.log(m30 / m30.shift(30)),
                "vr10": np.log(v.rolling(10).mean() / v.rolling(10).mean().shift(10)),
                "sdrat": np.log(r1.rolling(20).std() / r1.rolling(60).std()),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"), "c": c})
            for H in (5, 10, 20):
                df["fwd%d" % H] = c.shift(-H) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def ctt(d, col):
        d = d.dropna(subset=[col])
        s = d.groupby("day")[col].sum()
        n = len(s)
        if n < 3: return pd.Series({"cases": len(d), "days": n, "mean": np.nan, "t": np.nan})
        m = d[col].mean()
        se = np.sqrt((s - s.mean()).pow(2).sum() * n / (n - 1)) / len(d)
        return pd.Series({"cases": len(d), "days": n, "mean": m, "t": m / se})
    out = {}
    for H in (5, 10, 20):
        G = A[(A["pos"] % H == 0) & A["fwd%d" % H].notna()].copy()
        drift = G.groupby("coin")["fwd%d" % H].mean()
        G["ex"] = G["fwd%d" % H] - G["coin"].map(drift)
        F = G[(G["ret60"] < -0.1)].dropna(subset=["vr"]).copy()
        F["z"] = F.groupby("coin")["vr"].transform(lambda s: (s - s.mean()) / s.std())
        F["sig"] = np.sign(F["vr"]) * F["ex"]   # long growth, short dry-up
        F["side"] = np.where(F["vr"] > 0, "growth", "dryup")
        F["ret20neg"] = np.where(F["ret20"] < -0.1, "r20<-10", "r20>=-10")
        F["agit"] = np.where(F["sdrat"] > 0, "agit_proxy", "calm_proxy")
        out["H%d_falling_signed" % H] = ctt(F, "sig")
        out["H%d_falling_by_side_ex" % H] = F.groupby("side").apply(lambda d: ctt(d, "ex"))
        out["H%d_by_ret20_signed" % H] = F.groupby("ret20neg").apply(lambda d: ctt(d, "sig"))
        out["H%d_by_agit_signed" % H] = F.groupby("agit").apply(lambda d: ctt(d, "sig"))
        out["H%d_rho_vr_ex_falling" % H] = pd.Series({"n": len(F), "rho": stats.spearmanr(F["vr"], F["ex"])[0]})
        if H == 20:
            F["half"] = np.where(F["w"].str[1:].astype(int) <= 12, "w7-12", "w13-18")
            out["H20_by_half_signed"] = F.groupby("half").apply(lambda d: ctt(d, "sig"))
            out["H20_by_coin_rho"] = F.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "rho": stats.spearmanr(d["vr"], d["ex"])[0] if len(d) > 4 else np.nan}))
            F["vq"] = pd.qcut(F["z"], 4, labels=False)
            out["H20_vr_quartile_ex"] = F.groupby("vq").apply(lambda d: ctt(d, "ex"))
            F10 = F.dropna(subset=["vr10"]).copy()
            out["H20_rho_vr10"] = pd.Series({"n": len(F10), "rho": stats.spearmanr(F10["vr10"], F10["ex"])[0]})
            R = G[(G["ret60"] > 0.1)].dropna(subset=["vr"]).copy()
            R["sig"] = -np.sign(R["vr"]) * R["ex"]
            out["H20_rising_signed_contrarian"] = ctt(R, "sig")
            C = G[(G["ret60"].abs() <= 0.1)].dropna(subset=["vr"]).copy()
            C["sig"] = np.sign(C["vr"]) * C["ex"]
            out["H20_choppy_signed"] = ctt(C, "sig")
    return out
