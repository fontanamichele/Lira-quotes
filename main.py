from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import yfinance as yf
import pandas as pd
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Finance Data API",
    description="API for real-time and historical financial data including currencies, stocks, ETFs, and cryptocurrencies",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class PriceData(BaseModel):
    ticker: str
    price: float
    currency: str
    timestamp: datetime

class HistoricalPriceData(BaseModel):
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: Optional[int] = None
    currency: str

async def get_asset_currency(ticker_symbol: str) -> str:
    """
    Get the actual currency of an asset from Yahoo Finance.
    Returns the currency code (e.g., 'USD', 'EUR', 'GBP').
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        currency = info.get('currency', 'USD')  # Default to USD if not found
        
        # Handle special cases for currency pairs
        if ticker_symbol.endswith('=X'):
            # For currency pairs, the currency is usually USD (the quote currency)
            return 'USD'
        
        return currency.upper()
    except Exception as e:
        logger.warning(f"Could not determine currency for {ticker_symbol}: {str(e)}")
        return 'USD'  # Default to USD

async def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Get exchange rate between two currencies.
    Returns the rate to convert from_currency to to_currency.
    """
    if from_currency == to_currency:
        return 1.0
    
    try:
        # Create currency pair ticker (e.g., USDEUR=X for USD to EUR)
        if from_currency == "USD":
            pair_ticker = f"{to_currency}USD=X"  # e.g., EURUSD=X
            # For EURUSD=X, we need to invert the rate to get USD/EUR
            ticker = yf.Ticker(pair_ticker)
            hist = ticker.history(period="1d", interval="1m")
            if not hist.empty:
                rate = hist['Close'].iloc[-1]
                return 1.0 / rate  # Invert to get USD/EUR
        elif to_currency == "USD":
            pair_ticker = f"{from_currency}USD=X"  # e.g., EURUSD=X
            ticker = yf.Ticker(pair_ticker)
            hist = ticker.history(period="1d", interval="1m")
            if not hist.empty:
                return hist['Close'].iloc[-1]
        else:
            # For non-USD pairs, convert through USD
            # First get from_currency to USD
            from_to_usd = await get_exchange_rate(from_currency, "USD")
            # Then get USD to to_currency
            usd_to_target = await get_exchange_rate("USD", to_currency)
            return from_to_usd * usd_to_target
        
        logger.warning(f"Could not fetch exchange rate for {from_currency} to {to_currency}")
        return 1.0
        
    except Exception as e:
        logger.error(f"Error fetching exchange rate {from_currency} to {to_currency}: {str(e)}")
        return 1.0

@app.get("/")
async def root():
    return {"message": "Finance Data API", "version": "1.0.0"}


