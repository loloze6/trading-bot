from strategies.strategy_base import Strategy
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import logging
from strategies.strategy_base import TechnicalIndicators
import os


# For ML integration strat
try:
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# Registry of available strategies
STRATEGY_REGISTRY = {}

logger = logging.getLogger(__name__)  # Use the logger set up elsewhere

class SimpleMovingAverageStrategy(Strategy):
    """A simple strategy using moving average crossovers."""
    
    def __init__(self, short_window: int = 50, long_window: int = 200):
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on SMA crossover.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            Signal dictionary with 'action' key ('BUY', 'SELL', or 'HOLD')
        """
        if len(data) < self.long_window:
            logger.warning(f"Not enough data for SMA calculation. Need {self.long_window} periods.")
            return {'action': 'HOLD', 'reason': 'insufficient_data'}
        
        # Calculate moving averages
        data['short_ma'] = data['close'].rolling(window=self.short_window).mean()
        data['long_ma'] = data['close'].rolling(window=self.long_window).mean()
        
        # Get the most recent complete data point
        current = data.iloc[-1]
        previous = data.iloc[-2]
        
        # Check for crossover
        if pd.isna(current['short_ma']) or pd.isna(current['long_ma']):
            return {'action': 'HOLD', 'reason': 'incomplete_indicators'}
        
        # Generate signals
        if current['short_ma'] > current['long_ma'] and previous['short_ma'] <= previous['long_ma']:
            return {'action': 'BUY', 'reason': 'ma_crossover_bullish'}
        elif current['short_ma'] < current['long_ma'] and previous['short_ma'] >= previous['long_ma']:
            return {'action': 'SELL', 'reason': 'ma_crossover_bearish'}
        else:
            return {'action': 'HOLD', 'reason': 'no_crossover'}
        
class RSIStrategy(Strategy):
    """Trading strategy based on RSI (Relative Strength Index)."""
    
    def __init__(self, rsi_period: int = 14, 
                 oversold_threshold: int = 30, 
                 overbought_threshold: int = 70):
        """
        Initialize RSI strategy.
        
        Args:
            rsi_period: Period for RSI calculation
            oversold_threshold: RSI threshold for oversold condition (buy signal)
            overbought_threshold: RSI threshold for overbought condition (sell signal)
        """
        self.rsi_period = rsi_period
        self.oversold_threshold = oversold_threshold
        self.overbought_threshold = overbought_threshold
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on RSI values.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            Signal dictionary with 'action' key ('BUY', 'SELL', or 'HOLD')
        """
        if len(data) < self.rsi_period + 1:
            logger.warning(f"Not enough data for RSI calculation. Need at least {self.rsi_period + 1} periods.")
            return {'action': 'HOLD', 'reason': 'insufficient_data'}
        
        # Calculate RSI
        df = TechnicalIndicators.add_rsi(data, window=self.rsi_period)
        
        # Get the most recent complete data points
        current = df.iloc[-1]
        previous = df.iloc[-2]
        
        rsi_col = f'rsi_{self.rsi_period}'
        
        # Check for RSI signals
        if pd.isna(current[rsi_col]):
            return {'action': 'HOLD', 'reason': 'incomplete_indicators'}
        
        # Generate signals
        if current[rsi_col] < self.oversold_threshold and previous[rsi_col] >= self.oversold_threshold:
            return {'action': 'BUY', 'reason': 'rsi_oversold', 'confidence': 0.7}
        elif current[rsi_col] > self.overbought_threshold and previous[rsi_col] <= self.overbought_threshold:
            return {'action': 'SELL', 'reason': 'rsi_overbought', 'confidence': 0.7}
        else:
            return {'action': 'HOLD', 'reason': 'no_signal'}

