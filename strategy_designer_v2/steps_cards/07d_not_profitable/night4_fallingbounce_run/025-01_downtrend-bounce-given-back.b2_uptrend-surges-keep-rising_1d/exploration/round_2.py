def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    R = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b["close"].pct_change()
            b["nxt"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"]*b["nxt"]
            b["vol20"] = r.rolling(20).std()
            b["ret60"] = b["close"]/b["close"].shift(60)-1
            b["ret90"] = b["close"]/b["close"].shift(90)-1
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            b["ret5"] = b["close"]/b["close"].shift(5)-1
            b["dist_hi"] = b["close"]/b["close"].rolling(60,min_periods=20).max()-1
            b["vr"] = b["vol20"]/r.rolling(60,min_periods=40).std()
            held = (b["pos"].abs()>1e-6).astype(int)
            grp = (held.diff()!=0).cumsum()
            b["days_in"] = held.groupby(grp).cumsum()
            b["fc0"] = (b["forecast"]<=0).astype(int)
            b["nxt_z"] = b["nxt"]/b["vol20"]
            b["coin"]=c; b["w"]=w
            R.append(b)
    R = pd.concat(R)
    H = R[R["pos"].abs()>1e-6].dropna(subset=["g"])
    out["held_overall"] = pd.Series({"bars_held": len(H), "share_bars_held": len(H)/R["nxt"].notna().sum(), "mean_g": H.g.mean(), "mean_pos": H.pos.mean(), "share_held_fc0": H.fc0.mean(), "mean_g_fc0": H[H.fc0==1].g.mean(), "mean_g_fcpos": H[H.fc0==0].g.mean(), "share_ret90_avail": H.ret90.notna().mean()})
    def bk(col, q=5, df=H):
        x = df.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, duplicates="drop")
        gg = x.groupby("b")
        res = gg.agg(n=("g","size"), mean_g=("g","mean"), std_g=("g","std"), sum_g=("g","sum"), mean_nxt=("nxt","mean"), pos=("pos","mean"), worst1pct=("g", lambda s: s.quantile(.01)), xmean=(col,"mean"))
        res["t"] = res.mean_g/(res.std_g/np.sqrt(res.n))
        return res
    for col in ["ret20","ret60","ret90","dist_hi","ret5","vr","vol20","days_in"]:
        out["held_by_"+col] = bk(col)
    # loss tail: worst 2% held-bar losses, what state
    q = H.g.quantile(0.02)
    L = H[H.g<=q]
    out["worst2pct_state_vs_all"] = pd.DataFrame({"worst": L[["ret20","ret60","dist_hi","vr","vol20","days_in","fc0","pos","nxt_z"]].mean(), "all_held": H[["ret20","ret60","dist_hi","vr","vol20","days_in","fc0","pos","nxt_z"]].mean()})
    out["worst2pct_sumshare"] = pd.Series({"share_of_total_losses": L.g.sum()/H.g[H.g<0].sum(), "sum_g_all": H.g.sum(), "sum_g_worst": L.g.sum()})
    # combo: ret20 sign x dist_hi
    x = H.dropna(subset=["ret20","dist_hi"]).copy()
    x["r20"] = np.where(x.ret20>0,"r20+","r20-")
    x["dh"] = pd.qcut(x.dist_hi,3,labels=["far","mid","near"])
    out["held_r20_x_disthi"] = x.groupby(["r20","dh"]).g.agg(["size","mean","sum"])
    return out
