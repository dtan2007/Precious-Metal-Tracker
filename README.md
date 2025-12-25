# Precious Metals Portfolio Tracker

A full-stack web application for tracking precious metals investments (gold, silver, platinum, palladium). Monitor your purchases, view live spot prices, analyze historical trends with interactive charts, and calculate real-time profit/loss on your holdings.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- 📊 **Real-Time Dashboard** - View your complete portfolio at a glance
- 💵 **Live Spot Prices** - Fetches current precious metals prices from Metals-API
- 📈 **Historical Charts [FAKE DATA]** - Interactive 30-day price charts for gold and silver
- 💰 **Profit/Loss Tracking** - Automatic calculation of gains/losses and return percentages
- 🗂️ **Purchase Management** - Add, view, and delete purchase records
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 🔒 **Secure** - Environment variables for API keys and sensitive data

### Dashboard
View your complete portfolio with summary cards, current prices, holdings breakdown, and historical charts.

### Add Purchase
Simple form to record new bullion purchases with metal type, weight, price, and notes.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- A free API key from [MetalPriceAPI](https://metalpriceapi.com)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/dtan2007/precious-metals-tracker.git
cd precious-metals-tracker
```

2. **Create a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys:
# - Generate SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
# - Get METAL_PRICE_API_KEY from https://metalpriceapi.com
```

Your `.env` file should look like:
```
SECRET_KEY=your_generated_secret_key_here
METAL_PRICE_API_KEY=your_metalpriceapi_key_here
```

5. **Run the application:**
```bash
python app.py
```

6. **Open your browser:**
```
http://localhost:5000
```

## Usage

### Adding Your First Purchase

1. Click **"Add Purchase"** in the navigation bar
2. Select the metal type (Gold, Silver, Platinum, or Palladium)
3. Enter the weight in troy ounces (e.g., 1.00 for one ounce)
4. Enter the total price paid in USD
5. Select the purchase date
6. Optionally add notes (e.g., "American Silver Eagle from dealer X")
7. Click **"Add Purchase"**

### Understanding the Dashboard

- **Summary Cards**: Total invested, current value, profit/loss, and return percentage
- **Current Spot Prices**: Real-time prices per troy ounce for all four metals
- **Holdings by Metal**: Breakdown of your portfolio by metal type with individual profit/loss
- **Price Charts**: 30-day historical price trends for gold and silver
- **Purchase History**: Complete list of all your purchases with ability to delete

### Managing Your Portfolio

- **View Holdings**: All purchases are automatically aggregated by metal type
- **Track Performance**: Real-time profit/loss calculations based on current spot prices
- **Delete Purchases**: Click the delete button next to any purchase (with confirmation)
- **Export Data**: Your data is stored in a local SQLite database (`instance/database.db`)

## Tech Stack

### Backend
- **Python 3.12** - Programming language
- **Flask 3.0.0** - Web framework
- **SQLite** - Database (no setup required)
- **MetalPriceAPI** - Live precious metals prices

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Interactivity
- **Bootstrap 5.3** - Responsive CSS framework
- **Chart.js 4.4** - Interactive charts

### Tools
- **python-dotenv** - Environment variable management
- **requests** - HTTP library for API calls

## Project Structure

```
precious-metals-tracker/
├── app.py                      # Flask application and API routes
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── instance/
│   └── database.db            # SQLite database (auto-generated)
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       └── main.js            # Frontend JavaScript and charts
└── templates/
    ├── base.html              # Base template with navbar
    ├── index.html             # Dashboard page
    └── add_purchase.html      # Add purchase form
```

## API Configuration

This app uses [MetalPriceAPI](https://metalpriceapi.com) for precious metals pricing data.

**Free Tier:**
- 100 API requests per month
- Access to current spot prices
- No credit card required

**API Endpoints Used:**
- `/v1/latest` - Current spot prices

**Historical Data:**
The free tier does not include historical price data. The charts display mock historical data based on current prices with realistic variations. To get real historical data, you would need to either:
- Upgrade to a paid MetalPriceAPI plan
- Switch to a different API that provides historical data
- Store daily prices in your database over time

**Rate Limiting:**
Each dashboard page load uses 1 API request for live prices. The charts use mock data and don't consume API requests. With the free tier, you can load the dashboard about 100 times per month.

## Security

- **Environment Variables**: API keys and secrets stored in `.env` (not committed to git)
- **Secret Key**: Used for Flask session signing (generate a strong one!)
- **Input Validation**: Form inputs are validated on both client and server side
- **No Authentication**: Current version is single-user (runs locally)

**For Production Deployment:**
- Add user authentication
- Use a production WSGI server (Gunicorn, uWSGI)
- Use PostgreSQL instead of SQLite
- Enable HTTPS
- Implement rate limiting
- Add CSRF protection for forms

## Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Data export (CSV, PDF reports)
- [ ] Price alerts via email/SMS
- [ ] Mobile app (React Native or Flutter)
- [ ] More detailed analytics and reports
- [ ] Support for additional precious metals
- [ ] Integration with bullion dealers for purchase import
- [ ] Portfolio performance comparison with indices
- [ ] Tax reporting features
- [ ] Backup and restore functionality

## Troubleshooting

### "No module named 'dotenv'" Error
```bash
pip install python-dotenv
```

### Prices Showing $0.00
- Check that your `.env` file has a valid `METAL_PRICE_API_KEY`
- Verify the API key at https://metalpriceapi.com
- Check that you haven't exceeded the free tier limit (100 requests/month)
- Look for error messages in the terminal

### Charts Not Loading
- Hard refresh your browser (Ctrl+Shift+R or Ctrl+F5)
- Check browser console for JavaScript errors (F12 → Console)
- Ensure Chart.js is loading from CDN

### Database Errors
- Delete `instance/database.db` to reset the database
- The database will be automatically recreated on next run

### Port Already in Use
```bash
# Change the port in app.py (line at bottom):
app.run(debug=True, port=5001)  # Use 5001 instead of 5000
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [MetalPriceAPI](https://metalpriceapi.com) for providing precious metals pricing data
- [Bootstrap](https://getbootstrap.com) for the responsive CSS framework
- [Chart.js](https://www.chartjs.org) for beautiful, interactive charts
- [Flask](https://flask.palletsprojects.com) for the excellent Python web framework
