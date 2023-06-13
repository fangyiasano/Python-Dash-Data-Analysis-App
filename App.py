import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from main import (
    retail_sales_df, Monthly_sales_df,
    store_sales_df, dept_df, weekly_sales_df
)
from dash import Dash, html, Input, Output, dcc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.Navbar(
    id='navbar',
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarBrand('Retail Sales Dashboard',
                                    style={
                                        'color': 'white',
                                        'fontSize': '25px',
                                        'fontFamily': 'Times New Roman'
                                    },
                                    )
                )
            ],
            align="center"
        ),
    ],
    color='#090059'
)

card_content_dropdwn = [
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H6('Current Period'),
                            dcc.Dropdown(
                                id='dropdown_base',
                                options=[{'label': i, 'value': i}
                                         for i in retail_sales_df['Month'].unique()],
                                value='Feb',
                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H6('Reference Period'),
                            dcc.Dropdown(
                                id='dropdown_comp',
                                options=[{'label': i, 'value': i}
                                         for i in retail_sales_df['Month'].unique()],
                                value='Jan',
                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H6('The number of store'),
                            dcc.Dropdown(
                                id='store',
                                options=[{'label': i, 'value': i}
                                         for i in retail_sales_df['Store'].unique()],
                                value=1,
                            )
                        ]
                    ),
                ]
            )
        ]
    )
]

body_app = dbc.Container(
    [
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([dbc.Card(card_content_dropdwn, style={'height': '150px'})], width=4),
                dbc.Col([dbc.Card(id='card_num1', style={'height': '150px'})]),
                dbc.Col([dbc.Card(id='card_num2', style={'height': '150px'})]),
                dbc.Col([dbc.Card(id='card_num3', style={'height': '150px'})]),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([dbc.Card(id='card_num4', style={'height': '350px'})]),
                dbc.Col([dbc.Card(id='card_num5', style={'height': '350px'})]),
                dbc.Col([dbc.Card(id='card_num6', style={'height': '350px'})]),
            ]
        ),
        html.Br(),
        html.Br()
    ],
    style={'backgroundColor': '#f7f7f7'},
    fluid=True
)

app.layout = html.Div(id='parent', children=[navbar, body_app])


@app.callback(
    [
        Output('card_num1', 'children'),
        Output('card_num2', 'children'),
        Output('card_num3', 'children'),
        Output('card_num4', 'children'),
        Output('card_num5', 'children'),
        Output('card_num6', 'children'),
    ],
    [
        Input('dropdown_base', 'value'),
        Input('dropdown_comp', 'value'),
        Input('store', 'value')
    ]
)

