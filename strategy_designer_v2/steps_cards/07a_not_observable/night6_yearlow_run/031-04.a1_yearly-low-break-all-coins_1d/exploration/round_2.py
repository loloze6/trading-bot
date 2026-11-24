def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    # coin normal 10-bar drift and usual move on non-overlapping grid, all windows
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].reset_index(drop=True).values
            idx = np.arange(0, len(c) - 10, 10)
            rs += list(c[idx + 10] / c[idx] - 1)
        rs = np.array(rs)
        drift[coin] = rs.mean() if len(rs) else np.nan
        usual[coin] = rs.std(ddof=1) if len(rs) > 1 else np.nan
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            cell = np.arange(n) // 10
            c = b["close"].values
            fwd = np.full(n, np.nan)
            fwd[:n-10] = c[10:] / c[:n-10] - 1
            fc = b["forecast"].values
            mr = (b["regime"] == "mean_reversion").values
            depth = b["debug_info.components.depth.last_history_value"].values
            # band-based case marker (approx of step 5): rise of >=2 from lowest long level since last bet
            low = 0.0; bet = np.zeros(n, bool)
            for i in range(n):
                f = fc[i] if fc[i] > 0 else 0.0
                if f <= 0:
                    low = 0.0; continue
                low = min(low, f)
                if f - low >= 2:
                    bet[i] = True; low = f
            seen_cell_any = set(); seen_cell_bet = set()
            for i in range(n):
                if mr[i] and cell[i] not in seen_cell_any:
                    seen_cell_any.add(cell[i])
                    rows.append(dict(coin=coin, window=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     fwd=fwd[i], depth=depth[i], fc=fc[i], kind="first break bar"))
                if bet[i] and cell[i] not in seen_cell_bet:
                    seen_cell_bet.add(cell[i])
                    rows.append(dict(coin=coin, window=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     fwd=fwd[i], depth=depth[i], fc=fc[i], kind="band case"))
    D = pd.DataFrame(rows)
    D["unusual"] = D["fwd"] - D["coin"].map(drift)
    D["strength"] = D["unusual"] / D["coin"].map(usual)
    out = {}
    def clus(x):
        x = x.dropna(subset=["unusual"])
        g = x.groupby("day")["unusual"].apply(lambda s: (s - x["unusual"].mean()).sum())
        G = len(g); m = x["unusual"].mean()
        se = np.sqrt((g**2).sum() / len(x)**2 * G / (G - 1)) if G > 1 else np.nan
        return pd.Series(dict(cases=len(x), days=G, mean_unusual=m, t_day=m / se if se else np.nan,
                              std_unusual=x["unusual"].std(), strength=x["strength"].mean(),
                              mean_depth=x["depth"].mean(), mean_fc=x["fc"].mean()))
    out["by kind"] = D.groupby("kind").apply(clus)
    B = D[D.kind == "first break bar"].dropna(subset=["unusual"]).copy()
    B["depth_q"] = pd.qcut(B["depth"], 3, labels=["deepest", "mid", "shallow"])
    out["break cells by depth tercile"] = B.groupby("depth_q").apply(clus)
    out["break cells by year"] = B.groupby("year").apply(clus)
    out["band cases by coin"] = D[D.kind == "band case"].groupby("coin").size()
    out["band cases by year"] = D[D.kind == "band case"].groupby("year").size()
    out["share break cells forecast>=2"] = float((D[D.kind == "first break bar"]["fc"] >= 2).mean())
    out["corr depth vs unusual (break cells)"] = float(B[["depth", "unusual"]].corr().iloc[0, 1])
    out["spearman depth vs unusual"] = float(stats.spearmanr(B["depth"], B["unusual"])[0])
    return out