class MACDStrategy(Strategy):
    """Trading strategy based on MACD (Moving Average Convergence Divergence)."""
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        Initialize MACD strategy.
        
        Args:
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line period
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on MACD crossovers.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            Signal dictionary with 'action' key ('BUY', 'SELL', or 'HOLD')
        """
        min_periods = max(self.fast_period, self.slow_period) + self.signal_period
        
        if len(data) < min_periods:
            logger.warning(f"Not enough data for MACD calculation. Need at least {min_periods} periods.")
            return {'action': 'HOLD', 'reason': 'insufficient_data'}
        
        # Calculate MACD
        df = TechnicalIndicators.add_macd(
            data, fast=self.fast_period, slow=self.slow_period, signal=self.signal_period)
        
        # Get the most recent complete data points
        current = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Check for MACD crossover signals
        if pd.isna(current['macd_line']) or pd.isna(current['macd_signal']):
            return {'action': 'HOLD', 'reason': 'incomplete_indicators'}
        
        # Generate signals based on MACD line crossing above/below signal line
        if (current['macd_line'] > current['macd_signal'] and 
            previous['macd_line'] <= previous['macd_signal']):
            # Bullish crossover
            confidence = min(0.9, 0.5 + abs(current['macd_histogram']) / 2)
            return {'action': 'BUY', 'reason': 'macd_bullish_crossover', 'confidence': confidence}
            
        elif (current['macd_line'] < current['macd_signal'] and 
              previous['macd_line'] >= previous['macd_signal']):
            # Bearish crossover
            confidence = min(0.9, 0.5 + abs(current['macd_histogram']) / 2)
            return {'action': 'SELL', 'reason': 'macd_bearish_crossover', 'confidence': confidence}
            
        else:
            return {'action': 'HOLD', 'reason': 'no_crossover'}

class BollingerBandsStrategy(Strategy):
    """Trading strategy based on Bollinger Bands."""
    
    def __init__(self, window: int = 20, num_std: float = 2.0):
        """
        Initialize Bollinger Bands strategy.
        
        Args:
            window: Moving average period
            num_std: Number of standard deviations for bands
        """
        self.window = window
        self.num_std = num_std
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on Bollinger Bands.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            Signal dictionary with 'action' key ('BUY', 'SELL', or 'HOLD')
        """
        if len(data) < self.window + 1:
            logger.warning(f"Not enough data for Bollinger Bands calculation. Need at least {self.window + 1} periods.")
            return {'action': 'HOLD', 'reason': 'insufficient_data'}
        
        # Calculate Bollinger Bands
        df = TechnicalIndicators.add_bollinger_bands(data, window=self.window, num_std=self.num_std)
        
        # Get the most recent complete data points
        current = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Check for Bollinger Bands signals
        if pd.isna(current['bb_upper']) or pd.isna(current['bb_lower']):
            return {'action': 'HOLD', 'reason': 'incomplete_indicators'}
        
        # Generate signals
        # Price crossing below lower band (buy signal)
        if previous['close'] <= previous['bb_lower'] and current['close'] > current['bb_lower']:
            return {'action': 'BUY', 'reason': 'price_crossed_above_lower_band', 'confidence': 0.65}
        
        # Price crossing above upper band (sell signal)
        elif previous['close'] >= previous['bb_upper'] and current['close'] < current['bb_upper']:
            return {'action': 'SELL', 'reason': 'price_crossed_below_upper_band', 'confidence': 0.65}
        
        # Price below lower band (potential buy)
        elif current['close'] < current['bb_lower']:
            return {'action': 'BUY', 'reason': 'price_below_lower_band', 'confidence': 0.55}
        
        # Price above upper band (potential sell)
        elif current['close'] > current['bb_upper']:
            return {'action': 'SELL', 'reason': 'price_above_upper_band', 'confidence': 0.55}
        
        else:
            return {'action': 'HOLD', 'reason': 'price_within_bands'}

