## Translate IPv4 address to Geolocations data ##
This repository demonstrate a Python script using MaxMind free GeoLite2City database to translate a given IPv4 address to the desired geo-location data such as continent, country, subdivision and city.

### Using the geoip2 library ###
You are required to signup at MaxMind before able to download the free database. Sign up at https://dev.maxmind.com/geoip/geoip2/geolite2/

Place the downloaded database (.mmdb) to a directory and you will need to refer the database path in the codes.

Install the library
```
pip install geoip2
```

Using the library
```python
import geoip2.database

# initialization
reader = geoip2.database.Reader('the-mmdb-database-path')

response = reader.city('99.203.80.145')

print(response) # return the City model with the dict-like data
```

Output
```json
geoip2.models.City({'city': {'geoname_id': 4354256, 'names': {'en': 'Elkridge'}}, 'continent': {'code': 'NA', 'geoname_id': 6255149, 'names': {'de': 'Nordamerika', 'en': 'North America', 'es': 'Norteamérica', 'fr': 'Amérique du Nord', 'ja': '北アメリカ', 'pt-BR': 'América do Norte', 'ru': 'Северная Америка', 'zh-CN': '北美洲'}}, 'country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}}, 'location': {'accuracy_radius': 100, 'latitude': 39.2151, 'longitude': -76.754, 'metro_code': 512, 'time_zone': 'America/New_York'}, 'postal': {'code': '21075'}, 'registered_country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}}, 'subdivisions': [{'geoname_id': 4361885, 'iso_code': 'MD', 'names': {'de': 'Maryland', 'en': 'Maryland', 'es': 'Maryland', 'fr': 'Maryland', 'ja': 'メリーランド州', 'pt-BR': 'Maryland', 'ru': 'Мэриленд', 'zh-CN': '马里兰州'}}], 'traits': {'ip_address': '99.203.80.145', 'prefix_len': 25}}, ['en'])
```

Extract geo-location data from the output

```python
result = {
    # Continent Code: eg. NA (North America)
    'continent_code': response.continent.code,
    # Country ISO Code: eg. US
    'country_iso_code': response.country.iso_code,
    # State / Province: eg. MD / Maryland
    'subdiv1_iso_code': response.subdivisions
    .most_specific.iso_code,
    'subdiv1_name': response.subdivisions
    .most_specific.name,
    # City: eg. Elkridge
    'city': response.city.name
}
```

### Code Examples ###
Python with dict output: 
```
./apps/ip2loc.py
```

Python with Pandas dataframe:
```
./apps/pandas_ip2loc.py
```

PySpark Dataframe with UDF:
```
./apps/pyspark_ip2loc.py
```