def update_cards(base, comparison, store):

    sales_base = store_sales_df.loc[(store_sales_df['Month'] == base) & (store_sales_df['Store'] == store)].reset_index()['Monthly_Sales'][0]
    sales_comp = store_sales_df.loc[(store_sales_df['Month'] == comparison) & (store_sales_df['Store'] == store)].reset_index()['Monthly_Sales'][0]

    diff_1 = np.round(sales_base - sales_comp, 1)

    holi_base = Monthly_sales_df.loc[(Monthly_sales_df['Month'] == base) & (Monthly_sales_df['Store'] == store)].reset_index()['Holiday_Sales_Monthly'][0]
    holi_comp = Monthly_sales_df.loc[(Monthly_sales_df['Month'] == comparison) & (Monthly_sales_df['Store'] == store)].reset_index()['Holiday_Sales_Monthly'][0]

    diff_holi = np.round(holi_base - holi_comp, 1)

    base_d_ct = retail_sales_df["Dept"].loc[(retail_sales_df['Month'] == base) & (retail_sales_df['Store'] == store)].drop_duplicates().count()
    comp_d_ct = retail_sales_df["Dept"].loc[(retail_sales_df['Month'] == comparison) & (retail_sales_df['Store'] == store)].drop_duplicates().count()

    diff_store = np.round(base_d_ct - comp_d_ct, 1)

    weekly_base = weekly_sales_df.loc[(weekly_sales_df['Month'] == base) & (weekly_sales_df['Store'] == store)].reset_index()
    weekly_comp = weekly_sales_df.loc[(weekly_sales_df['Month'] == comparison) & (weekly_sales_df['Store'] == store)].reset_index()

    dept_base = dept_df.loc[(dept_df['Month'] == base) & (dept_df['Store'] == store)].sort_values('Weekly_Sales', ascending=False).reset_index()[:10]
    dept_comp = dept_df.loc[(dept_df['Month'] == comparison) & (dept_df['Store'] == store)].sort_values('Weekly_Sales', ascending=False).reset_index()[:10]

    dept_base_1 = dept_df.loc[(dept_df['Month'] == base) & (dept_df['Store'] == store)].sort_values('Weekly_Sales', ascending=False).reset_index()[:10]
    dept_base_1 = dept_base_1.rename(columns={'Weekly_Sales': 'Weekly_Sales_base'})
    dept_comp_1 = dept_df.loc[(dept_df['Month'] == comparison) & (dept_df['Store'] == store)].sort_values('Weekly_Sales', ascending=False).reset_index()
    dept_comp_1 = dept_comp_1.rename(columns={'Weekly_Sales': 'Weekly_Sales_comp'})

    merged_df = pd.merge(dept_base_1, dept_comp_1, on='Dept', how='left')
    merged_df['diff'] = merged_df['Weekly_Sales_base'] - merged_df['Weekly_Sales_comp']

    fig = go.Figure(data=[go.Scatter(x=weekly_base['week_no'], y=weekly_base['Weekly_Sales'],
                                     line=dict(color='firebrick', width=4), name='{}'.format(base)),
                          go.Scatter(x=weekly_comp['week_no'], y=weekly_comp['Weekly_Sales'],
                                     line=dict(color='#090059', width=4), name='{}'.format(comparison))])

    fig.update_layout(plot_bgcolor='white',
                      margin=dict(l=40, r=5, t=60, b=40),
                      yaxis_tickprefix='$',
                      yaxis_ticksuffix='M',
                      )

    fig2 = go.Figure([go.Bar(x=dept_base['Weekly_Sales'],
                             y=dept_base['Dept'],
                             name='{}'.format(base),
                             text=dept_base['Weekly_Sales'], orientation='h',
                             textposition='outside',
                             ),
                      ])

    fig3 = go.Figure([go.Bar(x=dept_comp['Weekly_Sales'],
                             y=dept_comp['Dept'],
                             name='{}'.format(comparison),
                             text=dept_comp['Weekly_Sales'], orientation='h',
                             textposition='outside'
                             ),
                      ])

    fig2.update_layout(plot_bgcolor='white',
                       xaxis=dict(range=[0, '{}'.format(dept_base['Weekly_Sales'].max() + 3)]),
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M',
                       title='{}'.format(base),
                       title_x=0.5,
                     )

    fig3.update_layout(plot_bgcolor='white',
                       xaxis=dict(range=[0, '{}'.format(dept_comp['Weekly_Sales'].max() + 3)]),
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M',
                       title='{}'.format(comparison),
                       title_x=0.5,
                       )


    fig4 = go.Figure([go.Bar(x=merged_df['diff'],
                             y=merged_df['Dept'],
                             orientation='h',
                             textposition='outside'
                             ),
                      ])

    fig4.update_layout(plot_bgcolor='white',
                       margin=dict(l=40, r=5, t=60, b=40),
                       xaxis_tickprefix='$',
                       xaxis_ticksuffix='M')

    if diff_1 >= 0:
        a = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>+{0}{1}{2}</sub>".format('$', diff_1, 'M')],
                         style={'textAlign': 'center'})
    elif diff_1 < 0:
        a = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>-{0}{1}{2}</sub>".format('$', np.abs(diff_1), 'M')],
                         style={'textAlign': 'center'})
    if diff_holi >= 0:
        b = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>+{0}{1}{2}</sub>".format('$', diff_holi, 'M')],
                         style={'textAlign': 'center'})
    elif diff_holi < 0:
        b = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>-{0}{1}{2}</sub>".format('$', np.abs(diff_holi), 'M')],
                         style={'textAlign': 'center'})
    if diff_store >= 0:
        c = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>+{0}</sub>".format(diff_store)],
                         style={'textAlign': 'center'})
    elif diff_store < 0:
        c = dcc.Markdown(dangerously_allow_html=True,
                         children=["<sub>-{0}</sub>".format(np.abs(diff_store))],
                         style={'textAlign': 'center'})

    card_content = [
        dbc.CardBody(
            [
                html.H6('Monthly Sales in Total', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                html.H3('{0}{1}{2}'.format("$", sales_base, "M"), style={'color': '#090059', 'textAlign': 'center'}),
                a
            ]
        )
    ]

    card_content1 = [
        dbc.CardBody(
            [
                html.H6('Holiday Sales', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                html.H3('{0}{1}{2}'.format("$", holi_base, "M"), style={'color': '#090059', 'textAlign': 'center'}),
                b
            ]
        )
    ]

    card_content2 = [
        dbc.CardBody(
            [
                html.H6('All Departments', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
                html.H3('{0}'.format(base_d_ct), style={'color': '#090059', 'textAlign': 'center'}),
                c
            ]
        )
    ]

    card_content3 = [
        dbc.CardBody(
            [
                html.H6('Weekly Sales Comparison', style={'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Graph(figure=fig, style={'height': '250px'})
            ]
        )
    ]

    card_content4 = [
        dbc.CardBody(
            [
                html.H6('Departments with highest Sales', style={'fontWeight': 'bold', 'textAlign': 'center'}),
                dbc.Row([
                    dbc.Col([dcc.Graph(figure=fig2, style={'height': '300px'}), ]),
                    dbc.Col([dcc.Graph(figure=fig3, style={'height': '300px'}), ])

                ])
            ]
        )
    ]

    card_content5 = [
        dbc.CardBody(
            [
                html.H6('Sales difference between Top departments ({} - {})'.format(base, comparison),
                        style={'fontWeight': 'bold', 'textAlign': 'center'}),
                dcc.Graph(figure=fig4, style={'height': '300px'})
            ]
        )
    ]

    return card_content, card_content1, card_content2, card_content3, card_content4, card_content5


if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)

