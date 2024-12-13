import pandas as pd
import requests as req
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Part 1: Fetch cryptocurrency data
url = "https://api.coingecko.com/api/v3/coins/markets"
parameters = {
    "vs_currency": 'inr',
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}
response = req.get(url, params=parameters)
data = response.json()
crypto_df = pd.DataFrame(data)
crypto_df = crypto_df[["id", "symbol", "current_price", "market_cap", "total_volume", "last_updated"]]

# Part 2: Function to fetch historical price data
def fetch_historical_data(crypto_id, vs_currency='inr', days=15):
    """Fetch historical price data for a cryptocurrency."""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {'vs_currency': vs_currency, 'days': days}
    try:
        response = req.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = [entry[1] for entry in data['prices']]  # Extract closing prices
        return prices
    except req.exceptions.RequestException as e:
        print(f"Error fetching historical data for {crypto_id}: {e}")
        return []

# Part 3: Dash app setup
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Cryptocurrency Portfolio Tracker"),
    
    # Input form to enter portfolio data
    html.Div([
        html.Label("Enter your portfolio (format: 'crypto_name:quantity')"),
        dcc.Input(id='portfolio-input', type='text', placeholder="e.g. bitcoin:0.5, ethereum:2"),
        html.Button('Submit', id='submit-button', n_clicks=0),
    ]),
    
    # Display portfolio value
    html.Div(id='portfolio-value'),
    
    # Display pie chart for portfolio distribution
    dcc.Graph(id='portfolio-chart'),
    
    # Display line graph for historical price trends
    dcc.Graph(id='historical-line-graph')
])

# Part 4: Callback to update portfolio value, pie chart, and line graph
@app.callback(
    [Output('portfolio-value', 'children'),
     Output('portfolio-chart', 'figure'),
     Output('historical-line-graph', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('portfolio-input', 'value')]
)
def update_dashboard(n_clicks, portfolio_input):
    if n_clicks == 0 or not portfolio_input:
        return "", {}, {}

    # Parse user portfolio input
    try:
        user_portfolio = {}
        for entry in portfolio_input.split(","):
            crypto_name, quantity = entry.split(":")
            user_portfolio[crypto_name.strip().lower()] = float(quantity.strip())
    except ValueError:
        return "Invalid input format. Please use 'crypto_name:quantity'.", {}, {}

    # Calculate portfolio value
    total_value = 0
    portfolio_values = {}
    for crypto_name, quantity in user_portfolio.items():
        match = crypto_df[crypto_df["id"] == crypto_name]
        if not match.empty:
            current_price = match.iloc[0]['current_price']
            value = quantity * current_price
            portfolio_values[crypto_name] = value
            total_value += value

    # Create pie chart for portfolio distribution
    pie_chart = px.pie(
        names=[crypto.capitalize() for crypto in portfolio_values.keys()],
        values=portfolio_values.values(),
        title="Portfolio Distribution by Cryptocurrencies"
    )
    
    # Create line graph for historical price trends
    historical_data = {}
    for crypto_name in user_portfolio.keys():
        historical_prices = fetch_historical_data(crypto_name)
        if historical_prices:
            historical_data[crypto_name] = historical_prices

    line_graph_data = []
    for crypto_name, prices in historical_data.items():
        line_graph_data.append(
            pd.DataFrame({
                'Day': range(1, len(prices) + 1),
                'Price': prices,
                'Crypto': crypto_name.capitalize()
            })
        )

    if line_graph_data:
        line_graph_df = pd.concat(line_graph_data, ignore_index=True)
        line_graph = px.line(
            line_graph_df, x='Day', y='Price', color='Crypto',
            title="Historical Price Trends (Past 15 Days)"
        )
    else:
        line_graph = {}

    # Return portfolio summary, pie chart, and line graph
    portfolio_summary = f"Total Portfolio Value: ₹{total_value:,.2f}"
    return portfolio_summary, pie_chart, line_graph

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

