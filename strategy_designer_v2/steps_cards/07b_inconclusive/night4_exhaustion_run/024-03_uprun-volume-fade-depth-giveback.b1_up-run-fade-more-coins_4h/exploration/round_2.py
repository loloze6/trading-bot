def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs.extend(c[idx + H] / c[idx] - 1)
        dm, ds = np.mean(rs), np.std(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            rg = b["debug_info.components.run_gain.last_history_value"].values
            vf = b["debug_info.components.vol_fade.last_history_value"].values
            cs = pd.Series(c)
            p30 = cs.pct_change(180).values
            p10 = cs.pct_change(60).values
            p90 = cs.pct_change(540).values
            up = (cs.diff() > 0).astype(int)
            # streak length
            sl = up.groupby((up != up.shift()).cumsum()).cumsum().values
            n = len(c)
            for start in range(0, n, H):
                cell = np.arange(start, min(start + H, n))
                hit = cell[f[cell] <= -2]
                if len(hit) == 0:
                    continue
                t = hit[0]
                if t + H >= n:
                    continue
                u = -(c[t + H] / c[t] - 1 - dm)
                rows.append({"coin": coin, "win": w, "rg": rg[t], "vf": vf[t],
                             "p30": p30[t], "p10": p10[t], "p90": p90[t],
                             "len": sl[t], "u18": u, "s18": u / ds})
    d = pd.DataFrame(rows)

    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    def ols(g, cols):
        g = g.dropna(subset=cols + ["u18"])
        X = np.column_stack([np.ones(len(g))] + [g[c].values for c in cols])
        y = -g["u18"].values  # unflipped drift-adjusted return
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.Series({**{f"b_{c}": b for c, b in zip(["const"] + cols, beta)},
                          **{f"t_{c}": b / s for c, b, s in zip(["const"] + cols, beta, se)}, "n": len(y)})

    out = {}
    out["rg_vf_describe"] = d[["rg", "vf", "len"]].describe()
    out["ols_all"] = ols(d, ["rg", "vf"])
    d["p30s"] = np.where(d["p30"] < 0, "p30_neg", "p30_pos")
    d["p90s"] = np.where(d["p90"] < 0, "p90_neg", "p90_pos")
    out["ols_by_p30sign"] = d.groupby("p30s").apply(lambda g: ols(g, ["rg", "vf"]))
    out["ols_by_p90sign"] = d.groupby("p90s").apply(lambda g: ols(g, ["rg", "vf"]))
    out["summ_by_p30sign"] = d.groupby("p30s").apply(summ)
    out["summ_by_p90sign"] = d.groupby("p90s").apply(summ)
    d["rgq"] = pd.qcut(d["rg"].rank(method="first"), 5, labels=False)
    out["rgq_x_p30sign"] = d.pivot_table(index="rgq", columns="p30s", values="u18", aggfunc="mean")
    out["rgq_x_p90sign"] = d.pivot_table(index="rgq", columns="p90s", values="u18", aggfunc="mean")
    out["ols_vf_within_rgq"] = d.groupby("rgq").apply(lambda g: ols(g, ["vf"]))
    out["by_len"] = d.groupby(d["len"].clip(upper=8)).apply(summ)
    d["p90q"] = pd.qcut(d["p90"].rank(method="first"), 5, labels=False)
    out["by_p90q"] = d.groupby("p90q").apply(summ)
    out["ols_rg_vf_p90"] = ols(d, ["rg", "vf", "p90"])
    return out
