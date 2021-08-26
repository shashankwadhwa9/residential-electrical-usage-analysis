DATA_BUCKET="shashank-smart-hub-data"
# location data
aws s3 cp data/locations/denver_co_1576656000.csv \
    s3://${DATA_BUCKET}/smart_hub_locations_csv/state=co/
aws s3 cp data/locations/palo_alto_ca_1576742400.csv \
    s3://${DATA_BUCKET}/smart_hub_locations_csv/state=ca/
aws s3 cp data/locations/portland_metro_or_1576742400.csv \
    s3://${DATA_BUCKET}/smart_hub_locations_csv/state=or/
aws s3 cp data/locations/stamford_ct_1576569600.csv \
    s3://${DATA_BUCKET}/smart_hub_locations_csv/state=ct/

# sensor mapping data
aws s3 cp data/mappings/ \
    s3://${DATA_BUCKET}/sensor_mappings_json/state=or/ \
    --recursive

# electrical usage data
aws s3 cp data/usage/2019-12-21/ \
    s3://${DATA_BUCKET}/smart_hub_data_json/dt=2019-12-21/ \
    --recursive
aws s3 cp data/usage/2019-12-22/ \
    s3://${DATA_BUCKET}/smart_hub_data_json/dt=2019-12-22/ \
    --recursive

# electricity rates data
aws s3 cp data/rates/ \
    s3://${DATA_BUCKET}/electricity_rates_xml/ \
    --recursive