import geopandas as gpd
import pandas as pd
from dash import Dash, html, dcc
#from dash.dependencies import Input, Output
import plotly.express as px
#Datos
spdf_url = 'https://raw.githubusercontent.com/eduardoge13/dashboard-render/master/src/data/spdf_nacional.csv'
spdf = pd.read_csv(spdf_url) # por medio de github

spdf = spdf.loc[:,["cvegeo", 'mean_ntl', 'max_ntl', 'min_ntl', 'median_sum_ntl', 'median_ntl']]
pov_ntl_shp = gpd.read_file('https://github.com/eduardoge13/dashboard-render/blob/master/src/data/shapefile/pov_index_ntl.shp')
map_prueba = gpd.read_file('https://github.com/eduardoge13/dashboard-render/blob/master/src/data/shapefileinegi/marco_municipal_04_23.shp')
#  transfromacion de datos
pov_ntl_shp = pov_ntl_shp.join(spdf.set_index("cvegeo"), on="cvegeo", how = "left")

# Graficos
 #Scatter bla bla bla
fig = px.scatter(pov_ntl_shp, y="log_sum", x="IPI", color="por_pov", hover_name="Municipio", log_y=True)
 #Histograma
 # Top 10 municipios con mayor suma de luces y mayor IPI
top_log_sum = pov_ntl_shp.sort_values(by='log_sum', ascending=False)[:10]
top_IPI = pov_ntl_shp.sort_values(by='IPI', ascending=False)[:10]

fig1 = px.bar(top_log_sum, y='Municipio', x='log_sum', title='Top 10  municipios por logaritmo de la suma de luminosidad', hover_name="Municipio", orientation="h")
fig2 = px.bar(top_IPI, y='Municipio', x='IPI', title='Top 10 municipios por Indice de pobreza', hover_name="Municipio", orientation="h")


## Mapas
map1 = px.choropleth_mapbox(pov_ntl_shp, geojson=pov_ntl_shp.geometry,
                            locations=pov_ntl_shp.index,color='log_sum',
                            center={'lat': 19.4326, 'lon': -99.1332},
                           mapbox_style='open-street-map',zoom=4,
                           opacity=0.5, hover_name='Municipio', hover_data=['IPI','por_pov'],
                           title='Log_sum Values by Municipality')

map2 = px.choropleth_mapbox(pov_ntl_shp, geojson=pov_ntl_shp.geometry,
                            locations=pov_ntl_shp.index,color='mean_ntl',
                            center={'lat': 19.4326, 'lon': -99.1332},
                           mapbox_style='open-street-map',zoom=4,
                           opacity=0.5, hover_name='Municipio', hover_data=['IPI','por_pov'],
                           title='Maximo de luminosidad por municipio')




# App
app = Dash(__name__)
server = app.server
# Layout
app.layout = html.Div([
    html.H1("Dashboard"),
    html.Div([
        html.H2("Scatter Plot"),
        dcc.Graph(figure=fig)
    ],),
    html.Div([
        html.H2("Histogram"),
        dcc.Graph(figure=fig1)
    ],),
    html.Div([
        html.H2("Histogram"),
        dcc.Graph(figure=fig2)
    ], ),
    html.Div([
        html.H2("Map"),
        dcc.Graph(figure=map1),
        dcc.Graph(figure=map2)
    ], ),
])


   

if __name__ == '__main__':
    app.run(debug=True)