@app.get("/prices/current", response_model=List[PriceData])
async def get_current_prices(
    tickers: List[str] = Query(..., description="List of any valid ticker symbols from Yahoo Finance"),
    currency: str = Query("USD", description="Currency for price conversion")
):
    """
    Get current prices for specified assets in the given currency.
    Supports any valid ticker symbol available on Yahoo Finance, including:
    - Stocks: AAPL, MSFT, GOOGL, etc.
    - ETFs: SPY, QQQ, VWCE.AS, etc.
    - Cryptocurrencies: BTC-USD, ETH-USD, etc.
    - Currency exchange rates: EURUSD=X, GBPUSD=X, USDJPY=X, etc.
    - Any other asset available on Yahoo Finance
    """
    try:
        if not tickers:
            raise HTTPException(status_code=400, detail="At least one ticker must be provided")
        
        prices = []
        failed_tickers = []
        
        for ticker in tickers:
            try:
                logger.info(f"Fetching current price for ticker: {ticker}")
                
                # Create yfinance ticker object
                asset = yf.Ticker(ticker)
                
                # Get current price data
                hist = asset.history(period="1d", interval="1m")
                
                if hist.empty:
                    logger.warning(f"No data available for ticker: {ticker}")
                    failed_tickers.append(ticker)
                    continue
                
                # Get the latest price and determine the asset's actual currency
                current_price = hist['Close'].iloc[-1]
                asset_currency = await get_asset_currency(ticker)
                
                # Convert to requested currency if different from asset's currency
                if currency.upper() != asset_currency:
                    exchange_rate = await get_exchange_rate(asset_currency, currency.upper())
                    current_price = current_price * exchange_rate
                
                prices.append(PriceData(
                    ticker=ticker,
                    price=round(current_price, 4),
                    currency=currency.upper(),
                    timestamp=datetime.now()
                ))
                
                logger.info(f"Successfully fetched price for {ticker}: {current_price}")
                
            except Exception as e:
                logger.error(f"Error getting price for {ticker}: {str(e)}")
                failed_tickers.append(ticker)
                continue
        
        if not prices:
            error_msg = f"No valid prices found for the provided tickers: {tickers}"
            if failed_tickers:
                error_msg += f". Failed tickers: {failed_tickers}"
            raise HTTPException(status_code=404, detail=error_msg)
        
        logger.info(f"Successfully returned prices for {len(prices)} out of {len(tickers)} tickers")
        return prices
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current prices: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/prices/historical", response_model=List[HistoricalPriceData])
async def get_historical_prices(
    tickers: List[str] = Query(..., description="List of any valid ticker symbols from Yahoo Finance"),
    currency: str = Query("USD", description="Currency for price conversion"),
    period: str = Query("1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"),
    interval: str = Query("1d", description="Interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")
):
    """
    Get historical prices for specified assets in the given currency.
    Supports any valid ticker symbol available on Yahoo Finance, including:
    - Stocks: AAPL, MSFT, GOOGL, etc.
    - ETFs: SPY, QQQ, VWCE.AS, etc.
    - Cryptocurrencies: BTC-USD, ETH-USD, etc.
    - Currency exchange rates: EURUSD=X, GBPUSD=X, USDJPY=X, etc.
    - Any other asset available on Yahoo Finance
    """
    try:
        if not tickers:
            raise HTTPException(status_code=400, detail="At least one ticker must be provided")
        
        historical_data = []
        failed_tickers = []
        
        for ticker in tickers:
            try:
                logger.info(f"Fetching historical data for ticker: {ticker}")
                
                # Create yfinance ticker object
                asset = yf.Ticker(ticker)
                
                # Get historical data
                hist = asset.history(period=period, interval=interval)
                
                if hist.empty:
                    logger.warning(f"No historical data available for ticker: {ticker} (period={period}, interval={interval})")
                    failed_tickers.append(ticker)
                    continue
                
                logger.info(f"Successfully fetched {len(hist)} records for {ticker}")
                
                # Get the asset's actual currency and exchange rate for conversion (if needed)
                asset_currency = await get_asset_currency(ticker)
                exchange_rate = 1.0
                if currency.upper() != asset_currency:
                    exchange_rate = await get_exchange_rate(asset_currency, currency.upper())
                
                # Convert to our format with currency conversion
                for date_idx, row in hist.iterrows():
                    historical_data.append(HistoricalPriceData(
                        ticker=ticker,
                        date=date_idx.date(),
                        open=round(row['Open'] * exchange_rate, 4),
                        high=round(row['High'] * exchange_rate, 4),
                        low=round(row['Low'] * exchange_rate, 4),
                        close=round(row['Close'] * exchange_rate, 4),
                        volume=int(row['Volume']) if pd.notna(row['Volume']) else None,
                        currency=currency.upper()
                    ))
                
            except Exception as e:
                logger.error(f"Error getting historical data for {ticker}: {str(e)}")
                failed_tickers.append(ticker)
                continue
        
        if not historical_data:
            error_msg = f"No valid historical data found for the provided tickers: {tickers}"
            if failed_tickers:
                error_msg += f". Failed tickers: {failed_tickers}"
            raise HTTPException(status_code=404, detail=error_msg)
        
        logger.info(f"Successfully returned {len(historical_data)} historical records for {len(tickers) - len(failed_tickers)} tickers")
        return historical_data
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting historical prices: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
