import os
import pandas as pd
from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio

app = Flask(__name__, template_folder='templates')

def load_data():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'cars.csv')
    cars_data = pd.read_csv(file_path)
    
    def clean_column(column, dtype=float, errors='coerce'):
        try:
            return pd.to_numeric(column.str.replace('SAR', '').str.replace(',', '').str.strip(), errors=errors)
        except ValueError:
            if pd.isna(column) or column.str.lower() == 'cylinders':
                return pd.Series([], dtype=dtype)  
            else:
                raise 

    cars_data['price_cleaned'] = clean_column(cars_data['price'])
    cars_data['engine_capacity_cleaned'] = clean_column(cars_data['engine_capacity'], dtype=int)
    cars_data['horse_power_cleaned'] = clean_column(cars_data['horse_power'], dtype=int)
  
    return cars_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize-price')
def visualize_price():
    cars_data = load_data()
    prices = cars_data['price_cleaned']

    if not isinstance(prices, (pd.Series, list)):
        prices = [] 

    fig = px.histogram(x=prices, nbins=50, title='Price Distribution of Cars')
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('visualize.html', graph=graph_html)

@app.route('/visualize-hp-vs-engine')
def visualize_hp_vs_engine():
    cars_data = load_data()
    engine_capacity = cars_data['engine_capacity_cleaned']
    horse_power = cars_data['horse_power_cleaned']

    fig = px.scatter(x=engine_capacity, y=horse_power,
                     title='Horsepower vs Engine Capacity',
                     labels={'x': 'Engine Capacity (L)', 'y': 'Horsepower'})
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('visualize.html', graph=graph_html)

@app.route('/visualize-electric-cars')
def visualize_electric_cars():
    cars_data = load_data()
    electric_cars = cars_data[cars_data['is_electric'] == True]
    non_electric_cars = cars_data[cars_data['is_electric'] == False]

    fig = px.scatter(x=electric_cars['horse_power_cleaned'], y=electric_cars['price_cleaned'],
                     labels={'x': 'Horsepower', 'y': 'Price'},
                     title='Electric Cars (Horsepower vs Price)')
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('visualize.html', graph=graph_html)

if __name__ == '__main__':
    app.run(debug=True)