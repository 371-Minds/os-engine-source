import plotly.graph_objects as go
import plotly.express as px
import json

# Parse the data
data_json = {"performance_metrics": [{"metric": "Throughput (tasks/sec)", "original": 19.8, "improved": 972.5}, {"metric": "Avg Response Time (ms)", "original": 50.5, "improved": 10.3}, {"metric": "Max Concurrent Tasks", "original": 1, "improved": 20}, {"metric": "Error Rate (%)", "original": 8.5, "improved": 0.2}, {"metric": "Memory Efficiency (MB)", "original": 45.2, "improved": 32.1}, {"metric": "Cache Hit Rate (%)", "original": 0, "improved": 78.3}]}

# Extract metrics and values
metrics = []
original_values = []
improved_values = []

for item in data_json["performance_metrics"]:
    # Abbreviate metric names to fit 15 character limit for axis labels
    metric = item["metric"]
    if "Throughput" in metric:
        metric = "Tasks/sec"
    elif "Response Time" in metric:
        metric = "Response (ms)"
    elif "Concurrent" in metric:
        metric = "Max Concurrent"
    elif "Error Rate" in metric:
        metric = "Error Rate %"
    elif "Memory" in metric:
        metric = "Memory (MB)"
    elif "Cache" in metric:
        metric = "Cache Hit %"
    
    metrics.append(metric)
    # Handle zero values for log scale by using small positive number
    original_val = item["original"] if item["original"] > 0 else 0.1
    improved_val = item["improved"] if item["improved"] > 0 else 0.1
    original_values.append(original_val)
    improved_values.append(improved_val)

# Create grouped bar chart
fig = go.Figure()

# Add bars for original version
fig.add_trace(go.Bar(
    name='Original',
    x=metrics,
    y=original_values,
    marker_color='#1FB8CD',
    cliponaxis=False
))

# Add bars for improved version
fig.add_trace(go.Bar(
    name='Improved',
    x=metrics,
    y=improved_values,
    marker_color='#DB4545',
    cliponaxis=False
))

# Update layout with log scale
fig.update_layout(
    title='BaseAgent Performance Comparison',
    xaxis_title='Metrics',
    yaxis_title='Value (log)',
    yaxis_type='log',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image("performance_comparison.png")
