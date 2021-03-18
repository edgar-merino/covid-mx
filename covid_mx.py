#! python
# -*- coding: utf-8 -*-

'''
Get the updated number of covid cases for Mexico from official source:
http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip
Plot it into a Mexico's map and generate a html file with the result map.
'''

# standard libraries
import os, sys
from zipfile import ZipFile 
# third party libraries
import requests
import pandas as pd
import plotly
import plotly.express as px

# get file from Internet before proceed
url_mx_covid='http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip'
file_name=url_mx_covid.rsplit('/', 1)[1]
print('Retrieving data from datosabiertos.salud.gob.mx ...')
r = requests.get(url_mx_covid, allow_redirects=True)
open(file_name, 'wb').write(r.content)

# unzip file and get filename within it
print('Unzipping downloaded file ...')
with ZipFile(file_name, 'r') as zip:
  names = zip.namelist()
  if len(names) != 1:
    print(f'Unexpected format for file {file_name}')
    sys.exit(1)
  data_file=names[0]
  zip.extractall()

# read and process data
print('Processing data ...')
df=pd.read_csv(data_file, encoding='latin1')
cnt_by_ent=df.groupby('ENTIDAD_UM')['ENTIDAD_UM'].count().reset_index(name='CASOS')
ent=pd.read_csv('data/entidades.csv')
tot=pd.merge(cnt_by_ent, ent, left_on='ENTIDAD_UM', right_on='ENTIDAD', how='inner')

# read update date
total=df['ID_REGISTRO'].count()
updated=df['FECHA_ACTUALIZACION'][0]
label='{:,} Casos de COVID en México, Actualizado al: {:} <br> '.format(total, updated)

# read mexico geojson information for plotting the shown map
print('Generating map ...')
repo_url='https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
mx_regions_geo=requests.get(repo_url).json()

# set map features
fig=px.choropleth(
  data_frame=tot,
  geojson=mx_regions_geo,
  locations='ESTADO',
  featureidkey='properties.name',
  color='CASOS',
  color_continuous_scale='Jet',
  #scope='north america'
)

# hide the rest of the map
fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

# set color and other features
fig.update_layout(
  title_text=label,
  font=dict(
    family='Ubuntu',
    size=18,
    color='#7f7f7f',
  ),
  annotations=[
    dict(
      x=0.55,
      y=-0.1,
      xref='paper',
      yref='paper',
      text='Fuente:<a href="https://datos.gob.mx/busca/dataset/informacion-referente-a-casos-covid-19-en-mexico">Datos abiertos México</a>',
      showarrow=False
    )
  ]
)

# show map
#fig.show()

# html file
print('Saving to file ...')
outfile='covid-'+updated+'.html'
plotly.offline.plot(fig, filename=outfile)

# remove unziped file
print('Cleaning up ...')
os.remove(data_file)
os.remove('datos_abiertos_covid19.zip')

print('Done.')
