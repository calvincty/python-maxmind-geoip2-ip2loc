import os
import json
import apps.ip2loc as ip2loc

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def test_ip2loc():
    ip_addr = '99.203.80.145'
    data = ip2loc.ip2loc(ip_addr)

    assert data['subdiv1_name'] == 'Maryland'
