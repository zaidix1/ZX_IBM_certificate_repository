# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'site1'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'site2'},
                                                    {'label': 'KSC LC-39A', 'value': 'site3'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'site4'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100',
                                                       1000: '1000',
                                                       2000: '2000',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),
        
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site',
        title='Total Success Launches By All Sites')
        return fig
    # return the outcomes piechart for a selected site
    elif entered_site == 'site1':
        filtered_df1=filtered_df[['Launch Site']=='CCAFS LC-40']
        fig = px.pie(filtered_df1, values='class', 
        names='Launch Site', 
        title='Total Success Launches By CCAFS LC-40')
        return fig
    elif entered_site == 'site2':
        fig = px.pie(filtered_df[['Launch Site']=='VAFB SLC-4E'], values='class', 
        names='class', 
        title='Total Success Launches By VAFB SLC-4E')
        return fig
    elif entered_site == 'site3':
        fig = px.pie(filtered_df[['Launch Site']=='KSC LC-39A'], values='class', 
        names='class', 
        title='Total Success Launches By KSC LC-39A')
        return fig
    else:
        fig = px.pie(filtered_df[['Launch Site']=='CCAFS SLC-40'], values='class', 
        names='class', 
        title='Total Success Launches By CCAFS SLC-40')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slider_range):
    low, high = slider_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if entered_site == 'ALL':
        fig = px.scatter(
        spacex_df[mask], x="Payload Mass (kg)", y="class", 
        color="Booster Version Category",
        hover_data=['Payload Mass (kg)'],
        title='Correlation between Payload and Success for all Sites')
        return fig
    elif entered_site == 'site1':
        mask1 = (spacex_df['Launch Site'] == 'CCAFS LC-40') & (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
        spacex_df[mask1], x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        hover_data=['Payload Mass (kg)'],
        title='Correlation between Payload and Success for CCAFS LC-40')
        return fig
    elif entered_site == 'site2':
        mask1 = (spacex_df['Launch Site'] == 'VAFB SLC-4E') & (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
        spacex_df[mask1], x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        hover_data=['Payload Mass (kg)'],
        title='Correlation between Payload and Success for VAFB SLC-4E')
        return fig
    elif entered_site == 'site3':
        mask1 = (spacex_df['Launch Site'] == 'KSC LC-39A') & (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
        spacex_df[mask1], x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        hover_data=['Payload Mass (kg)'],
        title='Correlation between Payload and Success for KSC LC-39A')
        return fig
    else:
        mask1 = (spacex_df['Launch Site'] == 'CCAFS SLC-40') & (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
        spacex_df[mask1], x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        hover_data=['Payload Mass (kg)'],
        title='Correlation between Payload and Success for CCAFS SLC-40')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
