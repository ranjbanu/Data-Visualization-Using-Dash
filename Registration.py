#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


# In[2]:


registration_df= pd.read_csv("Registration_data_Plotly.csv")


# In[3]:


registration_df['Registration Time'] = pd.to_datetime(registration_df['Registration Time'].astype(str),format='%d-%m-%Y %H:%S')


# In[4]:


registration_df['Registration_date']=registration_df['Registration Time'].dt.date


# In[5]:

registration_df_grp = pd.DataFrame(registration_df.groupby(['Registration_date','Outreach_Partner','Medium'])['Medium'].count().reset_index(name='Count'))

registration_medium = pd.DataFrame(registration_df_grp.groupby(['Medium'])['Count'].sum().reset_index(name='Total'))

registration_count = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())

registration_outreachpartner = pd.DataFrame(registration_count.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)


# In[8]:


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])


# In[ ]:


app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('widslogo.jpg'),
                     id = 'wids-image',
                     style={'height': '60px',
                            'width': 'auto',
                            'margin-bottom': '25px'})


            ], className='one-third column'),

        html.Div([
            html.Div([
                html.H3('WiDS Conference Pune, 2021', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('Track Registrations for the Conference', style={'margin-bottom': '0px', 'color': 'white'})
            ])

        ], className='one-half column', id = 'title'),

        html.Div([
            html.H6('Last Updated: ' + str(registration_df['Registration_date'].iloc[-1].strftime('%B %d, %Y')),
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1'),
        ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),

    html.Div([
        html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('whatsapp.png'),
                     id = 'whatsapp',
                     style={'height': '40px',
                            'width': 'auto',
                            'margin-bottom': '25px'})

            ], className='one-third column') ,           
            html.H6(children='WHATS APP',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{registration_medium[registration_medium['Medium']=='WHATS APP GROUP']['Total'].iloc[0]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30})

        ], className='card_container three columns'),
        
        html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('gmaillogo.jpg'),
                     id = 'gmaillogo',
                     style={'height': '40px',
                            'width': 'auto',
                            'margin-bottom': '25px'})
             ], className='one-third column') ,            
            html.H6(children='EMAIL',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{registration_medium[registration_medium['Medium']=='EMAIL']['Total'].iloc[0]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30})

        ], className='card_container three columns'),    
        html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('wordofmouth.png'),
                     id = 'wordofmouth',
                     style={'height': '40px',
                            'width': 'auto',
                            'margin-bottom': '25px'})
             ], className='one-third column') ,              
            html.H6(children='WORD OF MOUTH',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{registration_medium[registration_medium['Medium']=='WORD OF MOUTH']['Total'].iloc[0]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30})

        ], className='card_container three columns'),         
        html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('facebook.png'),
                     id = 'facebook',
                     style={'height': '40px',
                            'width': 'auto',
                            'margin-bottom': '25px'})
             ], className='one-third column') ,             
            html.H6(children='SOCIAL MEDIA',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{registration_medium[registration_medium['Medium']=='SOCIAL MEDIA WIDS PUNE']['Total'].iloc[0]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30})

        ], className='card_container three columns'),     
        html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('partner.png'),
                     id = 'partner',
                     style={'height': '40px',
                            'width': 'auto',
                            'margin-bottom': '25px'})
             ], className='one-third column') ,              
            html.H6(children='PARTNER',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{registration_medium[registration_medium['Medium']=='OUT REACH PARTNER']['Total'].iloc[0]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30})

        ], className='card_container three columns'), 
        
    ], className='row flex-display'),
    html.Div([
        html.Div([
            html.P('Select Partner:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id = 'OutPartner',
                         multi = False,
                         searchable= True,
                         value='Accenture',
                         placeholder= 'Select Partner',
                         style={'color': 'white'},
                         options= [{'label': c, 'value': c}
                                   for c in (registration_outreachpartner['Outreach_Partner'].unique())],className='dcc_compon'),
            html.P('Outreach Partner registrations across mediums: ',className='fix_label', style={'text-align': 'center', 'color': 'white','margin-bottom': '15px'}),            
            dcc.Graph(id = 'WHATSAPP', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-bottom': '20px','margin-top': '20px'}),
            dcc.Graph(id = 'EMAIL', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
             dcc.Graph(id = 'WORD_OF_MOUTH', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
            dcc.Graph(id = 'SOCIAL_MEDIA', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
            dcc.Graph(id = 'PARTNER', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),            

            ], className='create_container two columns'),
        
        html.Div([ dcc.Graph(id = 'pie_chart', config={'displayModeBar': 'hover'})
        ], className='create_container four columns'),
        
        html.Div([dcc.Graph(id = 'line_chart', config={'displaylogo': False}
                      )
        ], className='create_container six columns'),        
        
        ], className='row flex-display'),
], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(Output('WHATSAPP', 'figure'),
              [Input('OutPartner','value')])
def update_confirmed(OutPartner):
    registration_medium = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())
    registration_outreachpartner = pd.DataFrame(registration_medium.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)
    value_WHATSAPP = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['WHATS APP GROUP'].iloc[0]
    return {
        'data': [go.Indicator(
               mode='number',
               value=value_WHATSAPP,
               number={
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'WHATSAPP',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50
        )
    }


@app.callback(Output('EMAIL', 'figure'),
              [Input('OutPartner','value')])
def update_confirmed(OutPartner):
    registration_medium = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())
    registration_outreachpartner = pd.DataFrame(registration_medium.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)
    value_EMAIL = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['EMAIL'].iloc[0]
    return {
        'data': [go.Indicator(
               mode='number',
               value=value_EMAIL,
               number={
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'EMAIL',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }


@app.callback(Output('WORD_OF_MOUTH', 'figure'),
              [Input('OutPartner','value')])
def update_confirmed(OutPartner):
    registration_medium = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())
    registration_outreachpartner = pd.DataFrame(registration_medium.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)
    value_WORD_OF_MOUTH = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['WORD OF MOUTH'].iloc[0]
    return {
        'data': [go.Indicator(
               mode='number',
               value=value_WORD_OF_MOUTH,
               number={
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'WORD OF MOUTH',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }


@app.callback(Output('PARTNER', 'figure'),
              [Input('OutPartner','value')])
def update_confirmed(OutPartner):
    registration_medium = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())
    registration_outreachpartner = pd.DataFrame(registration_medium.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)
    value_PARTNER = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['OUT REACH PARTNER'].iloc[0]
    return {
        'data': [go.Indicator(
               mode='number',
               value=value_PARTNER,
               number={
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'OUT REACH PARTNER',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }

@app.callback(Output('SOCIAL_MEDIA', 'figure'),
              [Input('OutPartner','value')])
def update_confirmed(OutPartner):
    registration_medium = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())
    registration_outreachpartner = pd.DataFrame(registration_medium.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)
    value_SOCIAL_MEDIA = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['SOCIAL MEDIA WIDS PUNE'].iloc[0]
    return {
        'data': [go.Indicator(
               mode='number',
               value=value_SOCIAL_MEDIA,
               number={
                       'font': {'size': 20}},
               domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'SOCIAL MEDIA',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )
    }

@app.callback(Output('pie_chart', 'figure'),
              [Input('OutPartner','value')])
def update_graph(OutPartner):
    registration_medium = pd.DataFrame(registration_df_grp.drop(columns = 'Registration_date').groupby(['Outreach_Partner','Medium']).count().reset_index())
    registration_outreachpartner = pd.DataFrame(registration_medium.pivot(index='Outreach_Partner', columns='Medium', values='Count')).reset_index().fillna(0)

    value_WHATSAPP = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['WHATS APP GROUP'].iloc[0]
    value_EMAIL = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['EMAIL'].iloc[0]
    value_WORD_OF_MOUTH = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['WORD OF MOUTH'].iloc[0]
    value_PARTNER = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['OUT REACH PARTNER'].iloc[0]
    value_SOCIAL_MEDIA = registration_outreachpartner[registration_outreachpartner['Outreach_Partner'] == OutPartner]['SOCIAL MEDIA WIDS PUNE'].iloc[0]    
    
    colors = ['orange', '#dd1e35', 'green', '#e55467','purple']

    return {
        'data': [go.Pie(
            labels=['WhatsApp', 'Email', 'Word Of Mouth', 'Social Media','Partner'],
            values=[value_WHATSAPP, value_EMAIL, value_WORD_OF_MOUTH, value_SOCIAL_MEDIA,value_PARTNER],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+percent',
            hole=.6,
            #rotation=45,
            # insidetextorientation= 'radial'

        )],

        'layout': go.Layout(
            title={'text': 'Total Registrations: ' + (OutPartner),
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}


        )
    }

@app.callback(Output('line_chart', 'figure'),
              [Input('OutPartner','value')])
def update_graph(OutPartner):
    registration_datewise = pd.DataFrame(registration_df_grp.groupby(['Registration_date','Outreach_Partner','Medium'])['Medium'].count().fillna(0).reset_index(name='Count'))
    registration_partner = registration_datewise[registration_datewise['Outreach_Partner']==OutPartner].groupby(['Registration_date'])['Count'].sum().reset_index()
    min_date = min(registration_partner['Registration_date']).strftime('%Y-%m-%d')
    max_date = max(registration_partner['Registration_date']).strftime('%Y-%m-%d')
    return {   'data': [go.Scatter(
                x=registration_partner['Registration_date'].astype(str),
                y=registration_partner['Count'],
                mode='lines',
                name='Registration by the Outreach Partner' ,
                line=dict(width=4, color='#FF00FF'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + registration_partner['Registration_date'].astype(str) + '<br>' +
                '<b>Registrations</b>: ' + [f'{x:,.0f}' for x in registration_partner['Count']] + '<br>'


            )],

        'layout': go.Layout(
            title={'text': 'Registration from ' + min_date+' to '+ max_date,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Registration Date</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>No. of Registrations</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
                       )


        )
    }


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True)

