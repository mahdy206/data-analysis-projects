import sys
print(sys.executable)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import warnings
warnings.filterwarnings("ignore")

# 1. DATA LOADING & PREPROCESSING

df = pd.read_csv(r'C:\Users\Mohamed\Desktop\dv1\e-commerce\files\cleaned_data.csv', encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"]  = pd.to_datetime(df["Ship Date"])
df["Year"]       = df["Order Date"].dt.year
df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
df["Quarter"]    = df["Order Date"].dt.to_period("Q").astype(str)
df["Profit Margin"] = df["Profit"] / df["Sales"]

ALL_YEARS      = sorted(df["Year"].unique())
ALL_CATEGORIES = sorted(df["Category"].unique())
ALL_REGIONS    = sorted(df["Region"].unique())
ALL_SEGMENTS   = sorted(df["Segment"].unique())

CATEGORY_OPTIONS = [{"label": c, "value": c} for c in ALL_CATEGORIES]
REGION_OPTIONS   = [{"label": r, "value": r} for r in ALL_REGIONS]
SEGMENT_OPTIONS  = [{"label": s, "value": s} for s in ALL_SEGMENTS]
YEAR_OPTIONS     = [{"label": str(y), "value": y} for y in ALL_YEARS]

PM_MIN = round(float(df["Profit Margin"].min()), 2)
PM_MAX = round(float(df["Profit Margin"].max()), 2)

# 2. COLOUR PALETTE — LIGHT THEME

COLORS = {
    "bg":       "#F5F7FA",
    "card":     "#FFFFFF",
    "border":   "#DDE3EC",
    "accent1":  "#3B82F6",
    "accent2":  "#F59E0B",
    "accent3":  "#10B981",
    "accent4":  "#EF4444",
    "text":     "#1E293B",
    "subtext":  "#64748B",
}

CHART_PALETTE = [
    "#93C5FD",
    "#FCD34D",
    "#6EE7B7",
    "#FCA5A5",
    "#C4B5FD",
    "#FDE68A",
    "#99F6E4",
    "#FDBA74",
]

LAYOUT_DEFAULTS = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F8FAFC",
    font=dict(family="'DM Sans', sans-serif", color=COLORS["text"]),
    margin=dict(l=50, r=30, t=55, b=50),
)

AXIS_DEFAULTS = dict(
    showgrid=True,
    gridcolor="#E2E8F0",
    gridwidth=0.5,
    zeroline=False,
    linecolor=COLORS["border"],
    tickfont=dict(size=11, color=COLORS["subtext"]),
    title_font=dict(size=12, color=COLORS["text"]),
)

def make_legend(title_text):
    return dict(
        title=dict(text=f"<b>{title_text}</b>", font=dict(size=12, color=COLORS["text"])),
        bgcolor="#FFFFFF",
        bordercolor=COLORS["border"],
        borderwidth=1,
        font=dict(size=11, color=COLORS["text"]),
        itemsizing="constant",
        tracegroupgap=4,
    )


def card(children, style=None):
    base = {
        "background": COLORS["card"],
        "border": f"1px solid {COLORS['border']}",
        "borderRadius": "12px",
        "padding": "20px",
        "marginBottom": "20px",
        "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
    }
    if style:
        base.update(style)
    return html.Div(children, style=base)


def section_title(text):
    return html.H3(
        text,
        style={
            "color": COLORS["accent1"],
            "fontFamily": "'DM Sans', sans-serif",
            "fontSize": "13px",
            "fontWeight": "700",
            "letterSpacing": "2px",
            "textTransform": "uppercase",
            "marginBottom": "16px",
            "marginTop": "0",
        },
    )


def chart_title(text):
    return html.P(
        text,
        style={
            "color": COLORS["text"],
            "fontFamily": "'DM Serif Display', serif",
            "fontSize": "15px",
            "fontWeight": "400",
            "margin": "0 0 4px 0",
        },
    )


# 3. APP INITIALISATION

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Superstore Sales Dashboard"

# 4. LAYOUT

