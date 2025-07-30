import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import math
import json

# Parse the data
data = {
    "components": [
        {"name": "Content Generation Engine", "type": "core", "subcomponents": ["AI Content Creator", "Template Engine", "Brand Voice Manager", "Content Optimizer"]},
        {"name": "Email Marketing System", "type": "core", "subcomponents": ["Campaign Builder", "Segmentation Engine", "A/B Testing", "Delivery System"]},
        {"name": "Social Media System", "type": "core", "subcomponents": ["Post Scheduler", "Multi-Platform Publisher", "Engagement Monitor", "Content Formatter"]},
        {"name": "Content Strategy System", "type": "core", "subcomponents": ["Content Calendar", "Topic Research", "Performance Predictor", "Trend Analyzer"]},
        {"name": "Analytics System", "type": "core", "subcomponents": ["Performance Tracker", "ROI Calculator", "Audience Insights", "Conversion Analytics"]},
        {"name": "Intelligent Router", "type": "orchestration", "subcomponents": ["Task Analyzer", "System Dispatcher", "Workflow Coordinator"]},
        {"name": "Credential Warehouse", "type": "security", "subcomponents": ["API Keys", "OAuth Tokens", "Platform Credentials"]},
        {"name": "Human Checkpoints", "type": "oversight", "subcomponents": ["Content Approval", "Brand Review", "Campaign Validation"]}
    ],
    "integrations": [
        {"from": "Content Generation Engine", "to": "Email Marketing System", "type": "data"},
        {"from": "Content Generation Engine", "to": "Social Media System", "type": "data"},
        {"from": "Analytics System", "to": "Content Strategy System", "type": "feedback"},
        {"from": "Intelligent Router", "to": "All Systems", "type": "orchestration"},
        {"from": "Credential Warehouse", "to": "All External APIs", "type": "authentication"}
    ]
}

# Define colors for different component types
color_map = {
    "core": "#1FB8CD",          # Strong cyan
    "orchestration": "#DB4545",  # Bright red  
    "security": "#2E8B57",      # Sea green
    "oversight": "#5D878F",     # Cyan
    "external": "#D2BA4C"       # Moderate yellow
}

# Create structured positions with better spacing
components = data["components"]
positions = {}

# Central orchestration
positions["Intelligent Router"] = (0, 0)

# Core systems in organized grid
core_components = [c for c in components if c["type"] == "core"]
core_positions = [
    (-3, 2.5),   # Content Generation Engine
    (3, 2.5),    # Email Marketing System  
    (3, -2.5),   # Social Media System
    (-3, -2.5),  # Content Strategy System
    (0, -4)      # Analytics System
]

for i, comp in enumerate(core_components):
    if i < len(core_positions):
        positions[comp["name"]] = core_positions[i]

# Security and oversight in clear positions
positions["Credential Warehouse"] = (-6, 0)
positions["Human Checkpoints"] = (6, 0)

# External systems with better spacing
external_systems = {
    "Email APIs": (6, 4),
    "Social APIs": (6, -4),
    "Analytics APIs": (-6, -4)
}

# Create the figure
fig = go.Figure()

# Add grouping rectangles for different system types
# Core systems group
fig.add_shape(
    type="rect",
    x0=-4.5, y0=-5, x1=4.5, y1=3.5,
    line=dict(color="rgba(31,184,205,0.3)", width=2, dash="dash"),
    fillcolor="rgba(31,184,205,0.05)",
    layer="below"
)

# Add group labels
fig.add_trace(go.Scatter(
    x=[-4], y=[3.2],
    mode='text',
    text="Core Systems",
    textfont=dict(size=12, color="#1FB8CD", family="Arial Bold"),
    showlegend=False,
    hoverinfo='none'
))

fig.add_trace(go.Scatter(
    x=[-6], y=[1],
    mode='text',
    text="Security",
    textfont=dict(size=12, color="#2E8B57", family="Arial Bold"),
    showlegend=False,
    hoverinfo='none'
))

fig.add_trace(go.Scatter(
    x=[6], y=[1],
    mode='text',
    text="Oversight",
    textfont=dict(size=12, color="#5D878F", family="Arial Bold"),
    showlegend=False,
    hoverinfo='none'
))

# Add connections with clearer styles and arrows
integrations = data["integrations"]

# Direct data connections
direct_connections = [
    ("Content Generation Engine", "Email Marketing System", "data"),
    ("Content Generation Engine", "Social Media System", "data"),
    ("Analytics System", "Content Strategy System", "feedback")
]

for from_comp, to_comp, conn_type in direct_connections:
    if from_comp in positions and to_comp in positions:
        from_pos = positions[from_comp]
        to_pos = positions[to_comp]
        
        # Different colors for different connection types
        if conn_type == "data":
            color = "#13343B"
            width = 4
            dash = "solid"
        else:  # feedback
            color = "#964325"
            width = 3
            dash = "dash"
            
        fig.add_trace(go.Scatter(
            x=[from_pos[0], to_pos[0]],
            y=[from_pos[1], to_pos[1]],
            mode='lines',
            line=dict(color=color, width=width, dash=dash),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"{conn_type.title()}: {from_comp} → {to_comp}"
        ))

# Orchestration connections (hub and spoke from Intelligent Router)
router_pos = positions["Intelligent Router"]
for comp in components:
    if comp["name"] != "Intelligent Router" and comp["name"] in positions:
        to_pos = positions[comp["name"]]
        fig.add_trace(go.Scatter(
            x=[router_pos[0], to_pos[0]],
            y=[router_pos[1], to_pos[1]],
            mode='lines',
            line=dict(color="#DB4545", width=2, dash="dot"),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"Orchestration: Intelligent Router → {comp['name']}"
        ))

