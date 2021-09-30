import json
from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from typing import Dict, List


class IPAddressPoolException(Exception):
    pass


class IPAddressPool:
    def __init__(self, ipaddr_db_json_path: str):
        self.json_path = ipaddr_db_json_path
        self._ip_version = 4
        self._network = None
        self._ipaddr_pool = []
        self._hostnames = {}
        self._load_from_json(ipaddr_db_json_path)

    @property
    def prefixlen(self):
        return self._network.prefixlen

    def used_addresses(self, cidr=True):
        addrs = dict(self._hostnames)
        if cidr:
            addrs = {k: self._cidr_addr(v) for k, v in addrs.items()}
        return addrs

    @property
    def addresses(self) -> List[IPv4Address]:
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

        iface = IPv4Interface(ipv4_cidr_address)
        network: IPv4Network = iface.network
        address_list = list(network.hosts())
        self._network = network
        self._ipaddr_pool = address_list
        self._save()

    def new_address(self, hostname: str, cidr=True) -> IPv4Address:
        if hostname in self._hostnames:
            raise IPAddressPoolException(f"Hostname {hostname} already in use")
        try:
            addr = self._ipaddr_pool.pop(0)
        except IndexError:
            raise IPAddressPoolException("Uninitialized address pool")
        self._hostnames[hostname] = addr
        self._save()
        if cidr:
            addr = self._cidr_addr(addr)
        return addr

    def address_for(self, hostname: str, cidr=True) -> IPv4Address:
        try:
            addr = self._hostnames[hostname]
        except KeyError:
            raise IPAddressPoolException(f"No address for hostname {hostname}")
        if cidr:
            addr = self._cidr_addr(addr)
        return addr

    def release_address(self, hostname):
        try:
            addr = self._hostnames.pop(hostname)
        except KeyError:
            raise IPAddressPoolException(f"No address for hostname {hostname}")

        self._ipaddr_pool.append(addr)
        self._ipaddr_pool.sort()
        self._save()

    def _cidr_addr(self, addr: IPv4Address):
        addr_str = f"{addr}/{self.prefixlen}"
        addr = IPv4Interface(addr_str)
        return addr

    def _to_dict(self):
        _dict = {
            "ip_version": self._ip_version,
            "network": str(self._network),
            "hostnames": {k: str(v) for k, v in self._hostnames.items()},
        }

        return _dict

    def _initialize_from_dict(self, ip_pool_dict: Dict):
        self._ip_version = ip_pool_dict["ip_version"]
        network = IPv4Network(ip_pool_dict["network"])
        hostnames = ip_pool_dict["hostnames"]

        # unused_addrs = ip_pool_dict["unused_addresses"]

        pool = []
        # hostnames = {}

        for hostname, addr_str in hostnames.items():
            addr = IPv4Address(addr_str)
            if addr in hostnames.values():
                dupes = [hostname, hostnames[addr]]
                raise IPAddressPoolException(
                    f"Address [{addr_str}] used more than once: {dupes} "
                )
            hostnames[hostname] = addr
        pool = list(network.hosts())
        used_addrs = list(hostnames.values())
        for used in used_addrs:
            if used in pool:
                pool.remove(used)

        self._network = network
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