app.layout = html.Div(
    style={"backgroundColor": COLORS["bg"], "minHeight": "100vh", "fontFamily": "'DM Sans', sans-serif"},
    children=[
        html.Link(
            href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=DM+Serif+Display&display=swap",
            rel="stylesheet",
        ),

        #Header
        html.Div(
            style={
                "background": "#FFFFFF",
                "borderBottom": f"1px solid {COLORS['border']}",
                "padding": "28px 40px 20px",
                "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
            },
            children=[
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "14px"},
                    children=[
                        html.Div("📦", style={"fontSize": "32px", "lineHeight": "1"}),
                        html.Div([
                            html.H1(
                                "Superstore Sales Performance Dashboard",
                                style={
                                    "color": COLORS["text"],
                                    "fontFamily": "'DM Serif Display', serif",
                                    "fontSize": "26px",
                                    "fontWeight": "400",
                                    "margin": "0",
                                },
                            ),
                            html.P(
                                "E-Commerce Analytics · Regions · Categories · Trends",
                                style={"color": COLORS["subtext"], "fontSize": "13px", "margin": "4px 0 0"},
                            ),
                        ]),
                    ],
                ),
            ],
        ),

        #Main Content
        html.Div(
            style={"padding": "24px 40px", "maxWidth": "1600px", "margin": "0 auto"},
            children=[

                #GLOBAL FILTERS
                card(
                    [
                        section_title("🎛  Global Filters"),
                        html.Div(
                            style={"display": "flex", "flexWrap": "wrap", "gap": "24px", "marginBottom": "20px"},
                            children=[
                                html.Div([
                                    html.Label("Year", style={"color": COLORS["subtext"], "fontSize": "12px", "display": "block", "marginBottom": "6px"}),
                                    dcc.Dropdown(
                                        id="filter-year",
                                        options=[{"label": "All Years", "value": "All"}] + YEAR_OPTIONS,
                                        value="All",
                                        clearable=False,
                                        style={"width": "160px", "backgroundColor": COLORS["bg"]},
                                    ),
                                ]),
                                html.Div([
                                    html.Label("Category", style={"color": COLORS["subtext"], "fontSize": "12px", "display": "block", "marginBottom": "6px"}),
                                    dcc.Dropdown(
                                        id="filter-category",
                                        options=[{"label": "All Categories", "value": "All"}] + CATEGORY_OPTIONS,
                                        value="All",
                                        clearable=False,
                                        style={"width": "200px"},
                                    ),
                                ]),
                                html.Div([
                                    html.Label("Region", style={"color": COLORS["subtext"], "fontSize": "12px", "display": "block", "marginBottom": "6px"}),
                                    dcc.Dropdown(
                                        id="filter-region",
                                        options=[{"label": "All Regions", "value": "All"}] + REGION_OPTIONS,
                                        value="All",
                                        clearable=False,
                                        style={"width": "180px"},
                                    ),
                                ]),
                                html.Div([
                                    html.Label("Segment", style={"color": COLORS["subtext"], "fontSize": "12px", "display": "block", "marginBottom": "6px"}),
                                    dcc.RadioItems(
                                        id="filter-segment",
                                        options=[{"label": " All", "value": "All"}] + [{"label": f" {s}", "value": s} for s in ALL_SEGMENTS],
                                        value="All",
                                        inline=True,
                                        style={"color": COLORS["text"], "fontSize": "13px", "gap": "12px"},
                                    ),
                                ]),
                            ],
                        ),

                        html.Div([
                            html.Div(
                                style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                children=[
                                    html.Label(
                                        "Profit Margin Range",
                                        style={"color": COLORS["subtext"], "fontSize": "12px"},
                                    ),
                                    html.Span(
                                        id="pm-range-label",
                                        style={
                                            "color": COLORS["accent1"],
                                            "fontSize": "12px",
                                            "fontWeight": "600",
                                            "background": "#EFF6FF",
                                            "padding": "2px 10px",
                                            "borderRadius": "20px",
                                            "border": f"1px solid #BFDBFE",
                                        },
                                    ),
                                ],
                            ),
                            dcc.RangeSlider(
                                id="filter-profit-margin",
                                min=PM_MIN,
                                max=PM_MAX,
                                step=0.01,
                                value=[PM_MIN, PM_MAX],
                                marks={
                                    PM_MIN: {"label": f"{PM_MIN:.0%}", "style": {"color": COLORS["accent4"], "fontSize": "11px"}},
                                    0:      {"label": "0%",            "style": {"color": COLORS["subtext"], "fontSize": "11px"}},
                                    0.25:   {"label": "25%",           "style": {"color": COLORS["subtext"], "fontSize": "11px"}},
                                    0.50:   {"label": "50%",           "style": {"color": COLORS["subtext"], "fontSize": "11px"}},
                                    PM_MAX: {"label": f"{PM_MAX:.0%}", "style": {"color": COLORS["accent3"], "fontSize": "11px"}},
                                },
                                tooltip={"placement": "bottom", "always_visible": False},
                                allowCross=False,
                            ),
                        ], style={"marginTop": "4px"}),
                    ],
                    style={"marginBottom": "28px"},
                ),

                #KPI CARDS
                html.Div(
                    id="kpi-row",
                    style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "16px", "marginBottom": "28px"},
                ),

                # SECTION 1 — COMPARISON CHARTS — Weeks 1 & 2
                section_title("📊  Comparison Charts"),

                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "20px"},
                    children=[
                        card([
                            chart_title("Sales by Category"),
                            html.P("Column chart comparing total sales per product category", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-column", config={"displayModeBar": False}),
                        ]),
                        card([
                            chart_title("Profit by Sub-Category"),
                            html.P("Horizontal bar chart ranking sub-categories by profit", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-bar", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "28px"},
                    children=[
                        card([
                            chart_title("Sales by Region & Category (Stacked Column)"),
                            html.P("Stacked column showing category contribution per region", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-stacked-col", config={"displayModeBar": False}),
                        ]),
                        card([
                            chart_title("Profit by Segment & Category (Stacked Bar)"),
                            html.P("Stacked bar comparing profit breakdown by customer segment", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-stacked-bar", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "28px"},
                    children=[
                        card([
                            chart_title("Sales vs Profit by Category & Ship Mode (Clustered Column)"),
                            html.P("Clustered column comparing sales and profit per shipping mode", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-clustered-col", config={"displayModeBar": False}),
                        ]),
                        card([
                            chart_title("Sales vs Profit by Region (Clustered Bar)"),
                            html.P("Clustered bar contrasting sales and profit across regions", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-clustered-bar", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                # SECTION 2 — RELATIONSHIP CHARTS — Weeks 3 & 4
                section_title("🔗  Relationship Charts"),

                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "28px"},
                    children=[
                        card([
                            chart_title("Sales vs Profit — Scatter Chart"),
                            html.P("Reveals the relationship between sales and profit", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-scatter", config={"displayModeBar": False}),
                        ]),
                        card([
                            chart_title("Sales vs Profit vs Quantity — Bubble Chart"),
                            html.P("Bubble size = Quantity; shows three-variable relationship", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-bubble", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                # SECTION 3 — DISTRIBUTION CHARTS
                section_title("📐  Distribution Charts"),

                card([
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "8px"},
                        children=[
                            html.Div([
                                chart_title("Sales Distribution by Category — Histogram"),
                                html.P("Which category has higher-value orders & whether sales are skewed", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0"}),
                            ]),
                            html.Div([
                                html.Label("Bin Size", style={"color": COLORS["subtext"], "fontSize": "12px", "display": "block", "marginBottom": "4px", "textAlign": "right"}),
                                dcc.Slider(
                                    id="hist-bins",
                                    min=1, max=10, step=1, value=4,
                                    marks={i: str(i) for i in [1, 3, 5, 7, 10]},
                                    tooltip={"placement": "bottom"},
                                ),
                            ], style={"width": "260px"}),
                        ],
                    ),
                    dcc.Graph(id="chart-histogram", config={"displayModeBar": False}),
                ]),

                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "28px"},
                    children=[
                        card([
                            chart_title("Profit Distribution by Discount Level — Box Chart"),
                            html.P("relation between discount level and profit", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-box", config={"displayModeBar": False}),
                        ]),
                        card([
                            chart_title("Sales Distribution by Segment — Violin Chart"),
                            html.P("Kernel density of sales values per customer segment", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                            dcc.Graph(id="chart-violin", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                # SECTION 4 — TIME-SERIES CHARTS — Weeks 8 & 9
                section_title("📈  Time-Series Charts"),

                card([
                    chart_title("Monthly Sales Trend — Line Chart"),
                    html.P("Tracks monthly revenue over time with direct category labels at line ends", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                    dcc.Graph(id="chart-line", config={"displayModeBar": False}),
                ]),

                card([
                    chart_title("Cumulative Sales & Profit Over Time — Area Chart"),
                    html.P("Stacked area showing the cumulative growth of sales and profit", style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 12px"}),
                    dcc.Graph(id="chart-area", config={"displayModeBar": False}),
                ]),

                html.Div(
                    "copy rights - Haitham ,Mahdy , Lilian , Amany X Maryim",
                    style={"color": COLORS["subtext"], "fontSize": "12px", "textAlign": "center", "padding": "20px 0 30px"},
                ),
            ],
        ),
    ],
)


# ─────────────────────────────────────────────
# 5. HELPER — FILTER DATA
# ─────────────────────────────────────────────

def filter_df(year, category, region, segment, pm_range):
    d = df.copy()
    if year != "All":
        d = d[d["Year"] == int(year)]
    if category != "All":
        d = d[d["Category"] == category]
    if region != "All":
        d = d[d["Region"] == region]
    if segment != "All":
        d = d[d["Segment"] == segment]
    pm_low, pm_high = pm_range
    d = d[(d["Profit Margin"] >= pm_low) & (d["Profit Margin"] <= pm_high)]
    return d


# ─────────────────────────────────────────────
# 6. CALLBACKS
# ─────────────────────────────────────────────

FILTER_INPUTS = [
    Input("filter-year",          "value"),
    Input("filter-category",      "value"),
    Input("filter-region",        "value"),
    Input("filter-segment",       "value"),
    Input("filter-profit-margin", "value"),
]


# ── Profit Margin label ──────────────────────────────────────────────────────
@app.callback(
    Output("pm-range-label", "children"),
    Input("filter-profit-margin", "value"),
)
def update_pm_label(pm_range):
    lo, hi = pm_range
    return f"{lo:.1%}  →  {hi:.1%}"


# ── KPI Cards ────────────────────────────────────────────────────────────────
@app.callback(Output("kpi-row", "children"), FILTER_INPUTS)
def update_kpis(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    kpis = [
        ("💰 Total Sales",     f"${d['Sales'].sum():,.0f}",    COLORS["accent1"]),
        ("📈 Total Profit",    f"${d['Profit'].sum():,.0f}",   COLORS["accent3"]),
        ("🛒 Total Orders",    f"{d['Order ID'].nunique():,}", COLORS["accent2"]),
        ("📦 Avg Order Value", f"${d['Sales'].mean():,.2f}",   COLORS["accent4"]),
    ]
    return [
        html.Div(
            style={
                "background": COLORS["card"],
                "border": f"1px solid {COLORS['border']}",
                "borderLeft": f"4px solid {color}",
                "borderRadius": "10px",
                "padding": "18px 22px",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
            },
            children=[
                html.P(label, style={"color": COLORS["subtext"], "fontSize": "12px", "margin": "0 0 6px"}),
                html.H2(value, style={"color": color, "fontFamily": "'DM Serif Display', serif", "fontSize": "26px", "margin": "0", "fontWeight": "400"}),
            ],
        )
        for label, value, color in kpis
    ]


# ── chart-column: Sales by Category ─────────────────────────────────────────
@app.callback(Output("chart-column", "figure"), FILTER_INPUTS)
def update_column(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(agg, x="Category", y="Sales", color="Category",
                 color_discrete_sequence=CHART_PALETTE,
                 labels={"Sales": "Total Sales (USD)", "Category": "Product Category"},
                 title="Total Sales by Product Category")
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Category"))
    fig.update_xaxes(**AXIS_DEFAULTS)
    fig.update_yaxes(**AXIS_DEFAULTS, tickprefix="$")
    return fig


# ── chart-bar: Profit by Sub-Category ───────────────────────────────────────
@app.callback(Output("chart-bar", "figure"), FILTER_INPUTS)
def update_bar(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby("Sub-Category", as_index=False)["Profit"].sum().sort_values("Profit")
    bar_colors = [COLORS["accent4"] if v < 0 else COLORS["accent3"] for v in agg["Profit"]]
    fig = go.Figure(go.Bar(
        x=agg["Profit"], y=agg["Sub-Category"], orientation="h",
        marker_color=bar_colors, marker_line_width=0,
        name="Profit",
    ))
    fig.add_trace(go.Bar(
        x=[None], y=[None], orientation="h",
        marker_color=COLORS["accent3"], name="Profit ≥ 0",
        showlegend=True,
    ))
    fig.add_trace(go.Bar(
        x=[None], y=[None], orientation="h",
        marker_color=COLORS["accent4"], name="Profit < 0",
        showlegend=True,
    ))
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title="Profit by Sub-Category", title_font_size=14,
        showlegend=True, legend=make_legend("Profit Sign"),
        xaxis=dict(**AXIS_DEFAULTS, title="Total Profit (USD)", tickprefix="$"),
        yaxis=dict(**AXIS_DEFAULTS, title="Sub-Category"),
    )
    return fig


# ── chart-stacked-col: Sales by Region & Category ───────────────────────────
@app.callback(Output("chart-stacked-col", "figure"), FILTER_INPUTS)
def update_stacked_col(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby(["Region", "Category"], as_index=False)["Sales"].sum()
    fig = px.bar(agg, x="Region", y="Sales", color="Category", barmode="stack",
                 color_discrete_sequence=CHART_PALETTE,
                 labels={"Sales": "Total Sales (USD)"},
                 title="Sales by Region & Category (Stacked)")
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Category"))
    fig.update_xaxes(**AXIS_DEFAULTS, title="Region")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Total Sales (USD)", tickprefix="$")
    return fig


# ── chart-stacked-bar: Profit by Segment & Category ─────────────────────────
@app.callback(Output("chart-stacked-bar", "figure"), FILTER_INPUTS)
def update_stacked_bar(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby(["Segment", "Category"], as_index=False)["Profit"].sum()
    fig = px.bar(agg, x="Profit", y="Segment", color="Category", orientation="h", barmode="stack",
                 color_discrete_sequence=CHART_PALETTE,
                 labels={"Profit": "Total Profit (USD)"},
                 title="Profit by Segment & Category (Stacked)")
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Category"))
    fig.update_xaxes(**AXIS_DEFAULTS, title="Total Profit (USD)", tickprefix="$")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Customer Segment")
    return fig


# ── chart-clustered-col: Sales vs Profit by Ship Mode & Category ─────────────
@app.callback(Output("chart-clustered-col", "figure"), FILTER_INPUTS)
def update_clustered_col(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby(["Ship Mode", "Category"], as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    agg_m = agg.melt(id_vars=["Ship Mode", "Category"],
                     value_vars=["Sales", "Profit"],
                     var_name="Metric", value_name="Value")
    fig = px.bar(agg_m, x="Ship Mode", y="Value", color="Metric",
                 facet_col="Category", barmode="group",
                 color_discrete_sequence=[COLORS["accent1"], COLORS["accent3"]],
                 labels={"Value": "USD"},
                 title="Sales vs Profit by Ship Mode & Category (Clustered)")
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Metric"))
    fig.for_each_xaxis(lambda a: a.update(**AXIS_DEFAULTS, title="Ship Mode"))
    fig.for_each_yaxis(lambda a: a.update(**AXIS_DEFAULTS, title="USD", tickprefix="$"))
    return fig


# ── chart-clustered-bar: Sales vs Profit by Region ───────────────────────────
@app.callback(Output("chart-clustered-bar", "figure"), FILTER_INPUTS)
def update_clustered_bar(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby("Region", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    agg_m = agg.melt(id_vars="Region",
                     value_vars=["Sales", "Profit"],
                     var_name="Metric", value_name="Value")
    fig = px.bar(agg_m, x="Value", y="Region", color="Metric", orientation="h", barmode="group",
                 color_discrete_sequence=[COLORS["accent1"], COLORS["accent3"]],
                 labels={"Value": "USD"},
                 title="Sales vs Profit by Region (Clustered)")
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Metric"))
    fig.update_xaxes(**AXIS_DEFAULTS, title="USD", tickprefix="$")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Region")
    return fig


# ── chart-scatter: Sales vs Profit ───────────────────────────────────────────
@app.callback(Output("chart-scatter", "figure"), FILTER_INPUTS)
def update_scatter(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    fig = px.scatter(d.sample(min(len(d), 2000), random_state=42),
                     x="Sales", y="Profit",
                     color="Category", symbol="Segment",
                     color_discrete_sequence=CHART_PALETTE, opacity=0.65,
                     hover_data=["Sub-Category", "Discount"],
                     labels={"Sales": "Order Sales (USD)", "Profit": "Order Profit (USD)"},
                     title="Sales vs Profit per Order")
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["accent4"], line_width=1, opacity=0.6)
    fig.update_traces(marker_size=5)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True,
                      legend=dict(
                          **make_legend("Category / Segment"),
                          groupclick="toggleitem",
                      ))
    fig.update_xaxes(**AXIS_DEFAULTS, title="Order Sales (USD)", tickprefix="$")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Order Profit (USD)", tickprefix="$")
    return fig


# ── chart-bubble: Sales vs Profit vs Quantity ────────────────────────────────
@app.callback(Output("chart-bubble", "figure"), FILTER_INPUTS)
def update_bubble(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby(["Sub-Category", "Category"], as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
    fig = px.scatter(agg, x="Sales", y="Profit", size="Quantity",
                     color="Category", text="Sub-Category",
                     color_discrete_sequence=CHART_PALETTE, size_max=55,
                     labels={"Sales": "Total Sales (USD)", "Profit": "Total Profit (USD)", "Quantity": "Units Sold"},
                     title="Sales vs Profit by Sub-Category (Bubble = Quantity Sold)")
    fig.update_traces(textposition="top center", textfont_size=9, marker_opacity=0.8)
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["accent4"], line_width=1, opacity=0.5)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Category"))
    fig.update_xaxes(**AXIS_DEFAULTS, title="Total Sales (USD)", tickprefix="$")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Total Profit (USD)", tickprefix="$")
    return fig


# ── chart-histogram: Sales Distribution by Category ──────────────────────────
@app.callback(Output("chart-histogram", "figure"), FILTER_INPUTS + [Input("hist-bins", "value")])
def update_histogram(year, category, region, segment, pm_range, bins):
    d = filter_df(year, category, region, segment, pm_range)
    fig = px.histogram(
        d,
        x="Sales",
        color="Category",
        nbins=bins * 20,
        barmode="overlay",
        opacity=0.65,
        color_discrete_sequence=CHART_PALETTE,
        labels={"Sales": "Order Sales (USD)", "count": "Number of Orders", "Category": "Category"},
        title="Sales Distribution by Category — Which category has higher-value orders?",
    )
    fig.update_traces(marker_line_width=0.8, marker_line_color=COLORS["bg"])
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title_font_size=14,
        bargap=0.02,
        showlegend=True,
        legend=make_legend("Category"),
    )
    fig.update_xaxes(**AXIS_DEFAULTS, title="Order Sales (USD)", tickprefix="$")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Number of Orders")
    return fig


# ── chart-box: Profit Distribution by Category ───────────────────────────────
@app.callback(Output("chart-box", "figure"), FILTER_INPUTS)
def update_box(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)

    fig = px.box(
        d,
        x="Discount Tier",
        y="Profit",
        category_orders={"Discount Tier": ["No Discount", "Low (1-20%)", "Medium (21-40%)", "High (>40%)"]},
        color="Discount Tier",
        color_discrete_sequence=CHART_PALETTE,
        points="outliers",
        labels={"Profit": "Order Profit (USD)", "Discount Tier": "Discount Level"},
        title="Profit Distribution by Discount Level<br><sup>Box Chart</sup>",
    )
    fig.update_yaxes(range=[-300, 300])  # still needs clamping, but boxes tell a clear story

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=COLORS["accent4"],
        line_width=1,
        opacity=0.5,
    )

    # ── KEY FIX: clamp y-axis so boxes are visible ──────────────────────────
    # Extreme outliers (up to ±$6 600) compress the IQR boxes to invisible lines.
    # Clamping to ±$500 keeps all three boxes clearly readable.
    fig.update_yaxes(
        **AXIS_DEFAULTS,
        title="Order Profit (USD)",
        tickprefix="$",
        range=[-500, 500],          # clamp — boxes have IQR of $17–$70, outliers reach ±$6 600
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title_font_size=14,
        showlegend=False,
        annotations=[dict(
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            font=dict(size=10, color=COLORS["subtext"]),
            align="left",
        )],
    )

    fig.update_xaxes(**AXIS_DEFAULTS, title="Discount Level")

    return fig


# ── chart-violin: Sales Distribution by Segment ──────────────────────────────
@app.callback(Output("chart-violin", "figure"), FILTER_INPUTS)
def update_violin(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    fig = px.violin(d, x="Segment", y="Sales", color="Segment",
                    box=True, points="outliers",
                    color_discrete_sequence=CHART_PALETTE,
                    labels={"Sales": "Order Sales (USD)", "Segment": "Customer Segment"},
                    title="Sales Distribution by Customer Segment")
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Segment"))
    fig.update_xaxes(**AXIS_DEFAULTS, title="Customer Segment")
    fig.update_yaxes(**AXIS_DEFAULTS, title="Order Sales (USD)", tickprefix="$")
    return fig


# ── chart-line: Monthly Sales Trend — WITH DIRECT END-OF-LINE LABELS ─────────
@app.callback(Output("chart-line", "figure"), FILTER_INPUTS)
def update_line(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    agg = d.groupby(["Month", "Category"], as_index=False)["Sales"].sum().sort_values("Month")

    fig = go.Figure()
    categories = sorted(agg["Category"].unique())

    for i, cat in enumerate(categories):
        cat_data = agg[agg["Category"] == cat].sort_values("Month")
        color = CHART_PALETTE[i % len(CHART_PALETTE)]

        fig.add_trace(go.Scatter(
            x=cat_data["Month"],
            y=cat_data["Sales"],
            mode="lines+markers",
            name=cat,
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color),
            
        ))

        # Direct label at the end of each line
        if not cat_data.empty:
            last_x = cat_data["Month"].iloc[-1]
            last_y = cat_data["Sales"].iloc[-1]
            fig.add_annotation(
                x=last_x,
                y=last_y,
                text=f"<b>{cat}</b>",
                showarrow=False,
                xanchor="left",
                xshift=10,           # nudge label 10px to the right of the last point
                font=dict(size=11, color=color, family="'DM Sans', sans-serif"),
            )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title="Monthly Sales Trend by Product Category",
        title_font_size=14,
        showlegend=True,
        #margin=dict(l=50, r=130, t=55, b=80),   wider right margin so labels aren't clipped
    )
    fig.update_xaxes(**AXIS_DEFAULTS, title="Month", tickangle=45)
    fig.update_yaxes(**AXIS_DEFAULTS, title="Monthly Sales (USD)", tickprefix="$")
    return fig


# ── chart-area: Cumulative Sales & Profit ────────────────────────────────────
@app.callback(Output("chart-area", "figure"), FILTER_INPUTS)
def update_area(year, category, region, segment, pm_range):
    d = filter_df(year, category, region, segment, pm_range)
    monthly = d.groupby("Month", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Month")
    monthly["Cumulative Sales"]  = monthly["Sales"].cumsum()
    monthly["Cumulative Profit"] = monthly["Profit"].cumsum()
    m = monthly.melt(id_vars="Month",
                     value_vars=["Cumulative Sales", "Cumulative Profit"],
                     var_name="Metric", value_name="Value")
    fig = px.area(m, x="Month", y="Value", color="Metric",
                  color_discrete_sequence=[COLORS["accent1"], COLORS["accent3"]],
                  labels={"Value": "Cumulative USD", "Month": "Month"},
                  title="Cumulative Sales & Profit Over Time")
    fig.update_traces(line_width=2)
    fig.update_layout(**LAYOUT_DEFAULTS, title_font_size=14,
                      showlegend=True, legend=make_legend("Metric"))
    fig.update_xaxes(**AXIS_DEFAULTS, title="Month", tickangle=45)
    fig.update_yaxes(**AXIS_DEFAULTS, title="Cumulative Value (USD)", tickprefix="$")
    return fig


# ─────────────────────────────────────────────
# 7. RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=8050)