# Financial Ratio Dashboard Configuration

# Analysis Settings
ANALYSIS_CONFIG = {
    'periods_to_analyze': 4,  # Number of quarters to include
    'include_annual_data': True,
    'currency': 'USD',
    'decimal_places': 3
}

# Ratio Calculation Settings
RATIO_CONFIG = {
    'profitability': {
        'gross_margin': {'min': 0, 'max': 1, 'optimal': 'higher'},
        'operating_margin': {'min': 0, 'max': 1, 'optimal': 'higher'},
        'net_margin': {'min': 0, 'max': 1, 'optimal': 'higher'},
        'roa': {'min': 0, 'max': 0.5, 'optimal': 'higher'},
        'roe': {'min': 0, 'max': 1, 'optimal': 'higher'}
    },
    'liquidity': {
        'current_ratio': {'min': 1, 'max': 3, 'optimal': 'range'},
        'quick_ratio': {'min': 0.8, 'max': 2, 'optimal': 'range'},
        'cash_ratio': {'min': 0.1, 'max': 0.8, 'optimal': 'range'}
    },
    'leverage': {
        'debt_to_equity': {'min': 0, 'max': 2, 'optimal': 'lower'},
        'debt_ratio': {'min': 0, 'max': 0.8, 'optimal': 'lower'},
        'interest_coverage': {'min': 1.5, 'max': 20, 'optimal': 'higher'}
    },
    'efficiency': {
        'asset_turnover': {'min': 0.5, 'max': 2, 'optimal': 'higher'},
        'inventory_turnover': {'min': 4, 'max': 12, 'optimal': 'higher'},
        'receivables_turnover': {'min': 6, 'max': 15, 'optimal': 'higher'}
    }
}

# Dashboard Settings
DASHBOARD_CONFIG = {
    'theme': 'plotly_white',
    'colors': {
        'positive': '#2E8B57',
        'negative': '#DC143C',
        'neutral': '#4682B4',
        'warning': '#FF8C00',
        'tech': '#1F77B4',
        'retail': '#FF7F0E',
        'manufacturing': '#2CA02C'
    },
    'chart_templates': {
        'profitability': 'bar',
        'liquidity': 'line',
        'leverage': 'scatter',
        'efficiency': 'heatmap'
    }
}

# Report Settings
REPORT_CONFIG = {
    'include_executive_summary': True,
    'include_detailed_analysis': True,
    'include_recommendations': True,
    'export_formats': ['html', 'pdf', 'json'],
    'language': 'en'
}
