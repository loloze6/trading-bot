from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
import pandas as pd
import logging

logger = logging.getLogger(__name__)  # Use the logger set up elsewhere

def convert_fetch_interval(fetch_interval):
    INTERVAL_MAP = {
        60: '1m',
        300: '5m',
        900: '15m',
        3600: '1h',
        86400: '1d'
    }
    return INTERVAL_MAP.get(fetch_interval, '1m')  # Défaut à '1m' si non trouvé


class DataManager:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
        # self.trading_pair = TRADING_PAIR
        # self.interval_conv = convert_fetch_interval(FETCH_INTERVAL)  # Pour get_klines

    # def fetch_latest_price(self):
    #     try:
    #         klines = self.client.get_klines(symbol=self.trading_pair, interval=self.interval_conv, limit=2)
    #         close_price = float(klines[-1][4])
    #         return close_price
    #     except Exception as e:
    #         raise RuntimeError(f"Invalid configuration. Please check your settings. {e}")
        
    
    def get_historical_klines(self, symbol: str, interval: str, 
                              limit: int = 500) -> pd.DataFrame:
        """
        Fetch historical kline (candlestick) data.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            interval: Kline interval (e.g., '1h', '15m', '1d')
            limit: Number of klines to retrieve
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            logger.info(f"Fetching {limit} klines for {symbol} at {interval} interval")
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convert types
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching klines: {e}")
            return pd.DataFrame()