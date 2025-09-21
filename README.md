# Finance Data API

[![CI/CD Pipeline](https://github.com/yourusername/finance-data-api/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/finance-data-api/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive API provider for personal finance tracking applications that provides real-time and historical data for currencies, stocks, ETFs, and cryptocurrencies using the yfinance library.

## 🌟 Features

- **Multi-Asset Support**: Stocks, ETFs, cryptocurrencies, and currency exchange rates
- **Smart Currency Conversion**: Automatic detection of asset currencies with real-time conversion
- **Real-time Data**: Current prices for all supported assets
- **Historical Data**: Historical price data with flexible time periods and intervals
- **RESTful API**: Clean and intuitive API endpoints with automatic documentation
- **FastAPI Framework**: High-performance async API with built-in validation
- **Any Ticker Support**: Works with any valid ticker symbol from Yahoo Finance

## 🚀 Quick Start

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/finance-data-api.git
cd finance-data-api
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Supported Assets

The API supports **any valid ticker symbol** available on Yahoo Finance, including:

- **Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, and any other stock
- **ETFs**: SPY, QQQ, VTI, VWCE.AS, IWDA.AS, and any other ETF
- **Cryptocurrencies**: BTC-USD, ETH-USD, BNB-USD, XRP-USD, and any other crypto
- **Currency Exchange Rates**: EURUSD=X, GBPUSD=X, USDJPY=X, and any other currency pair
- **Any other asset** available on Yahoo Finance

## API Endpoints

### 1. Get Current Prices

```
GET /prices/current?tickers={ticker1,ticker2}&currency={currency}
```

- **tickers** (required): Comma-separated list of asset tickers
- **currency** (optional): Currency for price conversion (default: USD). All prices are converted from USD using real-time exchange rates
- Returns current prices for specified assets in the requested currency

### 2. Get Historical Prices

```
GET /prices/historical?tickers={ticker1,ticker2}&currency={currency}&period={period}&interval={interval}
```

- **tickers** (required): Comma-separated list of asset tickers
- **currency** (optional): Currency for price conversion (default: USD). All prices are converted from USD using real-time exchange rates
- **period** (optional): 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max (default: 1mo)
- **interval** (optional): 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo (default: 1d)
- Returns historical price data for specified assets in the requested currency

## Example Usage

### Get current prices for Apple and Tesla in USD

```bash
curl "http://localhost:8000/prices/current?tickers=AAPL,TSLA&currency=USD"
```

### Get current prices for Apple and Tesla in EUR

```bash
curl "http://localhost:8000/prices/current?tickers=AAPL,TSLA&currency=EUR"
```

### Get historical prices for Bitcoin in USD

```bash
curl "http://localhost:8000/prices/historical?tickers=BTC-USD&period=1y&interval=1d"
```

### Get historical prices for Bitcoin in EUR

```bash
curl "http://localhost:8000/prices/historical?tickers=BTC-USD&period=1y&interval=1d&currency=EUR"
```

### Get current price for VWCE (European ETF) in EUR

```bash
curl "http://localhost:8000/prices/current?tickers=VWCE.AS&currency=EUR"
```

### Get current price for VWCE (European ETF) in USD

```bash
curl "http://localhost:8000/prices/current?tickers=VWCE.AS&currency=USD"
```

### Get current exchange rates

```bash
curl "http://localhost:8000/prices/current?tickers=EURUSD=X,GBPUSD=X,USDJPY=X"
```

### Get historical exchange rates

```bash
curl "http://localhost:8000/prices/historical?tickers=EURUSD=X&period=1y&interval=1d"
```

### Get prices for any asset

```bash
# Any stock
curl "http://localhost:8000/prices/current?tickers=NVDA&currency=USD"

# Any ETF (including European ones) - VWCE is natively in EUR
curl "http://localhost:8000/prices/current?tickers=VWCE.AS&currency=EUR"

# Any cryptocurrency
curl "http://localhost:8000/prices/current?tickers=SOL-USD&currency=USD"

# Any currency pair
curl "http://localhost:8000/prices/current?tickers=EURGBP=X&currency=USD"
```

**Notes:**

- European ETFs require exchange suffixes (e.g., `.AS` for Amsterdam, `.DE` for Deutsche Börse, `.MI` for Milan)
- Currency exchange rates use the `=X` suffix (e.g., `EURUSD=X` for Euro to US Dollar rate)
- The API supports **any valid ticker symbol** available on Yahoo Finance
- **Smart Currency Conversion**: The API automatically detects each asset's actual currency and converts to the requested currency using real-time exchange rates
- Supported currencies include: USD, EUR, GBP, JPY, CHF, CAD, AUD, and many more

## Error Handling

The API includes comprehensive error handling:

- Invalid tickers are skipped with warnings
- Invalid categories return 400 errors
- Missing data returns appropriate HTTP status codes
- All errors are logged for debugging

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **yfinance**: Yahoo Finance data downloader
- **pandas**: Data manipulation and analysis
- **uvicorn**: ASGI server for running the API
- **pydantic**: Data validation using Python type annotations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 🚀 Free Deployment Options

### Railway (Recommended) ⭐

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-deploys! 🎉

**Benefits**: $5 free credit monthly, no cold starts, automatic deployments

### Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create "Web Service" from your repo
4. Deploy automatically

**Benefits**: 750 free hours/month, custom domains

### Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

**Benefits**: 3 free VMs, global deployment

### Docker Deployment

```bash
docker build -t finance-data-api .
docker run -p 8000:8000 finance-data-api
```

📖 **Detailed deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📊 API Status

The API uses Yahoo Finance as its data source. Please note:

- Data availability depends on Yahoo Finance
- Some assets may not be available in all regions
- Rate limiting may apply for high-frequency requests

## 🐛 Known Issues

- Some European ETFs may have limited historical data
- Currency conversion rates are updated in real-time but may have slight delays
- Weekend and holiday data may be limited

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for providing financial data
- [yfinance](https://github.com/ranaroussi/yfinance) library for data access
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [pandas](https://pandas.pydata.org/) for data manipulation

## 📞 Support

If you have any questions or need help, please:

- Open an [issue](https://github.com/yourusername/finance-data-api/issues)
- Check the [documentation](http://localhost:8000/docs) when running locally
- Review the [contributing guide](CONTRIBUTING.md)

---

⭐ If you found this project helpful, please give it a star on GitHub!
