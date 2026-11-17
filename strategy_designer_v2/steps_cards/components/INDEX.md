# Components: one line per wish answered (run | plan id | wish | answer)

night_005_run | 005-01_bearish-rsi-divergence-giveback_1d | RsiDivergenceComponent | cannot build: The wished value is 0 on every bar whose close is not a 30-bar high. It jumps to the full RSI gap (RSI at the earlier peak minus RSI now) as soon as the close edges past the prior high, so it is an on/off event pulse, not a measure that grows continuously (rule 3); the gap is graded only inside the event. No exact graded form of "bearish RSI divergence at a new high" follows from the wish, so the research step should restate it as a continuous measure (for example the RSI gap on every bar, with nearness to the 30-bar high in a separate regime rule) before it can be built.
night_005_run | 005-02_bullish-rsi-divergence-rebound_1d | RsiLowDivergence | built: RsiChangeFromPriorLowComponent {"exclude": 3, "lookback": 30, "rsi_period": 14, "rsi_window": 100}
night_006_run | 006-04_upside-squeeze-break-continuation_1d | RangeCompressionRatioComponent | built: RangeCompressionRatioComponent {"long_period": 100, "short_period": 20}
night_006_run | 006-05_downside-squeeze-break-continuation_1d | RangeCompressionRatio | exists: RangeCompressionRatioComponent {"long_period": 100, "short_period": 20}
night_012_run | 012-01_liquidation-flush-rebound_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"period": 30}
night_012_run | 012-02_volume-burst-fall-reversal_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"period": 30}
night_012_run | 012-03_lower-wick-flush-recovery_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"period": 30}
night_012_run | 012-04_flush-depth-retracement-size_1d | LowerWickShareComponent | built: LowerWickShareComponent {}
night_012_run | 012-01_liquidation-flush-rebound_1d | LowerWickComponent | built: LowerWickPercentComponent {}
night_012_run | 012-03_lower-wick-flush-recovery_1d | LowerWickShareComponent | built: CloseLocationInRangeComponent {}
night_012_run | 012-04_flush-depth-retracement-size_1d | VolumeRatioComponent | built: VolumeRatioComponent {"exclude_current": 1, "period": 20}
night_012_run | 012-04_flush-depth-retracement-size_1d | OpenToLowDropComponent | built: OpenToLowDropComponent {}
night_013_run | 013-01_nearness-to-high-predicts-gains.d1_gain-concentrated-at-the-high_1d | ConvexHighProximityComponent | built: ConvexHighProximityComponent {"period": 365, "power": 2.0}
night_rsi_run | 010-01_rsi-above-share-continuation_1d | RSIShareAboveMidline | built: RsiAboveMidlineShareComponent {"period": 14, "rsi_window": 100, "window": 30}
night_rsi_run | 010-02_rsi-below-share-continuation_1d | RsiTimeBelowMidlineComponent | exists: RsiAboveMidlineShareComponent {"period": 14, "window": 30}
night_rsi_run | 010-03_rsi-above-streak-continuation_1d | RsiMidlineAgeComponent | built: RsiMidlineAgeComponent {"max_bars": 60, "period": 14, "rsi_window": 100}
night_rsi_run | 010-04_rsi-below-streak-continuation_1d | RsiMidlineAgeComponent | built: RsiMidlineAgeComponent {"max_bars": 60, "period": 14, "rsi_window": 100, "tie_side": "above"}
night_rsi_run | 010-05_rsi-above-share-reversal_1d | RsiTimeAboveMidlineComponent | exists: RsiAboveMidlineShareComponent {"period": 14, "window": 30}
night_rsi_run | 010-06_rsi-below-share-reversal_1d | RsiTimeBelowMidlineComponent | built: RsiAboveMidlineShareComponent {"period": 14, "rsi_window": 100, "side": "below", "window": 30}
night_rsi_run | 010-07_rsi-above-streak-reversal_1d | RsiMidlineAgeComponent | exists: RsiMidlineAgeComponent {"max_bars": 60, "period": 14, "rsi_window": 100, "tie_side": "below"}
night_rsi_run | 010-08_rsi-below-streak-reversal_1d | RsiSideAgeComponent | exists: RsiMidlineAgeComponent {"max_bars": 60, "period": 14, "rsi_window": 100, "tie_side": "below"}
night_013_run | 013-01_nearness-to-high-predicts-gains.d1_gain-concentrated-at-the-high_1d | HighProximityMomentumComponent | built: HighProximityMomentumComponent {"period": 365, "power": 2.0, "return_period": 30}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains_1d | VolumeRatioComponent | built: VolumeRatioComponent {"centred": 1, "period": 30, "short_period": 5}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"centred": 1, "exclude_current": 0, "period": 20, "short_period": 1}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g2_break-of-30-day-high_1d | PriorHighBreakoutDistance | built: DistanceFromHighComponent {"exclude_current": 1, "period": 30, "source": "high"}
night_013_run | 013-02_follow-through-stronger-near-high_1d | HighAnchoredMomentumComponent | built: HighProximityMomentumComponent {"period": 365, "power": 1.0, "proximity": "ratio", "return_period": 30}
night_013_run | 013-03_breakout-above-high-continues_1d | DistanceAbovePriorHighComponent | exists: DistanceFromHighComponent {"exclude_current": 1, "period": 20, "source": "close"}
night_013_run | 013-04_heavy-volume-below-high-breakout_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"centred": 1, "period": 90, "short_period": 10}
night_013_run | 013-05_longer-stall-bigger-breakout_1d | StallUnderHighCountComponent | cannot build: no answer passed the checks after 3 attempts
night_013_run | 013-06_breakout-volume-drives-continuation_1d | VolumeRatio | exists: VolumeRatioComponent {"period": 90}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"centred": 1, "exclude_current": 0, "period": 30, "short_period": 1}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d | RelativeVolumeComponent | exists: VolumeRatioComponent {"centred": 1, "exclude_current": 0, "period": 20, "short_period": 1}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d3_nearness-strongest-when-calm_1d | CalmScaledDistanceFromHigh | built: HighProximityVolatilityRatioComponent {"period": 365, "vol_lookback": 365, "vol_period": 20}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d | RelativeVolumeComponent | built: VolumeRatioComponent {"log": 1, "period": 30}
night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g1_rebound-grows-with-volatility_1d | VolRankedFallRebound | built: VolatilityRankedFallComponent {"lookback": 120, "vol_period": 20}
night_run | 003-01_thin-volume-rise-reverses_1d | RelativeVolumeComponent | exists: VolumeRatioComponent {"log": 1, "period": 30}
night_run | 003-02_thin-volume-drop-rebounds_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"log": 1, "period": 30}
night_run | 003-03_heavy-volume-rise-continues_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"period": 30}
night_run | 003-04_heavy-volume-drop-continues_1d | VolumeRatioComponent | exists: VolumeRatioComponent {"exclude_current": 1, "period": 30}
night_run | 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d | volume_ratio | exists: VolumeRatioComponent {"period": 60}
night_run | 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d | volume_weighted_fall | built: VolumeWeightedScaledReturnComponent {"vol_period": 20, "volume_period": 30}
