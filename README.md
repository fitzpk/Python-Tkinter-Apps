# Python-Tkinter-Apps
Geo-spatial Python Applications Built using Tkinter

# App #1 - GeoJSON Polygon Area & Perimeter Calculator

Using a Tkinter GUI, this application takes GeoJSON polygon data (Features or Feature Collections) and calculates the area (km2) and perimeter (km) of each polygon within the given data file. The option to export the results is also provided.

Sample GeoJSON Data:<br>
`{`<br>
  `"type": "FeatureCollection",`<br>
  `"features": [`<br>
    `{`<br>
     ` "type": "Feature",`<br>
      `"properties": {`<br>
	`"name": "Wyoming"`<br>
	`},`<br>
      `"geometry": {`<br>
        `"type": "Polygon",`<br>
	`"coordinates":[[
	[-109.080842,45.002073],
	[-105.91517,45.002073],
	[-104.058488,44.996596],
	[-104.053011,43.002989],
	[-104.053011,41.003906],
	[-105.728954,40.998429],
	[-107.919731,41.003906],
	[-109.04798,40.998429],
	[-111.047063,40.998429],
	[-111.047063,42.000709],
	[-111.047063,44.476286],
	[-111.05254,45.002073],
	[-109.080842,45.002073]
	]]
      }
    }
  ]
}`

GUI Interface:

<img src="https://github.com/fitzpk/Python-Tkinter-Apps/blob/master/images/geocalc-gui.png" width="350"/>

Output Text File:

<img src="https://github.com/fitzpk/Python-Tkinter-Apps/blob/master/images/geocalc-output.png" width="400" height="320"/>

# App #2 - GeoJSON Point-in-Sample Area Analyzer

Sample GeoJSON Data:
`Stuff Here`
