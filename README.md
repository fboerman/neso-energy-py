# NESO-energy-py
![tests](https://github.com/fboerman/neso-energy-py/actions/workflows/run-tests.yml/badge.svg)

This package is a light weight wrapper around the [NESO energy data platform](https://www.neso.energy/data-portal) of the Electricity Operator of GB, NESO.

## Installation
There are 2 clients:
* ```NesoClient```: returns ```pandas``` dataframes
* ```NesoRawClient```: returns raw data without further parsing in a dataframe

If you do not need the ```pandas``` parsing and just use ```NesoRawClient```, install the package with ```pip install neso-energy-py```  
If you do need the parsing and want to use ```NesoClient```, install the package with ```pip install neso-energy-py[pandas]```

The package will detect the presence of ```pandas``` and make ```NesoClient``` available if possible.

## Example Usage
```python
from nesoenergy import NesoClient
client = NesoClient()
print('Available data sets:')
print(client.DATASETS)

# This download corresponds to the UI page: https://www.neso.energy/data-portal/historic-demand-data/historic_demand_data_2025

# Download the full dataset by simple csv download
df_csv = client.get_resource_csv_by_name(
    data_set='historic-demand-data',
    resource_name='historic_demand_data_2025'
)

# Download the data with a sql filter
df_filtered = client.query_resource_by_name(
    data_set='historic-demand-data',
    resource_name='historic_demand_data_2025',
    filter='"ENGLAND_WALES_DEMAND" > 30000'
)

```

There are several other functions to help you use it, the names should be self-explanatory. If not please open a github issue!