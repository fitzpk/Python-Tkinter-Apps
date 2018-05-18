# Python-Tkinter-Apps
Geo-spatial Python Applications Built using Tkinter

# App #1 - GeoJSON Polygon Area & Perimeter Calculator

Using a Tkinter GUI, this application takes GeoJSON polygon data (Features or Feature Collections) and calculates the area and perimeter of each polygon within the given data file.

Sample GeoJSON Data:
`{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
	"name": "Wyoming"
	},
      "geometry": {
        "type": "Polygon",
	"coordinates":[[
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
    },
    {
      "type": "Feature",
      "properties": {
	"name": "New Mexico"
	},
      "geometry": {
        "type": "Polygon",
	"coordinates":[[
	[-107.421329,37.000263],
	[-106.868158,36.994786],
	[-104.337812,36.994786],
	[-103.001438,37.000263],
	[-103.001438,36.501861],
	[-103.039777,36.501861],
	[-103.045254,34.01533],
	[-103.067161,33.002096],
	[-103.067161,31.999816],
	[-106.616219,31.999816],
	[-106.643603,31.901231],
	[-106.528588,31.786216],
	[-108.210008,31.786216],
	[-108.210008,31.331629],	
	[-109.04798,31.331629],
	[-109.042503,37.000263],
	[-107.421329,37.000263]
	]]      
      }
    }
  ]
}`



# App #2 - GeoJSON Point-in-Sample Area Analyzer

Sample GeoJSON Data:
`Stuff Here`
