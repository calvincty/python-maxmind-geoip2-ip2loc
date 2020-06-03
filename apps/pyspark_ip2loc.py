# -*- coding: utf-8 -*-
"""Translate IPv4 address to Geolocations data in PySpark UDF.

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
from pyspark.sql import SparkSession, Row
import pyspark.sql.functions as f
import pyspark.sql.types as t
import geoip2.database
import numpy as np

APP_DIR = os.path.dirname(os.path.realpath(__file__))


@f.udf(returnType=t.StructType([
    t.StructField('continent_code', t.StringType()),
    t.StructField('country_iso_code', t.StringType()),
    t.StructField('subdiv1_iso_code', t.StringType()),
    t.StructField('subdiv1_name', t.StringType()),
    t.StructField('city', t.StringType())
]))
def udf_ip2loc(ip_addr):
    """Geolocations data with multiple columns

    Input:
    IPv4 address

    Output:
    Struct(String()) - multiple string fields with geo-data

    Sample result dataframe:
    +---------------+--------------+----------------+----------------+------------+---------------+
    |ip_addr        |continent_code|country_iso_code|subdiv1_iso_code|subdiv1_name|city           |
    +---------------+--------------+----------------+----------------+------------+---------------+
    |76.91.144.129  |NA            |US              |CA              |California  |Baldwin Park   |
    |151.192.245.46 |AS            |SG              |                |            |Singapore      |
    |151.192.224.99 |AS            |SG              |                |            |Singapore      |
    |76.201.86.41   |NA            |US              |CA              |California  |El Dorado Hills|
    |73.237.38.59   |NA            |US              |GA              |Georgia     |Ellenwood      |
    |73.244.189.35  |NA            |US              |FL              |Florida     |West Palm Beach|
    |31.13.115.12   |EU            |IE              |                |            |               |
    |69.206.207.101 |NA            |US              |NY              |New York    |Middletown     |
    |99.203.80.145  |NA            |US              |MD              |Maryland    |Elkridge       |
    +---------------+--------------+----------------+----------------+------------+---------------+
    """
    try:
        reader = geoip2.database.Reader(
            APP_DIR + '/data/GeoLite2-City/GeoLite2-City.mmdb')
        response = reader.city(ip_addr)
        return Row(
            'continent_code',
            'country_iso_code',
            'subdiv1_iso_code',
            'subdiv1_name',
            'city'
        )(
            response.continent.code,
            response.country.iso_code,
            response.subdivisions.most_specific.iso_code,
            response.subdivisions.most_specific.name,
            response.city.name
        )
    except:  # pylint: disable=bare-except
        return Row('continent_code', 'country_iso_code', 'subdiv1_iso_code',
                   'subdiv1_name', 'city')('', '', '', '', '')


def main():
    """Demonstrate GeoIP2 country and city data implemented in PySpark."""
    spark = SparkSession.builder.appName('PySpark Ip2Loc').getOrCreate()

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
    df_ipv4 = spark.createDataFrame(
        data=np.array(ipv4_list).reshape(len(ipv4_list), 1).tolist(),
        schema=t.StructType([
            t.StructField('ip_addr', t.StringType())
        ]))
    df_ipv4 = df_ipv4.withColumn('Output', udf_ip2loc('ip_addr'))
    df_ipv4.select('ip_addr', 'Output.*').fillna('').show(20, False)


if __name__ == '__main__':
    main()