# Authentication connections from Credential Warehouse to externals
cred_pos = positions["Credential Warehouse"]
for ext_name, ext_pos in external_systems.items():
    fig.add_trace(go.Scatter(
        x=[cred_pos[0], ext_pos[0]],
        y=[cred_pos[1], ext_pos[1]],
        mode='lines',
        line=dict(color="#2E8B57", width=3, dash="dashdot"),
        showlegend=False,
        hoverinfo='text',
        hovertext=f"Authentication: Credential Warehouse → {ext_name}"
    ))

# Human checkpoint connections to key systems
human_pos = positions["Human Checkpoints"]
checkpoint_connections = ["Content Generation Engine", "Email Marketing System", "Social Media System"]
for comp_name in checkpoint_connections:
    if comp_name in positions:
        comp_pos = positions[comp_name]
        fig.add_trace(go.Scatter(
            x=[human_pos[0], comp_pos[0]],
            y=[human_pos[1], comp_pos[1]],
            mode='lines',
            line=dict(color="#5D878F", width=2, dash="longdash"),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"Human Review: {comp_name}"
        ))

# Add external system nodes
for ext_name, pos in external_systems.items():
    fig.add_trace(go.Scatter(
        x=[pos[0]],
        y=[pos[1]],
        mode='markers+text',
        marker=dict(
            size=30,
            color='#D2BA4C',
            line=dict(width=2, color='white'),
            symbol='square'
        ),
        text=ext_name.replace(" APIs", "<br>APIs"),
        textposition='middle center',
        textfont=dict(size=9, color='white', family="Arial Bold"),
        name="External APIs",
        showlegend=True,
        legendgroup="external",
        hoverinfo='text',
        hovertext=f"External Service: {ext_name}<br>Provides integration endpoints"
    ))

# Add component nodes with better text sizing
legend_added = set()
for comp in components:
    if comp["name"] in positions:
        pos = positions[comp["name"]]
        comp_type = comp["type"]
        color = color_map.get(comp_type, "#1FB8CD")
        
        # Create detailed hover text
        subcomp_list = "<br>".join([f"• {sc}" for sc in comp["subcomponents"]])
        hover_text = f"<b>{comp['name']}</b><br><br>Type: {comp_type.title()}<br><br>Subcomponents:<br>{subcomp_list}"
        
        # Better display names with line breaks
        display_name = comp["name"]
        if "Generation Engine" in display_name:
            display_name = "Content<br>Generation"
        elif "Marketing System" in display_name:
            display_name = "Email<br>Marketing"
        elif "Media System" in display_name:
            display_name = "Social<br>Media"
        elif "Strategy System" in display_name:
            display_name = "Content<br>Strategy"
        elif "Analytics System" in display_name:
            display_name = "Analytics<br>System"
        elif "Intelligent Router" in display_name:
            display_name = "Intelligent<br>Router"
        elif "Credential Warehouse" in display_name:
            display_name = "Credential<br>Warehouse"
        elif "Human Checkpoints" in display_name:
            display_name = "Human<br>Checkpoints"
        
        show_legend = comp_type not in legend_added
        if show_legend:
            legend_added.add(comp_type)
        
        # Size based on importance
        if comp_type == "orchestration":
            size = 55
        elif comp_type == "core":
            size = 45
        else:
            size = 40
            
        # Different shapes for different types
        symbol = 'circle'
        if comp_type == 'security':
            symbol = 'diamond'
        elif comp_type == 'oversight':
            symbol = 'hexagon'
        
        fig.add_trace(go.Scatter(
            x=[pos[0]],
            y=[pos[1]],
            mode='markers+text',
            marker=dict(
                size=size,
                color=color,
                line=dict(width=3, color='white'),
                symbol=symbol
            ),
            text=display_name,
            textposition='middle center',
            textfont=dict(size=10, color='white', family="Arial Black"),
            name=comp_type.title(),
            showlegend=show_legend,
            legendgroup=comp_type,
            hoverinfo='text',
            hovertext=hover_text,
            cliponaxis=False
        ))

# Add connection type legend with invisible traces
connection_types = [
    {"name": "Data Flow", "color": "#13343B", "dash": "solid", "width": 4},
    {"name": "Feedback", "color": "#964325", "dash": "dash", "width": 3},
    {"name": "Orchestration", "color": "#DB4545", "dash": "dot", "width": 2},
    {"name": "Authentication", "color": "#2E8B57", "dash": "dashdot", "width": 3},
    {"name": "Human Review", "color": "#5D878F", "dash": "longdash", "width": 2}
]

for conn in connection_types:
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color=conn["color"], dash=conn["dash"], width=conn["width"]),
        name=conn["name"],
        showlegend=True,
        legendgroup="connections"
    ))

# Update layout with proper spacing
fig.update_layout(
    title=dict(
        text="371 Minds Content & Marketing System",
        x=0.5,
        y=0.95,
        font=dict(size=16, family="Arial Bold")
    ),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.05,
        xanchor='center',
        x=0.5,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='rgba(0,0,0,0.3)',
        borderwidth=1,
        font=dict(size=10)
    ),
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-7.5, 7.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-5.5, 4.5]
    ),
    plot_bgcolor='rgba(248,249,250,0.5)',
    paper_bgcolor='white'
)

# Save the chart
fig.write_image("content_marketing_architecture.png", width=1400, height=1000, scale=2)