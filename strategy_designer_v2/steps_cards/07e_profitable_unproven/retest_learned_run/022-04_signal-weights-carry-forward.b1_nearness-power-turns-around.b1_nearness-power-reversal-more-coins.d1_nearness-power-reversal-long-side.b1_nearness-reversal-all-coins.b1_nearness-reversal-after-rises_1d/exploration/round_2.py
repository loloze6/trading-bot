def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for c, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].astype(float)
            b["coin"] = c; b["win"] = w
            for h in (5, 10):
                b[f"f{h}"] = cl.shift(-h) / cl - 1
            b["r30"] = cl / cl.shift(30) - 1
            b["r14"] = cl / cl.shift(14) - 1
            b["r60"] = cl / cl.shift(60) - 1
            b["near90"] = cl / b["high"].astype(float).rolling(90, min_periods=30).max() - 1
            lr = np.log(cl).diff()
            b["vol30"] = lr.rolling(30).std()
            b["i"] = np.arange(len(b))
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["fc"] = pd.to_numeric(b["forecast"], errors="coerce").fillna(0)
            b["raw"] = pd.to_numeric(b.get("debug_info.components.power_turn.last_history_value"), errors="coerce")
            rows.append(b[["coin","win","i","yr","f5","f10","r14","r30","r60","near90","vol30","fc","raw","regime"]])
    B = pd.concat(rows, ignore_index=True)
    for h in (5, 10):
        g = B[B["i"] % h == 0].dropna(subset=[f"f{h}","r30","near90","vol30"]).copy()
        g["ex"] = g[f"f{h}"] - g["coin"].map(g.groupby("coin")[f"f{h}"].mean())
        g["us"] = g["coin"].map(g.groupby("coin")[f"f{h}"].std())
        g["exs"] = g["ex"] / g["us"]
        tr = g[g.r30 > 0].copy()
        # multivariate in trend
        X = np.column_stack([np.ones(len(tr)), tr.r30.clip(0,3), tr.near90, (tr.fc>0).astype(float)*tr.fc])
        y = tr.exs.values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        out[f"multi_trend_h{h}"] = pd.DataFrame({"beta": beta, "t": beta/se}, index=["const","r30","near90","fc"]).round(4)
        # r30 graded inside trend, strength units
        tr["q"] = pd.qcut(tr.r30, 4, labels=False)
        out[f"r30_in_trend_q_h{h}"] = tr.groupby("q").agg(n=("exs","size"), strength=("exs","mean"), ex=("ex","mean"), r30=("r30","mean")).round(4)
        # near90 in trend
        tr["qn"] = pd.qcut(tr.near90, 4, labels=False, duplicates="drop")
        out[f"near90_in_trend_q_h{h}"] = tr.groupby("qn").agg(n=("exs","size"), strength=("exs","mean"), ex=("ex","mean")).round(4)
    g = B[B["i"] % 5 == 0].dropna(subset=["f5","r30","near90","vol30","r14","r60"]).copy()
    g["ex"] = g.f5 - g["coin"].map(g.groupby("coin")["f5"].mean())
    g["exs"] = g.ex / g["coin"].map(g.groupby("coin")["f5"].std())
    # r30 vol-scaled momentum over all bars
    for col in ("r14","r30","r60"):
        x = (g[col] / (g.vol30*np.sqrt(int(col[1:])))).clip(-5,5)
        r = stats.linregress(x, g.exs)
        out[f"volscaled_{col}_all"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(g)}"
    # per year: trend vs non trend strength
    g["trend"] = g.r30 > 0
    py = g.groupby(["yr","trend"])["exs"].mean().unstack().round(4)
    py["n"] = g.groupby("yr").size()
    out["year_trend_strength"] = py
    # per coin trend minus non trend
    pc = g.groupby(["coin","trend"])["ex"].mean().unstack()
    pc["diff"] = pc[True] - pc[False]
    out["coin_trend_diff"] = pc.round(4)
    # raw component sign in fc>0 cases: corr with near90
    a = g[g.fc > 0]
    out["fc>0_corr"] = pd.Series({"corr_fc_near90": a.fc.corr(a.near90), "corr_fc_r30": a.fc.corr(a.r30), "n": len(a)}).round(4)
    return out
