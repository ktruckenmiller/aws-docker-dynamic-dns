#!/bin/python3
import os
import boto3
from pprint import pprint
import requests
import socket
import sys
import time
class DynDNS(object):
    def __init__(self):
        self.r53 = boto3.client('route53')
        self.hosted_zone = os.environ.get('HOSTED_ZONE')
        self.domain_name = os.environ.get('DOMAIN_NAME')
        if not self.domain_name and not self.hosted_zone:
            raise Exception("You must set your domain and hosted zone.")

    def _get_hosted_zone_id(self):
        res = self.r53.list_hosted_zones()
        for zone in res['HostedZones']:
            if self.hosted_zone in zone.get('Name'):
                return zone['Id']
        raise Exception("No hosted zone found. {}".format(res))

    def resolve_ips(self):
        self.my_ip = requests.get('http://my-ip.clustermaestro.com').text
        records = self.r53.list_resource_record_sets(
            HostedZoneId=self.hosted_zone_id,
            StartRecordType='A',
            StartRecordName=self.domain_name
        )['ResourceRecordSets']
        for record in records:
            if self.domain_name in record['Name']:
                self.dns_ip = record['ResourceRecords'][0]['Value']
                if self.dns_ip == self.my_ip:
                    print('Ip addresses are the same.')
                    return
                else:
                    print('Ip address is different')
                    print(self.dns_ip)
                    print(self.my_ip)
                    return True
        raise Exception("Could not find records in route53")

    def start(self):
        self.hosted_zone_id = self._get_hosted_zone_id()
        while True:

            if self.resolve_ips():
                try:
                    socket.inet_aton(self.my_ip)
                    socket.inet_aton(self.dns_ip)
                    # legal
                except socket.error:
                    raise Exception("No address detected")

                print('update recordset')
                res = self.r53.change_resource_record_sets(
                    HostedZoneId=self.hosted_zone_id,
                    ChangeBatch={
                        'Changes': [{
                            'Action': "UPSERT",
                            'ResourceRecordSet': {
                                'Name': self.domain_name,
                                'Type': 'A',
                                'TTL': 300,
                                'ResourceRecords': [
                                    {'Value': self.my_ip}
                                ]
                            }
                        }]
                    }
                )
                print(res)
            print("Sleeping for 60 minutes.")
            time.sleep(60*60)




dyn = DynDNS()
dyn.start()
