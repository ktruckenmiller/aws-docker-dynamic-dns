from unittest.mock import MagicMock
from entrypoint import DynDNS
import pytest

@pytest.fixture
def main_obj():
    obj = DynDNS()
    obj.r53 = MagicMock()
    return obj

def test_get_hosted_zone(main_obj):
    main_obj.r53.list_hosted_zones.return_value={
        "HostedZones": [{
            "Id": "boston",
            "Name": 'something.com.'
        }]
    }
    main_obj.domain_name = 'mything.something.com'
    main_obj.hosted_zone = 'something.com'
    assert main_obj._get_hosted_zone_id() == 'boston'


def test_init(monkeypatch):
    monkeypatch.setenv('HOSTED_ZONE', 'mything.something.com')
    monkeypatch.setenv('DOMAIN_NAME', 'something.com')
    main_obj = DynDNS()
    assert main_obj.domain_name == 'something.com'
    assert main_obj.hosted_zone == 'mything.something.com'


# def test_start(monkeypatch):
#     monkeypatch.setenv('HOSTED_ZONE', 'kloudcover.com')
#     monkeypatch.setenv('DOMAIN_NAME', 'vpn.kloudcover.com')
#     obj = DynDNS()
#     obj.start()
