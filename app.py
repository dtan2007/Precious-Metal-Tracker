from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-only-for-local-testing')

DATABASE = 'instance/database.db'

def get_db():
    """Connect to database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metal_type TEXT NOT NULL,
            weight_oz REAL NOT NULL,
            price_paid REAL NOT NULL,
            purchase_date TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_live_prices():
    api_key = os.getenv('METAL_PRICE_API_KEY')
    
    #fake data
    mock_prices = {
        'gold': 2050.00,
        'silver': 25.50,
        'platinum': 950.00,
        'palladium': 1050.00
    }
    
    if not api_key:
        print("No METAL_PRICE_API_KEY found in .env file - using mock data")
        return mock_prices
    
    try:
        # 100 req/month
        url = f'https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=XAU,XAG,XPT,XPD'
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            print(f"API request failed with status {response.status_code} - using mock data")
            return mock_prices
        
        data = response.json()
        
        print("🔍 DEBUG - API Response:")
        print(f"   Success: {data.get('success', 'Not found')}")
        print(f"   Rates: {data.get('rates', 'Not found')}")
        
        if not data.get('success', False):
            print(f"⚠️  API error: {data.get('error', 'Unknown error')} - using mock data")
            return mock_prices
        
        # need to do 1/rates from metalpriceapi
        rates_data = data['rates']
        
        rates = {
            'gold': 1 / rates_data.get('XAU', 1) if rates_data.get('XAU', 0) > 0 else 0,
            'silver': 1 / rates_data.get('XAG', 1) if rates_data.get('XAG', 0) > 0 else 0,
            'platinum': 1 / rates_data.get('XPT', 1) if rates_data.get('XPT', 0) > 0 else 0,
            'palladium': 1 / rates_data.get('XPD', 1) if rates_data.get('XPD', 0) > 0 else 0
        }
        
        print(f"Parsed prices: Gold=${rates['gold']:.2f}, Silver=${rates['silver']:.2f}")
        
        return rates
    except requests.exceptions.Timeout:
        print("API request timed out - using mock data")
        return mock_prices
    except Exception as e:
        print(f"Error fetching prices: {e} - using mock data")
        return mock_prices

@app.route('/')
def index():
    """Dashboard page"""
    conn = get_db()
    purchases = conn.execute('SELECT * FROM purchases ORDER BY purchase_date DESC').fetchall()
    conn.close()
    
    prices = get_live_prices()
    
    portfolio = {
        'gold': {'weight': 0.0, 'cost': 0.0},
        'silver': {'weight': 0.0, 'cost': 0.0},
        'platinum': {'weight': 0.0, 'cost': 0.0},
        'palladium': {'weight': 0.0, 'cost': 0.0}
    }
    
    for purchase in purchases:
        metal = purchase['metal_type']
        portfolio[metal]['weight'] += float(purchase['weight_oz'])
        portfolio[metal]['cost'] += float(purchase['price_paid'])
    
    total_cost = 0.0
    total_value = 0.0
    
    for metal, data in portfolio.items():
        current_val = float(data['weight']) * float(prices[metal])
        cost_val = float(data['cost'])
        profit_val = current_val - cost_val
        
        data['current_value'] = current_val
        data['profit_loss'] = profit_val
        data['profit_loss_pct'] = (profit_val / cost_val * 100.0) if cost_val > 0 else 0.0
        
        total_cost += cost_val
        total_value += current_val
    
    total_profit_loss = total_value - total_cost
    total_profit_loss_pct = (total_profit_loss / total_cost * 100.0) if total_cost > 0 else 0.0
    
    return render_template('index.html', 
                         purchases=purchases,
                         portfolio=portfolio,
                         prices=prices,
                         total_cost=total_cost,
                         total_value=total_value,
                         total_profit_loss=total_profit_loss,
                         total_profit_loss_pct=total_profit_loss_pct)

@app.route('/add', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        metal_type = request.form['metal_type']
        weight_oz = float(request.form['weight_oz'])
        price_paid = float(request.form['price_paid'])
        purchase_date = request.form['purchase_date']
        notes = request.form.get('notes', '')
        
        conn = get_db()
        conn.execute('''
            INSERT INTO purchases (metal_type, weight_oz, price_paid, purchase_date, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (metal_type, weight_oz, price_paid, purchase_date, notes))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_purchase.html')

@app.route('/delete/<int:id>')
def delete_purchase(id):
    conn = get_db()
    conn.execute('DELETE FROM purchases WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/prices')
def api_prices():
    prices = get_live_prices()
    return jsonify(prices)

@app.route('/api/historical/<metal>')
def api_historical(metal):
    """API endpoint for historical price data"""
    current_prices = get_live_prices()
    base_price = current_prices.get(metal, 100)
    
    # fake data since theres no historical data from metalpriceapi
    data = []
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        # +-5%
        import random
        price = base_price * (1 + random.uniform(-0.05, 0.05))
        data.append({'date': date, 'price': round(price, 2)})
    
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("Starting Precious Metals Tracker")
    print("="*50)
    
    if os.getenv('SECRET_KEY'):
        print("SECRET_KEY loaded from .env")
    else:
        print("SECRET_KEY not found - using development fallback")
    
    if os.getenv('METAL_PRICE_API_KEY'):
        print("METAL_PRICE_API_KEY loaded from .env")
    else:
        print("METAL_PRICE_API_KEY not found - using mock price data")
    
    print("="*50)
    print("📊 Server running at: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)