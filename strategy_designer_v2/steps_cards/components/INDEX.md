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
night_run | 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce_1d | CloseLocationComponent | built: CloseLocationInRangeComponent {"reference": "high"}
night_run | 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce_1d | DownMoveCloseLocationComponent | built: FallCloseLocationComponent {"vol_period": 60}
night_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds_1d | RelativeVolumeToMedian | built: VolumeRatioComponent {"exclude_current": 1, "period": 20, "statistic": "median"}
night_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.b1_weekend-move-reverses-three-days_1d | LaggedVolatilityScaledReturnComponent | built: VolatilityScaledReturnComponent {"lag": 1, "period": 1, "vol_period": 20}
night_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d | VolumeWeightedScaledReturn | exists: VolumeWeightedScaledReturnComponent {"vol_period": 20, "volume_period": 20}
night_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d | RelativeVolume | exists: VolumeRatioComponent {"period": 30}
night_run | 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse_1d | VolumeWeightedScaledReturn | exists: VolumeWeightedScaledReturnComponent {"vol_period": 20, "volume_period": 20}
volume_run | 012-01_liquidation-flush-rebound_1d | LowerWickComponent | exists: LowerWickComponent {"relative_to": "range"}
volume_run | 012-03_lower-wick-flush-recovery_1d | LowerWickShareComponent | exists: CloseLocationInRangeComponent {"reference": "low"}
volume_run | 012-04_flush-depth-retracement-size_1d | LowerWickComponent | exists: LowerWickComponent {"relative_to": "range"}
volume_run | 012-04_flush-depth-retracement-size_1d | OpenToLowDropComponent | exists: OpenToLowDropComponent {}
volume_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains_1d | VolumeMeanRatio | exists: VolumeRatioComponent {"period": 30, "short_period": 5}
volume_run | 013-04_heavy-volume-below-high-breakout_1d | VolumeMeanRatio | exists: VolumeRatioComponent {"period": 90, "short_period": 10}
volume_run | 003-03_heavy-volume-rise-continues_1d | volume-weighted rise | exists: VolumeWeightedScaledReturnComponent {"vol_period": 20, "volume_period": 30}
volume_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds_1d | VolumeToMedianRatio | exists: VolumeRatioComponent {"exclude_current": 1, "period": 20, "statistic": "median"}
volume_run | 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse_1d | VolumeWeightedScaledReturnComponent | exists: VolumeWeightedScaledReturnComponent {"vol_period": 20, "volume_period": 20}
night_013_run | 013-05_longer-stall-bigger-breakout_1d | StallUnderHighCountComponent | built: StallUnderHighCountComponent {"band": 10.0, "period": 365, "window": 60}
night_006_run | 006-05_downside-squeeze-break-continuation_1d | DistanceBelowPriorLow | built: DistanceFromHighComponent {"exclude_current": 1, "extreme": "low", "form": "percent", "period": 20, "source": "high"}
night_006_run | 006-05_downside-squeeze-break-continuation_1d | PriorRangeCompressionRatio | built: RangeCompressionRatioComponent {"exclude_current": 1, "long_period": 100, "short_period": 20}
night_006_run | 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d | RangeWidthRatio | built: RangeCompressionRatioComponent {"form": "width", "long_period": 100, "short_period": 20}
night_run | 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.g1_high-vol-down-day-rebound_1d | VolatilityRatioToAverageComponent | built: VolatilityRatioToAverageComponent {"vol_lookback": 60, "vol_period": 20}
night_005_run | 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d | RankWeightedScaledMoveComponent | built: RankWeightedScaledMoveComponent {"abs_period": 60, "lookback": 100, "vol_period": 20}
slow_1h_run | 016-01_up-grind-price-continuation_1h | grind-share-of-rise | built: RiseBeyondLargestMovesComponent {"k": 3, "period": 72}
slow_1h_run | 016-02_down-grind-price-continuation_1h | GrindShareOfFallComponent | built: LossShareBeyondLargestComponent {"k": 3, "period": 72}
slow_1h_run | 016-03_up-jump-price-reversal_1h | TopGainsShareOfRiseComponent | built: TopGainsShareOfRiseComponent {"k": 3, "period": 72}
slow_1h_run | 016-04_down-jump-price-reversal_1h | FallConcentrationShare | built: TopLossesShareOfFallComponent {"form": "share", "k": 3, "period": 72}
slow_1h_run | 016-05_up-even-volume-continuation_1h | VolumeEvenness | built: VolumeRatioComponent {"period": 72, "short_period": 72, "short_statistic": "median"}
slow_1h_run | 016-07_up-volume-burst-reversal_1h | VolumeConcentrationComponent | built: TopVolumesShareComponent {"period": 72, "top_k": 3}
slow_1h_run | 016-08_down-volume-burst-reversal_1h | VolumeTopShareComponent | exists: TopVolumesShareComponent {"period": 72, "top_k": 3}
intraday_1h_run | 017-01_presettle-drop-after-uptrend_1h | settlement clock | built: HoursToSettlementComponent {}
intraday_1h_run | 017-02_presettle-rise-after-downtrend_1h | HourOfDayComponent | built: HourOfDayComponent {}
intraday_1h_run | 017-03_postsettle-recovery-after-uptrend_1h | HourOfDayComponent | exists: HourOfDayComponent {}
intraday_1h_run | 017-04_postsettle-decline-after-downtrend_1h | HourOfDayComponent | exists: HourOfDayComponent {}
intraday_1h_run | 017-05_settlement-move-reverses-after_1h | HourOfDayComponent | exists: HourOfDayComponent {}
slow_1h_run | 016-01_up-grind-price-continuation_1h | GrindShareOfRise | built: TopGainsShareOfRiseComponent {"form": "residual", "k": 3, "period": 72}
slow_1h_run | 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h | VolRatioWeightedScaledReturn | built: VolatilityScaledReturnComponent {"period": 24, "vol_lookback": 720, "vol_period": 168}
night3_4h_run | 019-03_upward-breakout-quiet-continuation_4h | StretchToAverageBarRangeRatio | built: RangeCompressionRatioComponent {"base": "mean_bar_range", "exclude_current": 1, "form": "width", "long_period": 180, "short_period": 12}
night3_4h_run | 019-03_upward-breakout-quiet-continuation_4h | NarrowRangeBreakoutComponent | built: NarrowRangeBreakoutComponent {"base_period": 180, "period": 12}
night3_4h_run | 019-04_downward-breakout-quiet-continuation_4h | StretchRangeToAverageBarRange | built: RangeCompressionRatioComponent {"base": "mean_bar_range", "exclude_current": 2, "form": "compression", "long_period": 180, "short_period": 12}
night3_4h_run | 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h | BreakoutInMeanRangesComponent | built: BreakoutInMeanRangesComponent {"base_period": 180, "period": 12}
night3_4h_run | 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h | QuietWeekNarrowRangeBreakoutComponent | built: NarrowRangeBreakoutRangeRatioComponent {"base_period": 180, "period": 12, "ratio_long_period": 360, "ratio_short_period": 42}
night3_4h_run | 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h | PullbackInMeanRangesComponent | built: BreakoutInMeanRangesComponent {"base_period": 180, "period": 12, "side": "below"}
night3_4h_run | 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h | NarrowRangeBreakdownComponent | built: NarrowRangeBreakoutComponent {"base_period": 180, "period": 12, "side": "below"}
night3_4h_run | 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h | MeanBarRangeRatioComponent | built: MeanBarRangeRatioComponent {"long_period": 360, "short_period": 42}
night3_ichimoku_run | 021-01_above-rising-cloud-continues-up_1d | IchimokuCloudPositionComponent | built: IchimokuCloudPositionComponent {"displacement": 26, "kijun_period": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-01_above-rising-cloud-continues-up_1d | IchimokuCloudSlopeComponent | built: IchimokuCloudSlopeComponent {"displacement": 26, "kijun_period": 26, "lookback": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-02_below-falling-cloud-continues-down_1d | IchimokuCloudDistanceComponent | built: IchimokuCloudPositionComponent {"displacement": 26, "edge": "nearest", "kijun_period": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-02_below-falling-cloud-continues-down_1d | IchimokuCloudSlopeComponent | exists: IchimokuCloudSlopeComponent {"displacement": 26, "kijun_period": 26, "lookback": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-03_thin-cloud-upward-breakout_1d | IchimokuCloudPositionComponent | built: IchimokuCloudPositionComponent {"base": "close", "displacement": 26, "edge": "nearest", "kijun_period": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-03_thin-cloud-upward-breakout_1d | IchimokuCloudWidthComponent | built: IchimokuCloudWidthComponent {"displacement": 26, "kijun_period": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-04_thin-cloud-downward-breakdown_1d | IchimokuCloudPositionComponent | exists: IchimokuCloudPositionComponent {"base": "close", "displacement": 26, "edge": "nearest", "kijun_period": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-04_thin-cloud-downward-breakdown_1d | IchimokuCloudWidthComponent | exists: IchimokuCloudWidthComponent {}
night3_ichimoku_run | 021-03_thin-cloud-upward-breakout_1d | CloudCrossUpAgeComponent | built: IchimokuCloudCrossAgeComponent {"displacement": 26, "kijun_period": 26, "max_bars": 120, "senkou_period": 52, "tenkan_period": 9, "window": 250}
night3_ichimoku_run | 021-04_thin-cloud-downward-breakdown_1d | CloudThinnessBreakBelowComponent | built: IchimokuBelowCloudDistancePerWidthComponent {"displacement": 26, "kijun_period": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d | CloudFallGentlenessComponent | built: IchimokuCloudSlopeComponent {"displacement": 26, "form": "proximity", "kijun_period": 26, "lookback": 26, "senkou_period": 52, "tenkan_period": 9}
night3_ichimoku_run | 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d | IchimokuCloudThinness | built: IchimokuCloudWidthComponent {"form": "proximity"}
night3_levels_run | 020-01_resistance-retest-turns-down_1d | TurnDownLevelProximity | built: SwingHighProximityComponent {"period": 90, "power": 1.0, "side": 2}
night3_levels_run | 020-01_resistance-retest-turns-down_1d | TurnDownLevelTouchCount | built: SwingHighClusterCountComponent {"band": 2.0, "form": "count", "period": 90, "side": 2}
night3_levels_run | 020-02_support-retest-bounces-up_1d | SupportTouchCountComponent | built: SwingLowTouchNearnessComponent {"band": 1.5, "fall_period": 5, "period": 90, "side": 2}
night3_levels_run | 020-03_resistance-breakout-continues-up_1d | ResistanceBreakTouchCountComponent | built: ResistanceBreakTouchCountComponent {"band": 2.0, "cross_period": 1, "period": 90, "side": 2}
night3_levels_run | 020-03_resistance-breakout-continues-up_1d | LevelTouchCountComponent | built: SwingHighClusterCountComponent {"band": 2.0, "form": "count", "level": "below", "period": 90, "side": 2}
night3_levels_run | 020-04_support-breakdown-continues-down_1d | SupportTouchCount | built: SwingHighClusterCountComponent {"band": 1.0, "exclude_current": 1, "form": "count", "level": "above", "period": 90, "pivot": "low", "side": 2}
night3_levels_run | 020-04_support-breakdown-continues-down_1d | HeldLevelBreakDepth | built: TouchWeightedSupportBreakDepthComponent {"band": 2.0, "period": 90, "side": 2}
night3_levels_run | 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d | VolatilityScaledHighBreakComponent | built: VolatilityScaledDistanceFromHighComponent {"period": 20, "vol_period": 20}
night3_learned_run | 022-01_learned-combined-signal-score_1d | PastPredictivePowerWeightedCompositeComponent | built: PastPredictivePowerWeightedCompositeComponent {"corr_lookback": 365, "high_period": 90, "horizon": 5, "return_period": 28, "reversal_period": 1, "vol_period": 30, "z_window": 365}
night3_learned_run | 022-02_combination-beats-best-single_1d | RelearnedCombinationScore | built: PastPredictivePowerWeightedCompositeComponent {"corr_lookback": 365, "high_period": 90, "horizon": 5, "return_period": 28, "reversal_period": 1, "vol_period": 30, "weighting": "regression"}
night3_learned_run | 022-02_combination-beats-best-single_1d | PastBestSingleSignalScore | built: PastPredictivePowerWeightedCompositeComponent {"corr_lookback": 365, "high_period": 90, "horizon": 5, "return_period": 28, "reversal_period": 1, "vol_period": 30, "weighting": "best", "z_window": 365}
night3_learned_run | 022-03_combined-extremes-larger-moves_1d | PerformanceWeightedSignal | built: PastPredictivePowerWeightedCompositeComponent {"signal": "momentum", "weighting": "single"}
night3_learned_run | 022-04_signal-weights-carry-forward_1d | PastPredictivePowerWeightedSignal | exists: PastPredictivePowerWeightedCompositeComponent {"signal": "momentum", "weighting": "single"}
night3_learned_run | 022-04_signal-weights-carry-forward_1d | TrailingPredictivePower | built: SignalPredictivePowerComponent {"corr_lookback": 365, "horizon": 5, "signal": "momentum"}
night3_learned_run | 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d | centred-power counter-bet | built: ExcessPredictivePowerZComponent {"corr_lookback": 365, "high_period": 90, "horizon": 5, "mean_window": 365, "z_window": 365}
night3_1h_run | 018-02_hourly-breakout-multiday-continuation_1h | VolScaledBreakAboveHighComponent | built: VolScaledBreakAboveHighComponent {"period": 480, "step": 24, "steps": 30}
night3_1h_run | 018-02_hourly-breakout-multiday-continuation_1h | MeanAbsDailyReturnComponent | built: MeanAbsReturnComponent {"period": 24, "window": 720}
night3_1h_run | 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h | PlungeTimesMonthRiseComponent | built: MeanAbsScaledFallTimesRiseComponent {"fall_period": 24, "rise_period": 720, "window": 720}
night3_1h_run | 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h | ProximityWeightedSurgeComponent | built: HighProximityScaledReturnComponent {"period": 720, "power": 2.0, "return_period": 24, "window": 720}
night3_1h_run | 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h | DropInMeanAbsDailyMoves | built: MeanAbsScaledReturnComponent {"period": 24, "window": 720}
night3_1h_run | 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h | ReturnToMeanAbsReturnRatio | exists: MeanAbsScaledReturnComponent {"period": 24, "window": 720}
night3_1h_run | 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h | DailyDropToMeanAbsDailyReturn | exists: MeanAbsScaledReturnComponent {"period": 24, "window": 720}
intraday_1h_run | 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h | MeanAbsoluteMoveRankComponent | built: MeanAbsoluteMoveRankComponent {"lookback": 720, "period": 168}
night4_volumehour_run | 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h | FallTimesPriorRise | built: MeanAbsScaledFallTimesRiseComponent {"fall_period": 1, "rise_lag": 1, "rise_period": 24, "window": 720}
night4_fallingbounce_run | 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d | LowProximityScaledRiseComponent | built: LowProximityScaledRiseComponent {"period": 90, "vol_period": 20}
night4_panic_run | 027-01_panic-range-multiple-rebound_4h | PanicRangeMultipleComponent | built: FallGatedRangeMultipleComponent {"base_period": 180, "fall_period": 6, "period": 6}
night4_panic_run | 027-04_panic-delayed-recovery-drift_4h | LaggedPanicStretchIntensity | built: ScaledFallRangeMultipleComponent {"lag": 6, "period": 6, "window": 180}
night4_panic_run | 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h | FallGatedRangeMultipleTimesVolRatio | built: FallGatedRangeMultipleVolatilityRatioComponent {"base_period": 180, "fall_period": 6, "period": 6, "vol_lookback": 360, "vol_period": 42}
night4_panic_run | 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h | PriorFallGatedPanicComponent | built: PriorFallTimesScaledFallRangeMultipleComponent {"lag": 6, "period": 6, "prior_period": 540, "window": 180}
night4_panic_run | 027-01_panic-range-multiple-rebound.d2_panic-after-rising-week_4h | PanicTimesPriorWeekComponent | built: PriorSlideDiscountedScaledFallRangeMultipleComponent {"lag": 6, "period": 6, "prior_period": 42, "window": 180}
night4_panic_run | 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h | LaggedFallGatedRangeMultiple | built: FallGatedRangeMultipleComponent {"base_period": 180, "fall_period": 6, "lag": 6, "period": 6}
