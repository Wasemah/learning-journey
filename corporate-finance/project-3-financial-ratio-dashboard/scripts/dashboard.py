import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import numpy as np
from financial_analysis import FinancialAnalyzer

# Initialize the app
app = dash.Dash(__name__)
app.title = "Financial Ratio Dashboard"

# Load data
analyzer = FinancialAnalyzer('data/financial_statements.csv', 'data/industry_benchmarks.json')
dashboard_data = analyzer.generate_dashboard_data()

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("📊 Financial Ratio Dashboard", 
                style={'textAlign': 'center', 'color': '#1E3A8A', 'marginBottom': 30}),
        
        # Company Selection
        html.Div([
            html.Label("Select Company:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='company-selector',
                options=[
                    {'label': 'TechCorp Inc (Technology)', 'value': 1},
                    {'label': 'Global Retail Co (Retail)', 'value': 2},
                    {'label': 'ManufacturePro (Manufacturing)', 'value': 3}
                ],
                value=1,
                style={'width': '300px', 'marginBottom': 20}
            )
        ], style={'marginBottom': 30}),
        
        # Financial Health Score
        html.Div(id='health-score', style={
            'padding': '20px', 
            'backgroundColor': '#f8f9fa', 
            'borderRadius': '10px',
            'marginBottom': 30
        }),
    ]),
    
    # Tabs for different analysis sections
    dcc.Tabs(id='analysis-tabs', value='profitability', children=[
        dcc.Tab(label='💰 Profitability', value='profitability'),
        dcc.Tab(label='💧 Liquidity', value='liquidity'),
        dcc.Tab(label='⚖️ Leverage', value='leverage'),
        dcc.Tab(label='🔧 Efficiency', value='efficiency'),
        dcc.Tab(label='📈 Valuation', value='valuation'),
        dcc.Tab(label='📋 Comparison', value='comparison'),
    ]),
    
    html.Div(id='tab-content', style={'marginTop': 20})
])

# Health Score Callback
@app.callback(
    Output('health-score', 'children'),
    Input('company-selector', 'value')
)
def update_health_score(company_id):
    company_data = dashboard_data[company_id]
    health = company_data['financial_health']
    
    # Determine color based on score
    if health['score'] >= 80:
        color = '#28A745'
    elif health['score'] >= 60:
        color = '#FFC107'
    else:
        color = '#DC3545'
    
    return [
        html.H3(f"Financial Health: {health['rating']}"),
        html.Div([
            html.Div(style={
                'width': f'{health["score"]}%',
                'height': '20px',
                'backgroundColor': color,
                'borderRadius': '10px'
            })
        ], style={
            'width': '100%',
            'backgroundColor': '#e9ecef',
            'borderRadius': '10px',
            'overflow': 'hidden'
        }),
        html.P(f"Score: {health['score']:.1f}%", style={'marginTop': '10px', 'marginBottom': '5px'}),
        html.Ul([html.Li(insight) for insight in health['insights']])
    ]

# Tab Content Callback
@app.callback(
    Output('tab-content', 'children'),
    [Input('analysis-tabs', 'value'),
     Input('company-selector', 'value')]
)
def render_tab_content(tab, company_id):
    company_data = dashboard_data[company_id]
    ratios = company_data['ratios']
    comparison = company_data['benchmark_comparison']
    
    if tab == 'profitability':
        return render_profitability_tab(ratios, comparison)
    elif tab == 'liquidity':
        return render_liquidity_tab(ratios, comparison)
    elif tab == 'leverage':
        return render_leverage_tab(ratios, comparison)
    elif tab == 'efficiency':
        return render_efficiency_tab(ratios, comparison)
    elif tab == 'valuation':
        return render_valuation_tab(ratios, comparison)
    elif tab == 'comparison':
        return render_comparison_tab()

