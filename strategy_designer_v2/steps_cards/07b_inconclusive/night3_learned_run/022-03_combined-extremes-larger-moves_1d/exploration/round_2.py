def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    comps = ["combined","s_momentum","s_reversal","s_high","s_volatility"]
    out = {}
    for h in (1, 5, 10, 20):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values
                n = len(b)
                for i in range(0, n - h, h):
                    d = {"coin": coin, "win": w, "r": c[i+h]/c[i]-1}
                    for k in comps:
                        col = f"debug_info.components.{k}.last_history_value"
                        d[k] = b[col].iloc[i] if col in b else np.nan
                    rows.append(d)
        df = pd.DataFrame(rows)
        df["u"] = df["r"] - df.groupby("coin")["r"].transform("mean")
        res = []
        for k in comps:
            s = df.dropna(subset=[k])
            q = s[k].abs().quantile(0.9)
            t = s[s[k].abs() >= q]
            su = np.sign(t[k]) * t["u"]
            L = su[t[k] > 0]; S = su[t[k] < 0]
            # all-cells slope of u on raw value
            sl = stats.linregress(s[k], s["u"])
            # top vs bottom quintile raw u, Welch
            q20, q80 = s[k].quantile([0.2, 0.8])
            hi = s[s[k] >= q80]["u"]; lo = s[s[k] <= q20]["u"]
            res.append({"comp": k, "n_cells": len(s), "top_n": len(t),
                        "top_mean": su.mean(), "top_t": su.mean()/(su.std()/np.sqrt(len(su))),
                        "long_n": len(L), "long_mean": L.mean(), "long_t": L.mean()/(L.std()/np.sqrt(len(L))),
                        "short_n": len(S), "short_mean": S.mean(), "short_t": S.mean()/(S.std()/np.sqrt(len(S))),
                        "slope_t_raw": sl.slope/sl.stderr,
                        "hiQ_minus_loQ": hi.mean()-lo.mean(),
                        "hiQ_lo_welch_t": stats.ttest_ind(hi, lo, equal_var=False).statistic})
        out[f"h{h}"] = pd.DataFrame(res)
        if h == 5:
            s = df.dropna(subset=["combined"]).copy()
            s["sgn"] = np.sign(s["combined"])
            out["h5_combined_sign_share_by_coin"] = s.groupby("coin")["sgn"].apply(lambda x: (x > 0).mean())
            out["h5_combined_sign_switch_rate"] = float(s.groupby(["coin","win"])["sgn"].apply(lambda x: (x.diff().abs() > 0).mean()).mean())
    return out
