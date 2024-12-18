# -*- coding: utf-8 -*-
"""Personal Finace Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1znBIW5CQhjo8qCb7SlyyZvBkdjHPiF8J
"""

# Import necessary libraries
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

file_path = 'Daily_Household_Transactions.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.dropna(subset=['Date'])

data['Month'] = data['Date'].dt.month_name()
data['Year'] = data['Date'].dt.year

data['Amount'] = data['Amount'].abs()
data['Income'] = data.apply(lambda row: row['Amount'] if row['Income/Expense'] == 'Income' else 0, axis=1)
data['Expense'] = data.apply(lambda row: row['Amount'] if row['Income/Expense'] == 'Expense' else 0, axis=1)

monthly_summary = data.groupby([data['Date'].dt.to_period('M').astype(str)])[['Income', 'Expense']].sum().reset_index()
category_summary = data.groupby('Category')[['Expense']].sum().reset_index()
mode_summary = data.groupby('Mode')[['Expense']].sum().reset_index()

app = Dash(__name__)

# visualizations
income_expense_trend = px.line(
    monthly_summary,
    x='Date',
    y=['Income', 'Expense'],
    title='Income vs Expense Trends',
    labels={'value': 'Amount', 'Date': 'Month'}
)

category_breakdown = px.pie(
    category_summary,
    values='Expense',
    names='Category',
    title='Expense Breakdown by Category'
)

payment_mode_chart = px.bar(
    mode_summary,
    x='Mode',
    y='Expense',
    title='Expense by Payment Mode',
    labels={'Expense': 'Amount'}
)

app.layout = html.Div([
    html.H1("Personal Finance Dashboard", style={'text-align': 'center'}),

    # Income vs Expense Trends
    html.Div([
        dcc.Graph(id='income-expense-chart', figure=income_expense_trend)
    ]),

    # Category Breakdown
    html.Div([
        dcc.Graph(id='category-breakdown-chart', figure=category_breakdown)
    ]),

    # Payment Mode Chart
    html.Div([
        dcc.Graph(id='payment-mode-chart', figure=payment_mode_chart)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)