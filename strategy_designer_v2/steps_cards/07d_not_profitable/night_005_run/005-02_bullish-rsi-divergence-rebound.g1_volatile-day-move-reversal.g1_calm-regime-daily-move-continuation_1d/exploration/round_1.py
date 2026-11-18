def explore(data):
    import pandas as pd, numpy as np
    out = {}
    out["coins"] = pd.Series({c: len(data["bars"][c]) for c in data["bars"]})
    rows = []
    fc = 'debug_info.components.calm_move.last_history_value'
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["ret1"]
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"] = c; b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["r5prev"] = b["close"]/b["close"].shift(5)-1
            b["fwd5"] = b["close"].shift(-5)/b["close"]-1
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["ret1"].mean()
    B["mkt"] = B["pos"]*B["coin"].map(mu)
    out["summary"] = pd.Series({
        "mean_gain": B["gain"].mean(), "mean_fee": B["fee"].mean(),
        "mean_mkt": B["mkt"].mean(), "mean_timing": (B["gain"]-B["mkt"]).mean(),
        "mean_abs_pos": B["pos"].abs().mean(), "share_long": (B["pos"]>0).mean(),
        "share_short": (B["pos"]<0).mean(), "share_flat": (B["pos"]==0).mean(),
        "mean_abs_poschange": (B["pos"]-B["previous_allocation"]).abs().mean()})
    B["side"] = np.sign(B["pos"])
    out["by_side"] = B.groupby("side").agg(n=("gain","size"), gain=("gain","mean"), fee=("fee","mean"), ret1=("ret1","mean"), abspos=("pos", lambda x: x.abs().mean()))
    B["fq"] = B.groupby("coin")["forecast"].transform(lambda x: pd.qcut(x.abs().rank(method="first"),5,labels=False))
    out["by_absfc_q"] = B.groupby("fq").agg(n=("gain","size"), gain=("gain","mean"), fee=("fee","mean"), abspos=("pos",lambda x:x.abs().mean()), absfc=("forecast",lambda x:x.abs().mean()))
    # position age: how long sign held
    B["fc_sign_change"] = (np.sign(B["forecast"]) != np.sign(B.groupby(["coin","w"])["forecast"].shift(1))).astype(int)
    out["sign_change_rate"] = B["fc_sign_change"].mean()
    out["corr_fc_lastfc"] = B[["forecast"]].assign(l=B.groupby(["coin","w"])["forecast"].shift(1)).corr().iloc[0,1]
    out["by_year"] = B.groupby("year").agg(gain=("gain","mean"), mkt=("mkt","mean"), fee=("fee","mean"), coinret=("ret1","mean"), longshare=("side", lambda x:(x>0).mean()))
    out["by_coin"] = B.groupby("coin").agg(gain=("gain","mean"), mkt=("mkt","mean"), fee=("fee","mean"), coinret=("ret1","mean"))
    # signed fwd5 by forecast quintile on non-overlapping grid
    g = B[B.groupby(["coin","w"]).cumcount()%5==0].copy()
    g["sx"] = np.sign(g["forecast"])*(g["fwd5"]-g["coin"].map(B.groupby("coin")["fwd5"].mean()))
    g["s1"] = np.sign(g["forecast"])*g["ret1"]
    out["grid_by_q"] = g.groupby("fq").agg(n=("sx","count"), sx5=("sx","mean"), s1=("s1","mean"))
    return out
