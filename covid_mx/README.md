# COVID In Mexico

Based on the data from mexican government, it plots the registered cases of COVID-19 from Mexico. 

The working data set is downloaded automatically from Internet to compute the number of cases by State and plot it in a map from Mexico. So as long as this dataset is maintaned it will provide updated information.

This version plot the cumulative cases by state no matter if it is closed or not. This program is to demonstrate how to plot information on a map from a country different of USA. Future versions (hopefully) will plot other metrics such as active cases or deceases.

## Usage

`python covid_mx.py`

The progress will be shown:

```
Retrieving data from datosabiertos.salud.gob.mx ...
Unzipping downloaded file ...
Processing data ...
Generating map ...
Saving to file ...
Cleaning up ...
Done.
```

The program generates a html interactive file with the generated map. As shown below:

![Plot](https://github.com/edgar-merino/covid-mx/img/covid-mx.png)

### Notes

Since it is needed to download the dataset, is required to have at least 1GB of free space on disk.

## Libraries

This program uses `plotly.express` to generate the map and `plotly` to save the result on a file.

## RST Links and references

- plotly.express: https://plotly.com/python/plotly-express/
- plotply: https://plotly.com/
- Video with explanation (In Spanish and not mine): https://www.youtube.com/watch?v=MaypM_PUuPk

## Copyright & License

Copyright (c) 2021, Edgar Merino. MIT License.