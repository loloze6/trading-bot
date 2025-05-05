# core/strategy_base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import pandas as pd
import logging
import numpy as np


logger = logging.getLogger("trading_bot.strategies")

class Strategy(ABC):
    """Abstract base class for trading strategies."""
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate trading signals based on market data.
        
        Args:
            data: Market data as a DataFrame
            
        Returns:
            Dictionary with signal details (e.g., {'action': 'BUY', 'confidence': 0.8})
        """
        pass

class TechnicalIndicators:
    """Utility class for calculating technical indicators."""
    
    @staticmethod
    def add_moving_averages(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
        """
        Add simple moving averages to dataframe.
        
        Args:
            df: DataFrame with price data
            windows: List of periods for moving averages
            
        Returns:
            DataFrame with added moving average columns
        """
        df_copy = df.copy()
        for window in windows:
            df_copy[f'sma_{window}'] = df_copy['close'].rolling(window=window).mean()
        return df_copy
    
    @staticmethod
    def add_exponential_moving_averages(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
        """
        Add exponential moving averages to dataframe.
        
        Args:
            df: DataFrame with price data
            windows: List of periods for moving averages
            
        Returns:
            DataFrame with added EMA columns
        """
        df_copy = df.copy()
        for window in windows:
            df_copy[f'ema_{window}'] = df_copy['close'].ewm(span=window, adjust=False).mean()
        return df_copy
    
    @staticmethod
    def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index to dataframe.
        
        Args:
            df: DataFrame with price data
            window: RSI calculation period
            
        Returns:
            DataFrame with added RSI column
        """
        df_copy = df.copy()
        delta = df_copy['close'].diff()
        
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        rs = avg_gain / avg_loss
        df_copy[f'rsi_{window}'] = 100 - (100 / (1 + rs))
        
        return df_copy
    
    @staticmethod
    def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence) to dataframe.
        
        Args:
            df: DataFrame with price data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            
        Returns:
            DataFrame with added MACD columns
        """
        df_copy = df.copy()
        
        # Calculate MACD components
        ema_fast = df_copy['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df_copy['close'].ewm(span=slow, adjust=False).mean()
        
        df_copy['macd_line'] = ema_fast - ema_slow
        df_copy['macd_signal'] = df_copy['macd_line'].ewm(span=signal, adjust=False).mean()
        df_copy['macd_histogram'] = df_copy['macd_line'] - df_copy['macd_signal']
        
        return df_copy
    
    @staticmethod
    def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
        """
        Add Bollinger Bands to dataframe.
        
        Args:
            df: DataFrame with price data
            window: Moving average period
            num_std: Number of standard deviations for bands
            
        Returns:
            DataFrame with added Bollinger Bands columns
        """
        df_copy = df.copy()
        
        # Calculate Bollinger Bands
        df_copy['bb_middle'] = df_copy['close'].rolling(window=window).mean()
        df_copy['bb_std'] = df_copy['close'].rolling(window=window).std()
        
        df_copy['bb_upper'] = df_copy['bb_middle'] + (df_copy['bb_std'] * num_std)
        df_copy['bb_lower'] = df_copy['bb_middle'] - (df_copy['bb_std'] * num_std)
        
        # Calculate Bandwidth and %B
        df_copy['bb_bandwidth'] = (df_copy['bb_upper'] - df_copy['bb_lower']) / df_copy['bb_middle']
        df_copy['bb_percent_b'] = (df_copy['close'] - df_copy['bb_lower']) / (df_copy['bb_upper'] - df_copy['bb_lower'])
        
        return df_copy
    
    @staticmethod
    def add_atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Add Average True Range to dataframe.
        
        Args:
            df: DataFrame with price data
            window: ATR calculation period
            
        Returns:
            DataFrame with added ATR column
        """
        df_copy = df.copy()
        
        # Calculate True Range
        df_copy['tr1'] = abs(df_copy['high'] - df_copy['low'])
        df_copy['tr2'] = abs(df_copy['high'] - df_copy['close'].shift())
        df_copy['tr3'] = abs(df_copy['low'] - df_copy['close'].shift())
        
        df_copy['true_range'] = df_copy[['tr1', 'tr2', 'tr3']].max(axis=1)
        df_copy[f'atr_{window}'] = df_copy['true_range'].rolling(window=window).mean()
        
        # Drop intermediate columns
        df_copy.drop(['tr1', 'tr2', 'tr3', 'true_range'], axis=1, inplace=True)
        
        return df_copy
    
    @staticmethod
    def add_stochastic_oscillator(df: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> pd.DataFrame:
        """
        Add Stochastic Oscillator to dataframe.
        
        Args:
            df: DataFrame with price data
            k_window: %K period
            d_window: %D period (simple moving average of %K)
            
        Returns:
            DataFrame with added Stochastic Oscillator columns
        """
        df_copy = df.copy()
        
        # Calculate %K
        df_copy['lowest_low'] = df_copy['low'].rolling(window=k_window).min()
        df_copy['highest_high'] = df_copy['high'].rolling(window=k_window).max()
        
        df_copy['%K'] = 100 * ((df_copy['close'] - df_copy['lowest_low']) / 
                              (df_copy['highest_high'] - df_copy['lowest_low']))
        
        # Calculate %D
        df_copy['%D'] = df_copy['%K'].rolling(window=d_window).mean()
        
        # Drop intermediate columns
        df_copy.drop(['lowest_low', 'highest_high'], axis=1, inplace=True)
        
        return df_copy
    
    @staticmethod
    def add_volume_indicators(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Add volume-based indicators to dataframe.
        
        Args:
            df: DataFrame with price and volume data
            window: Calculation period
            
        Returns:
            DataFrame with added volume indicators
        """
        df_copy = df.copy()
        
        # Volume Moving Average
        df_copy['volume_sma'] = df_copy['volume'].rolling(window=window).mean()
        
        # Money Flow Index
        df_copy['typical_price'] = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3
        df_copy['money_flow'] = df_copy['typical_price'] * df_copy['volume']
        
        # Determine positive and negative money flow
        df_copy['price_change'] = df_copy['typical_price'].diff()
        df_copy['positive_flow'] = np.where(df_copy['price_change'] > 0, df_copy['money_flow'], 0)
        df_copy['negative_flow'] = np.where(df_copy['price_change'] < 0, df_copy['money_flow'], 0)
        
        # Calculate MFI
        positive_flow_sum = df_copy['positive_flow'].rolling(window=window).sum()
        negative_flow_sum = df_copy['negative_flow'].rolling(window=window).sum()
        
        mf_ratio = positive_flow_sum / negative_flow_sum
        df_copy['mfi'] = 100 - (100 / (1 + mf_ratio))
        
        # Cleanup
        df_copy.drop(['typical_price', 'money_flow', 'price_change', 'positive_flow', 'negative_flow'], 
                    axis=1, inplace=True)
        
        return df_copy