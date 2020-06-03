# -*- coding: utf-8 -*-
"""Translate IPv4 address to Geolocations data.

This module demonstrates on using MaxMind free GeoLite2 City Database
to retrieve geo-locations data provided with an IPv4 address.

Install PyPi packages:
`pip install geoip2`

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.

You can signup and download the free GeoLite2 Database at
https://dev.maxmind.com/geoip/geoip2/geolite2/

"""

import os
import pandas as pd
import geoip2.database

APP_DIR = os.path.dirname(os.path.realpath(__file__))


def pandas_func_ip2loc(ip_addr):
    """Return geo-location data.

    Input:
    IPv4 address

    Output:
    Location dict-data.

    Sample:
     {
        'ip_addr': '99.203.80.145',
        'continent_code': 'NA',
        'country_iso_code': 'US',
        'subdiv1_iso_code': 'MD',
        'subdiv1_name': 'Maryland',
        'city': 'Elkridge',
    }
    """
    try:
        reader = geoip2.database.Reader(
            APP_DIR + '/data/GeoLite2-City/GeoLite2-City.mmdb')
        response = reader.city(ip_addr)
        return pd.Series([
            response.continent.code,
            response.country.iso_code,
            response.subdivisions.most_specific.iso_code,
            response.subdivisions.most_specific.name,
            response.city.name,
        ])
    except:  # pylint: disable=bare-except
        return pd.Series(['', '', '', '', ''])

    return result


def main():
    """Demonstrate GeoIP2 country and city data."""

    # List of IPv4 addresses
    ipv4_list = [
        '76.91.144.129',
        '151.192.245.46',
        '151.192.224.99',
        '76.201.86.41',
        '73.237.38.59',
        '73.244.189.35',
        '47.232.146.126',
        '69.206.186.192',
        '168.235.194.43',
        '108.212.247.72',
        '69.115.106.182',
        '70.187.128.215',
        '151.124.176.104',
        '73.239.62.185',
        '103.216.195.98',
        '72.66.9.194',
        '174.44.202.157',
        '31.13.115.12',
        '69.206.207.101',
        '99.203.80.145'
    ]

    # convert the list into Pandas dataframe
    df_ip = pd.DataFrame(data=ipv4_list, columns=['ip_addr'])

    # extract values to multiple columns
    df_ip[[
        'continent_code',
        'country_iso_code',
        'subdiv1_iso_code',
        'subdiv1_name',
        'city'
    ]] = df_ip.ip_addr.apply(pandas_func_ip2loc)

    # write dataframe into csv
    # df_ip.to_csv(APP_DIR + '/data/data.csv', index=False)


if __name__ == '__main__':
    main()
