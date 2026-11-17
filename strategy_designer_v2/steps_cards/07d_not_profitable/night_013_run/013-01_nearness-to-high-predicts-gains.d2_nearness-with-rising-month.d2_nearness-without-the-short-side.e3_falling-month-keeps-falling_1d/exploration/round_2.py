def explore(data):
    import numpy as np, pandas as pd
    out = {}
    G = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r30 = cl / cl.shift(30) - 1
            r90 = cl / cl.shift(90) - 1
            fwd = cl.shift(-3) / cl - 1
            idx = np.arange(0, len(b), 3)
            g = pd.DataFrame({"fc": b["forecast"].values[idx], "fwd": fwd.values[idx],
                              "r30": r30.values[idx], "r90": r90.values[idx],
                              "pos": b["postRebalance_current_allocation"].values[idx]})
            g["coin"] = c; g["win"] = w
            G.append(g)
    G = pd.concat(G).dropna(subset=["fwd"])
    G["exc"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    act = G[(G["fc"] < 0)].dropna(subset=["r90"]).copy()
    act["up90"] = act["r90"] > 0
    act["deep"] = act["fc"] < act["fc"].median()
    tt = lambda x: x.mean() / x.std() * np.sqrt(len(x))
    out["active_up90_x_deep"] = act.groupby(["up90", "deep"]).agg(n=("exc", "size"), exc=("exc", "mean"), t=("exc", tt), fc=("fc", "mean"))
    # graded: r90 terciles among active
    act["r90q"] = pd.qcut(act["r90"], 4, labels=False)
    out["active_by_r90_quartile"] = act.groupby("r90q").agg(n=("exc", "size"), exc=("exc", "mean"), t=("exc", tt), r90=("r90", "mean"))
    # gap r30 - r90/3 : fall of month relative to quarter
    act["gap"] = act["r30"] - act["r90"]
    act["gq"] = pd.qcut(act["gap"], 4, labels=False)
    out["active_by_month_minus_quarter_quartile"] = act.groupby("gq").agg(n=("exc", "size"), exc=("exc", "mean"), t=("exc", tt), gap=("gap", "mean"))
    # book daily return by up90 state
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            up = (cl / cl.shift(90) - 1) > 0
            v = b["postRebalance_total_value"]
            r = b["total_portfolio_value"].shift(-1) / v - 1
            pos = b["postRebalance_current_allocation"]
            df = pd.DataFrame({"r": r, "up": up, "pos": pos, "has90": cl.shift(90).notna()})
            rows.append(df[df["has90"] & (df["pos"] != 0)])
    R = pd.concat(rows).dropna(subset=["r"])
    out["book_bar_return_when_short_by_up90"] = R.groupby("up").agg(n=("r", "size"), mean=("r", "mean"), sh=("r", lambda x: x.mean() / x.std() * np.sqrt(365)))
    return out
