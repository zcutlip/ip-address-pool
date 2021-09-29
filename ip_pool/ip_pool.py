import ipaddress
import json
from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from typing import Dict


class IPAddressPoolException(Exception):
    pass


class IPAddressPool:
    def __init__(self, ipaddr_db_json_path: str):
        self.json_path = ipaddr_db_json_path
        self._ip_version = 4
        self._prefix_len = 0
        self._ipaddr_pool = []
        self._hostnames = {}
        self._load_from_json(ipaddr_db_json_path)

    @property
    def addresses(self):
        addresses = list(self._ipaddr_pool)
        addresses.extend(self._hostnames.keys())
        addresses.sort()

        return addresses

    def is_initialized(self):
        initialized = len(self._ipaddr_pool) > 0
        return initialized

    def initialize(self, ipv4_cidr_address: str):
        if self.is_initialized():
            raise IPAddressPoolException("Address pool already initialized")

        prefix_len, address_list = self._generate_addresses(ipv4_cidr_address)

        self._ipaddr_pool = address_list
        self._prefix_len = prefix_len
        self._save()

    def new_address(self, hostname: str):
        if hostname in self._hostnames:
            raise IPAddressPoolException(f"Hostname {hostname}")
        try:
            addr = self._ipaddr_pool.pop(0)
        except IndexError:
            raise IPAddressPoolException("Uninitialized address pool")
        self._hostnames[hostname] = addr
        self._save()
        return addr

    def address_for(self, hostname: str) -> IPv4Address:
        try:
            addr = self._hostnames[hostname]
        except KeyError:
            raise IPAddressPoolException(f"No address for hostname {hostname}")
        return addr

    def release_address(self, hostname):
        try:
            addr = self._hostnames.pop(hostname)
        except KeyError:
            raise IPAddressPoolException(f"No address for hostname {hostname}")

        self._ipaddr_pool.append(addr)
        self._ipaddr_pool.sort()
        self._save()

    def _to_dict(self):
        _dict = {
            "ip_version": self._ip_version,
            "network_prefix_len": self._prefix_len,
            "unused_addresses": [str(k) for k in self._ipaddr_pool],
            "hostnames": {k: str(v) for k, v in self._hostnames.items()},
        }

        return _dict

    def _initialize_from_dict(self, ip_pool_dict: Dict):
        self._ip_version = ip_pool_dict["ip_version"]
        self._prefix_len = ip_pool_dict["network_prefix_len"]
        unused_addrs = ip_pool_dict["unused_addresses"]
        hostnames = ip_pool_dict["hostnames"]

        pool = []
        # hostnames = {}

        for addr_str in unused_addrs:
            addr = IPv4Address(addr_str)
            pool.append(addr)

        for hostname, addr_str in hostnames.items():
            addr = IPv4Address(addr_str)
            if addr in hostnames.values():
                dupes = [hostname, hostnames[addr]]
                raise IPAddressPoolException(
                    f"Address [{addr_str}] used more than once: {dupes} "
                )
            hostnames[hostname] = addr

        self._hostnames = hostnames
        self._ipaddr_pool = pool

    def _save(self):
        save_dict = self._to_dict()
        json.dump(save_dict, open(self.json_path, "w"), indent=2)

    def _load_from_json(self, json_path):
        try:
            loaded = json.load(open(json_path, "r"))
            self._initialize_from_dict(loaded)
        except FileNotFoundError:
            pass

    def _generate_addresses(self, cidr_address):
        iface: IPv4Interface = ipaddress.ip_interface(cidr_address)
        network: IPv4Network = iface.network
        prefix_len = network.prefixlen
        hosts = list(network.hosts())
        return prefix_len, hosts
