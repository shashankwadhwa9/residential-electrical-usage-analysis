# Residential Electrical Usage Analysis

----
### About


* A hypothetical Smart Hub wirelessly collects detailed electrical usage data from individual, smart electrical receptacles and electrical circuit meters, spread throughout the residence.
* The goal of the Smart Hub is to enable the customers, using data, to reduce their electrical costs.
* The provider benefits from a reduction in load on the existing electrical grid and a better distribution of daily electrical load as customers shift usage to off-peak times to save money.

### Data description and preview

1. **Smart Hub electrical usage data**
   * There are a total of ten electrical sensors whose electrical usage in kilowatt-hours (kW) is recorded and transmitted. Each Smart Hub records and transmits electrical usage for 10 device sensors, 288 times per day (24 hr / 5 min intervals), for a total of 2,880 data points per day, per Smart Hub. 
   * There are two days worth of usage data for the demonstration, for a total of 5,760 data points.
   * ![](docs/usage_data.png)
2. **Smart Hub sensor mappings**
   * Mapping of the sensor column in the usage data e.g. ‘s_01’ to the corresponding actual device e.g., ‘Central Air Conditioner’
   * ![](docs/mappings_data.png)
3. **Smart Hub residential locations data**
   * Coordinates, home address and timezone for each residential Smart Hub.
   * ![](docs/locations_data.png)
4. **Electrical rates data**
   * Contains the cost of electricity
   * ![](docs/rates_data.png)

### AWS Services Used for Analysis

* **S3** - for storing all the raw data
* **Glue** - for preparing the data for analytics
* **Glue Data Catalog** - for storing the associated metadata (e.g., table definition and schema) 
* **Athena** - for querying the data on S3
* **QuickSight** - for creating the dashboard
* **Lambda** - for running a serverless function on the cloud


### Steps

1. Copy the raw data to S3. Usage data will be partitioned by date, whereas location and mapping data will be partitioned by state.
2. Run the glue crawlers to create the metadata for the raw data.
3. Create a lambda which will convert the raw usage, mappings and locations data to Parquet using Athena CTAS.
4. Convert the rates raw data (which is in XML format) to parquet using Glue job.
5. Create a lambda to create transformed data by joining multiple tables.
6. Create a lambda to have one single transformed parquet file, instead of multiple small files.
7. Cleanup resources