class MultipleIndicatorStrategy(Strategy):
    """
    Trading strategy that combines multiple technical indicators for more robust signals.
    """
    
    def __init__(self):
        """Initialize the multiple indicator strategy."""
        # Initialize sub-strategies
        self.rsi_strategy = RSIStrategy(rsi_period=14, oversold_threshold=30, overbought_threshold=70)
        self.macd_strategy = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
        self.bb_strategy = BollingerBandsStrategy(window=20, num_std=2.0)
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on multiple indicators.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            Signal dictionary with 'action' key ('BUY', 'SELL', or 'HOLD')
        """
        # Generate signals from each strategy
        rsi_signal = self.rsi_strategy.generate_signals(data)
        macd_signal = self.macd_strategy.generate_signals(data)
        bb_signal = self.bb_strategy.generate_signals(data)
        
        # Count buy and sell signals
        buy_count = sum(1 for signal in [rsi_signal, macd_signal, bb_signal] 
                        if signal['action'] == 'BUY')
        sell_count = sum(1 for signal in [rsi_signal, macd_signal, bb_signal] 
                         if signal['action'] == 'SELL')
        
        # Calculate confidence based on agreement between strategies
        buy_confidence = buy_count / 3
        sell_confidence = sell_count / 3
        
        # Generate final signal
        if buy_count >= 2:
            return {'action': 'BUY', 'reason': 'multiple_indicators_agree', 'confidence': buy_confidence}
        elif sell_count >= 2:
            return {'action': 'SELL', 'reason': 'multiple_indicators_agree', 'confidence': sell_confidence}
        else:
            return {'action': 'HOLD', 'reason': 'indicators_disagree'}

class MLReadyStrategy(Strategy):
    """
    Strategy that prepares data for machine learning models and can use them for predictions.
    This is a placeholder for future ML integration.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize ML-ready strategy.
        
        Args:
            model_path: Path to saved ML model (if None, will use rule-based fallback)
        """
        self.model_path = model_path
        self.model = None
        self.feature_columns = []
        
        # Try to load model if available
        if ML_AVAILABLE and model_path and os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                logger.info(f"ML model loaded from {model_path}")
                # Note: In a real implementation, you would also load feature info
            except Exception as e:
                logger.error(f"Error loading ML model: {e}")
        
        # Fallback strategy when ML is not available
        self.fallback_strategy = MultipleIndicatorStrategy()
    
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for ML model.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            DataFrame with features for ML model
        """
        # Add technical indicators as features
        df = data.copy()
        
        # Add various technical indicators
        df = TechnicalIndicators.add_moving_averages(df, [5, 10, 20, 50])
        df = TechnicalIndicators.add_exponential_moving_averages(df, [5, 10, 20, 50])
        df = TechnicalIndicators.add_rsi(df, window=14)
        df = TechnicalIndicators.add_macd(df)
        df = TechnicalIndicators.add_bollinger_bands(df)
        df = TechnicalIndicators.add_atr(df)
        df = TechnicalIndicators.add_stochastic_oscillator(df)
        
        # Add price-based features
        df['price_change'] = df['close'].pct_change()
        df['price_range'] = (df['high'] - df['low']) / df['close']
        
        # Add lagged features
        for lag in [1, 2, 3, 5]:
            df[f'close_lag_{lag}'] = df['close'].shift(lag)
            df[f'volume_lag_{lag}'] = df['volume'].shift(lag)
        
        # Drop rows with NaN values
        df.dropna(inplace=True)
        
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals using ML model or fallback to rule-based strategy.
        
        Args:
            data: OHLCV data as a DataFrame
            
        Returns:
            Signal dictionary with 'action' key ('BUY', 'SELL', or 'HOLD')
        """
        if len(data) < 50:  # Need enough data for features
            logger.warning("Not enough data for ML feature generation")
            return {'action': 'HOLD', 'reason': 'insufficient_data'}
        
        # If we have a model, use it
        if self.model is not None:
            try:
                # Prepare features
                features_df = self._prepare_features(data)
                
                if features_df.empty:
                    logger.warning("Empty feature set after preparation")
                    return self.fallback_strategy.generate_signals(data)
                
                # Get the most recent feature set
                latest_features = features_df.iloc[-1:] 
                
                # Make prediction
                prediction = self.model.predict(latest_features)
                prediction_proba = self.model.predict_proba(latest_features)
                
                # Map prediction to action
                # This assumes the model predicts 0 (SELL), 1 (HOLD), 2 (BUY)
                action_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
                action = action_map.get(prediction[0], 'HOLD')
                
                # Get confidence
                confidence = np.max(prediction_proba)
                
                return {
                    'action': action,
                    'reason': 'ml_prediction',
                    'confidence': float(confidence)
                }
                
            except Exception as e:
                logger.error(f"Error using ML model: {e}")
                logger.info("Falling back to rule-based strategy")
                return self.fallback_strategy.generate_signals(data)
        
        # If no model is available, use the fallback strategy
        return self.fallback_strategy.generate_signals(data)

STRATEGY_REGISTRY["BollingerBands"] = BollingerBandsStrategy

class StrategyFactory:
    """Factory for creating strategy instances."""
    
    @staticmethod
    def create_strategy(strategy_name: str, params: Dict[str, Any]) -> Optional[Strategy]:
        """
        Create a strategy instance based on name and parameters.
        
        Args:
            strategy_name: Name of the strategy (must match a key in STRATEGY_REGISTRY)
            params: Parameters to pass to the strategy constructor
            
        Returns:
            Strategy instance or None if strategy_name is not recognized
        """
        strategy_class = STRATEGY_REGISTRY.get(strategy_name)
        
        if not strategy_class:
            logger.error(f"Unknown strategy: {strategy_name}")
            return None
        
        try:
            strategy_instance = strategy_class(**params)
            logger.info(f"Created strategy {strategy_name} with parameters {params}")
            return strategy_instance
        except Exception as e:
            logger.error(f"Error creating strategy {strategy_name}: {e}")
            return None