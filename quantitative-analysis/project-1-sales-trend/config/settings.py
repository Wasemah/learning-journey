# Configuration settings for Sales Trend Analysis Project

# Data Configuration
DATA_CONFIG = {
    'data_path': 'data/sales_data.csv',
    'date_column': 'date',
    'value_columns': ['units_sold', 'revenue'],
    'category_columns': ['product', 'category', 'region']
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'time_period': 'monthly',  # daily, weekly, monthly, quarterly
    'top_n_products': 5,
    'regions': ['North', 'South', 'East', 'West'],
    'currency': 'USD'
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    'style': 'seaborn-v0_8',
    'figure_size': (12, 8),
    'colors': {
        'primary': '#2E86AB',
        'secondary': '#A23B72', 
        'tertiary': '#F18F01',
        'success': '#28A745',
        'warning': '#FFC107',
        'danger': '#DC3545'
    },
    'save_format': 'png',
    'dpi': 300
}

# Output Configuration
OUTPUT_CONFIG = {
    'results_directory': 'results',
    'reports_directory': 'reports',
    'create_timestamp_folders': True,
    'save_raw_data': False
}

# Email Report Configuration (Optional)
EMAIL_CONFIG = {
    'send_reports': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'receiver_emails': ['team@company.com']
}
