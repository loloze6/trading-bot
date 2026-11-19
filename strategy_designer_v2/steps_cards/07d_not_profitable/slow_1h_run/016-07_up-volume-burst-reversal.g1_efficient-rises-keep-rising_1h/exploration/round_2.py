def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].values; n=len(c)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            pos = b["postRebalance_current_allocation"].fillna(0).values
            chg = np.abs(pos - b["previous_allocation"].fillna(0).values)
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            fc = b["forecast"].fillna(0).values
            s = pd.Series(c)
            regime = ((s/s.shift(48)>1)&(s/s.shift(72)>1)).values
            absr = s.pct_change().abs()
            er = (s.pct_change(72).abs()/absr.rolling(72).sum()).values
            er_raw = np.where(regime, er, 0.0)
            i = np.arange(n)
            # slow position: hold the position from every 24th bar for 24 bars
            slow = pd.Series(np.where(i%24==0, pos, np.nan)).ffill().fillna(0).values
            # raw ER position scaled to same mean as pos
            rawpos = er_raw/ (np.nanmean(er_raw[er_raw>0]) if (er_raw>0).any() else 1)*0.5
            rawpos = np.nan_to_num(rawpos)
            slowraw = pd.Series(np.where(i%24==0, rawpos, np.nan)).ffill().fillna(0).values
            df = pd.DataFrame({"coin":coin,"w":w,"r1":r1,"pos":pos,"chg":chg,"fee":fee,"fc":fc,
                "slow":slow,"rawpos":rawpos,"slowraw":slowraw,"reg":regime})
            rows.append(df)
    A = pd.concat(rows).dropna(subset=["r1"])
    feerate = (A.fee.sum()/A.chg.sum())
    out["fee_per_unit_turnover"] = feerate
    res = {}
    for p in ["pos","slow","rawpos","slowraw"]:
        x = A[p]
        prev = A.groupby(["coin","w"])[p].shift(1).fillna(0)
        turn = (x-prev).abs()
        g = (x*A.r1).mean()*24; f = turn.mean()*feerate*24
        res[p] = {"gross_day":g,"fee_day":f,"net_day":g-f,"turnover_day":turn.mean()*24,"mean_pos":x.mean()}
    out["variants"] = pd.DataFrame(res).T
    # share of turnover from regime flips vs within-regime fc changes
    prevreg = A.groupby(["coin","w"]).reg.shift(1).fillna(False)
    flip = A.reg != prevreg
    out["turnover_share_on_regime_flip"] = A.chg[flip].sum()/A.chg.sum()
    out["share_bars_flip"] = flip.mean()
    # forecast hourly abs change within regime
    inreg = A[A.reg & prevreg]
    out["mean_abs_fc_change_inregime"] = inreg.groupby(["coin","w"]).fc.diff().abs().mean()
    # mean regime spell length in hours
    sp = A.groupby(["coin","w"]).reg.apply(lambda r: (r!=r.shift()).cumsum()[r].value_counts().mean())
    out["mean_regime_spell_h"] = sp.mean()
    return out