def render_profitability_tab(ratios, comparison):
    profit_data = ratios['profitability']
    comp_data = comparison['profitability']
    
    # Create bar chart
    metrics = list(profit_data.keys())
    company_values = list(profit_data.values())
    benchmark_values = [comp_data[metric]['benchmark_value'] for metric in metrics]
    
    fig = go.Figure(data=[
        go.Bar(name='Company', x=metrics, y=company_values, marker_color='#1F77B4'),
        go.Bar(name='Industry Benchmark', x=metrics, y=benchmark_values, marker_color='#FF7F0E')
    ])
    
    fig.update_layout(
        title='Profitability Ratios vs Industry Benchmarks',
        barmode='group',
        yaxis_title='Ratio Value'
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.H4("Profitability Analysis"),
        html.Table([
            html.Thead(html.Tr([
                html.Th('Ratio'), html.Th('Company'), html.Th('Benchmark'), 
                html.Th('Difference'), html.Th('Status')
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(metric.replace('_', ' ').title()),
                    html.Td(f"{profit_data[metric]:.3f}"),
                    html.Td(f"{comp_data[metric]['benchmark_value']:.3f}"),
                    html.Td(f"{comp_data[metric]['difference']:+.3f}"),
                    html.Td(comp_data[metric]['status'], style={
                        'color': 'green' if comp_data[metric]['status'] == 'Above' else 'red'
                    })
                ]) for metric in metrics
            ])
        ], style={'width': '100%', 'marginTop': 20})
    ])

def render_liquidity_tab(ratios, comparison):
    liquidity_data = ratios['liquidity']
    
    fig = px.bar(
        x=list(liquidity_data.keys()),
        y=list(liquidity_data.values()),
        title='Liquidity Ratios',
        labels={'x': 'Ratio', 'y': 'Value'},
        color=list(liquidity_data.values()),
        color_continuous_scale='Blues'
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.H4("Liquidity Position"),
        html.P("""
        Liquidity ratios measure a company's ability to pay off its short-term obligations. 
        Higher ratios generally indicate better short-term financial health.
        """)
    ])

def render_leverage_tab(ratios, comparison):
    leverage_data = ratios['leverage']
    
    fig = go.Figure(data=[
        go.Bar(x=list(leverage_data.keys()), y=list(leverage_data.values()))
    ])
    fig.update_layout(title='Leverage Ratios')
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.H4("Leverage Analysis"),
        html.P("""
        Leverage ratios indicate the extent to which a company is financing its operations 
        through debt versus equity. Moderate levels are generally preferred.
        """)
    ])

def render_efficiency_tab(ratios, comparison):
    efficiency_data = ratios['efficiency']
    
    fig = px.line(
        x=list(efficiency_data.keys()),
        y=list(efficiency_data.values()),
        title='Efficiency Ratios',
        markers=True
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.H4("Operational Efficiency"),
        html.P("""
        Efficiency ratios measure how well a company utilizes its assets and manages its operations 
        to generate revenue and profits.
        """)
    ])

def render_valuation_tab(ratios, comparison):
    valuation_data = ratios['valuation']
    
    fig = px.pie(
        values=list(valuation_data.values()),
        names=list(valuation_data.keys()),
        title='Valuation Ratios Distribution'
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.H4("Market Valuation"),
        html.P("""
        Valuation ratios help investors determine whether a company's stock is overvalued, 
        undervalued, or fairly priced relative to its financial performance.
        """)
    ])

def render_comparison_tab():
    # Load all companies data for comparison
    companies_data = []
    for company_id in [1, 2, 3]:
        analyzer.analyze_company(company_id)
        company_data = analyzer.analysis_results[company_id]
        companies_data.append({
            'name': company_data['company_name'],
            'industry': company_data['industry'],
            'health_score': company_data['financial_health']['score'],
            'net_margin': company_data['ratios']['profitability']['net_margin'],
            'current_ratio': company_data['ratios']['liquidity']['current_ratio'],
            'debt_to_equity': company_data['ratios']['leverage']['debt_to_equity'],
            'roa': company_data['ratios']['profitability']['roa']
        })
    
    df = pd.DataFrame(companies_data)
    
    # Create comparison chart
    fig = px.scatter(
        df, x='debt_to_equity', y='roa', size='health_score', color='industry',
        hover_data=['name'], title='ROA vs Debt-to-Equity by Company'
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.H4("Multi-Company Comparison"),
        html.Table([
            html.Thead(html.Tr([
                html.Th('Company'), html.Th('Industry'), html.Th('Health Score'),
                html.Th('Net Margin'), html.Th('Current Ratio'), html.Th('ROA')
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(comp['name']), html.Td(comp['industry']),
                    html.Td(f"{comp['health_score']:.1f}%"),
                    html.Td(f"{comp['net_margin']:.3f}"),
                    html.Td(f"{comp['current_ratio']:.2f}"),
                    html.Td(f"{comp['roa']:.3f}")
                ]) for comp in companies_data
            ])
        ], style={'width': '100%', 'marginTop': 20})
    ])

if __name__ == '__main__':
    print("🚀 Starting Financial Ratio Dashboard...")
    print("📊 Access the dashboard at: http://127.0.0.1:8050/")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
