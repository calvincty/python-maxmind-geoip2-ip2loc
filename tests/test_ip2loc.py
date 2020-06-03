"""Unit test cases in PyTest.

test_ip2loc: test with single ip address
test_pandas_ip2loc: test with a Pandas dataframe with list of ip addresses
"""

import os
import pandas as pd
import pytest
from apps import ip2loc, pandas_ip2loc as pd_ip2loc


TEST_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.it('Test getting geo information given an IPv4 address')
def test_ip2loc():
    """Test getting geo information given an IPv4 address."""
    ip_addr = '99.203.80.145'
    data = ip2loc.ip2loc(ip_addr)

    assert data['continent_code'] == 'NA'
    assert data['country_iso_code'] == 'US'
    assert data['subdiv1_iso_code'] == 'MD'
    assert data['subdiv1_name'] == 'Maryland'
    assert data['city'] == 'Elkridge'


@pytest.mark.it('Test getting geo information given a Panda DataFrame')
def test_pandas_ip2loc():
    """Test getting geo information given a Panda DataFrame."""
    ipv4_list = [
        '99.203.80.145',
        '76.91.144.129',
        '151.192.245.46',
        '151.192.224.99',
        '76.201.86.41',
        '0.0.0.0',
        'xx.ss.vasdacsa'
    ]
    df_test = pd.DataFrame(data=ipv4_list, columns=['ip_addr'])
    df_test[[
        'continent_code',
        'country_iso_code',
        'subdiv1_iso_code',
        'subdiv1_name',
        'city'
    ]] = df_test.ip_addr.apply(pd_ip2loc.pandas_func_ip2loc)

    assert df_test[df_test['ip_addr'] ==
                   '99.203.80.145']['continent_code'].values[0] == 'NA'
    assert df_test[df_test['ip_addr'] ==
                   '99.203.80.145']['country_iso_code'].values[0] == 'US'
    assert df_test[df_test['ip_addr'] ==
                   '99.203.80.145']['subdiv1_name'].values[0] == 'Maryland'
    # ip address without geo information
    assert df_test[df_test['ip_addr'] ==
                   '0.0.0.0']['country_iso_code'].values[0] == ''
    # ip address without subdivision
    assert df_test[df_test['ip_addr'] ==
                   '151.192.245.46']['subdiv1_iso_code'].values[0] is None
    # invalid ip address
    assert df_test[df_test['ip_addr'] ==
                   'xx.ss.vasdacsa']['country_iso_code'].values[0] == ''
