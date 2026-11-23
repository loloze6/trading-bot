def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cs = []
    for c, ws in data["bars"].items():
        parts = []
        for w, b in ws.items():
            cl = b["close"].values; n = (len(cl) - 1) // 2
            parts += list(cl[2:2*n+1:2] / cl[0:2*n-1:2] - 1)
        drift = np.mean(parts)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; ts = pd.to_datetime(b["timestamp"])
            r1 = cl / cl.shift(1) - 1
            al = b["postRebalance_current_allocation"].fillna(0)
            pg = al * (cl.shift(-1) / cl - 1)
            g3 = pg + pg.shift(-1)  # sun->mon, mon->tue
            after = pg.shift(-2) + pg.shift(-3)  # gain carried beyond tuesday
            hold_tue = al.shift(-2)
            t = pd.DataFrame({"coin": c, "w": w, "wn": int(w[1:]), "sun": ts.dt.weekday == 6, "fc": b["forecast"],
                              "f2": cl.shift(-2) / cl - 1, "drift": drift, "pos2": g3, "after": after, "hold_tue": hold_tue,
                              "alloc": al, "vol20": r1.rolling(20).std(), "r7": cl / cl.shift(7) - 1,
                              "r60": cl / cl.shift(60) - 1, "rise": r1})
            cs.append(t)
    C = pd.concat(cs, ignore_index=True)
    C["un"] = -(C["f2"] - C["drift"])
    sig = C["sun"] & (C["fc"] < 0)
    S = C[sig].dropna(subset=["f2"]).copy()
    out["case_book"] = pd.Series({"mean_pos_gain_2d": S["pos2"].mean(), "mean_alloc": S["alloc"].mean(),
        "mean_un": S["un"].mean(), "share_still_held_tue": (S["hold_tue"].abs() > 1e-6).mean(),
        "mean_gain_after_tue": S["after"].mean(), "corr_alloc_un": np.corrcoef(-S["alloc"], S["un"])[0, 1]})
    # non-case position days
    C["pg"] = C.groupby(["coin", "w"])["alloc"].transform(lambda s: s) 
    # trades sanity
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    tr["ewd"] = pd.to_datetime(tr["entry_time"]).dt.weekday
    tr["xwd"] = pd.to_datetime(tr["exit_time"]).dt.weekday
    tr["px_ret_short"] = -(tr["exit_price"] / tr["entry_price"] - 1) * 100
    out["trades_by_entry_wd"] = tr.groupby("ewd").agg(n=("side", "size"), pl=("profit_loss_percent", "mean"), px=("px_ret_short", "mean"), dur=("duration_minutes", lambda s: s.mean() / 1440))
    out["trades_by_exit_wd"] = tr.groupby("xwd").agg(n=("side", "size"), pl=("profit_loss_percent", "mean"), px=("px_ret_short", "mean"))
    # condition alone checks, short direction, non-signal bars on a 2-bar grid
    N = C[~sig].dropna(subset=["f2", "vol20", "r7"]).iloc[::2]
    for col in ["vol20", "r7", "r60"]:
        cuts = S[col].quantile([0, .2, .4, .6, .8, 1]).values; cuts[0] = -np.inf; cuts[-1] = np.inf
        S["q"] = pd.cut(S[col], cuts, labels=False); N["q"] = pd.cut(N[col], cuts, labels=False)
        a = S.groupby("q").agg(un_sig=("un", "mean"), pos2=("pos2", "mean"), n_sig=("un", "size"))
        a["un_nosig"] = N.groupby("q")["un"].mean(); a["n_nosig"] = N.groupby("q")["un"].size()
        a["sd_sig"] = S.groupby("q")["un"].std()
        out["cond_" + col] = a
    # book drawdown: deepest falls and cases inside
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["wn"] = int(w[1:]); rows.append(t)
    D = pd.concat(rows)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index().reset_index()
    v = (1 + B["book_return"]).cumprod(); B["dd"] = (v / v.cummax() - 1).values
    trough = B["dd"].idxmin(); peak = v[:trough + 1].idxmax()
    seg = B.loc[peak:trough]
    out["deepest_fall"] = pd.Series({"depth": B["dd"].min(), "days": len(seg), "windows_spanned": seg["wn"].nunique(),
        "first_w": seg["wn"].min(), "last_w": seg["wn"].max(), "coin_ret_mean_daily": seg["coin_return"].mean(),
        "book_mean_daily": seg["book_return"].mean(), "yearly_ret": v.iloc[-1] ** (365 / len(B)) - 1})
    S["in_fall"] = S["wn"].between(seg["wn"].min(), seg["wn"].max())
    out["cases_in_fall_window_vs_not"] = S.groupby("in_fall").agg(un=("un", "mean"), pos2=("pos2", "mean"), n=("un", "size"),
        vol20=("vol20", "mean"), r7=("r7", "mean"), r60=("r60", "mean"))
    # worst decile of case outcomes: features
    S["worst"] = S["pos2"] <= S["pos2"].quantile(0.1)
    out["worst_cases_features"] = S.groupby("worst")[["vol20", "r7", "r60", "rise", "alloc", "un"]].mean()
    return out
