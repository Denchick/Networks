import ipaddress
import logging
import socket
import re
import subprocess
import ipwhois
import warnings
import argparse

warnings.simplefilter("ignore")

class ASTracer:

    def __init__(self, host_or_ip):
        if (self.is_ip_address(host_or_ip)):
            self.dst_ip = host_or_ip
        try:
            self.dst_ip = socket.gethostbyname(host_or_ip)
        except socket.error as e:
            raise IOError('Unable to resolve {}: {}', self.dst, e)
    
    def is_ip_address(self, ip):
        try:
            ipaddress.ip_address(ip) # raise ValueError if not ip
            return True
        except ValueError:
            return False

    def tracert(self):
        print('Start trace routing.')
        p = subprocess.Popen(['tracert', '-d', self.dst_ip], stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            yield line.decode('cp866').strip()
            
    def run(self):
        for query in self.tracert():
            match = re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', query)
            if match:
                ip = match.group(0)
                try:
                    ip = ip.replace('-', '.')
                    obj = ipwhois.IPWhois(ip)
                    result = obj.lookup_rdap()
                    print(f"{query}\t AS{result['asn']} \t {result['asn_description']} \t {result['asn_registry']}")
                except ipwhois.exceptions.IPDefinedError:
                    number = query.split()[0]
                    print(f'{number}\t{ip} is Private-Use via RFC 1918.')
            else:
                print(query)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='autonomous System tracing tool.')
    parser.add_argument('address', help="server`s IP or domain_name")
    args = vars(parser.parse_args())

    obj = ASTracer(args['address'])
    obj.run()
