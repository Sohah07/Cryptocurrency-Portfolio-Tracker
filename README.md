# Cryptocurrency-Portfolio-Tracker
A web application built using Python and Dash to help users track their cryptocurrency portfolio in real-time. The app allows users to input their portfolio holdings, visualize their portfolio distribution, and monitor historical price trends of cryptocurrencies.

# Features
1. Cryptocurrency Data: Fetches real-time cryptocurrency prices, market caps, and volumes using the  CoinGecko API.
2. Portfolio Tracking: Users can input their cryptocurrency holdings and calculate the total portfolio value.
3. Visualization:
Pie chart for portfolio distribution.
Historical price trends (past 15 days) for cryptocurrencies.
4. Interactive Web App: Built with Dash to provide an easy-to-use interface.

# Demo

# API Used

The application uses the CoinGecko API to fetch:

Real-time cryptocurrency data (prices, market cap, and volume).
Historical price trends for cryptocurrencies (15-day intervals).

# Features in Detail

Real-Time Portfolio Tracking
Users can input their cryptocurrency holdings in the format cryptocurrency_name:quantity (e.g., bitcoin: 0.5, ethereum: 2 ).
The app calculates and displays the total portfolio value in INR (Indian Rupees).
Visualizations
Portfolio Distribution:
A pie chart representing the distribution of cryptocurrencies in the user’s portfolio.
Historical Price Trends:
Line charts showing the price trends of cryptocurrencies over the last 15 days.
Technologies Used

Frontend: Dash for the interactive web interface.
Backend: Python for data processing.
APIs: CoinGecko API for real-time cryptocurrency data.
Visualization: Plotly and Matplotlib for dynamic graphs.

# License

This project is licensed under the MIT License. See the 'LICENSE' file for details.

# Future Enhancements

Add more detailed historical price charts (e.g., 1 month, 6 months, 1 year).
Enable user authentication for personalized portfolios.
Add support for multiple currencies (USD, EUR, etc.).
Notifications for significant price changes

