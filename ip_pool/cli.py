import sys
from argparse import ArgumentParser
from typing import Dict

from .ip_pool import IPAddressPool, IPAddressPoolException


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("pool_db_json", help="Path to IP pool database json file")
    parser.add_argument(
        "--initialize",
        metavar="CIDR_ADDRESS",
        help="Initialize IP pool with the provided CIDR address/netmask",
    )
    parser.add_argument(
        "--new-address",
        metavar="HOSTNAME",
        help="Allocate next unused address to HOSTNAME",
    )
    parser.add_argument(
        "--release-address",
        metavar="HOSTNAME",
        help="Release address for HOSTNAME and return it to the pool",
    )

    parser.add_argument(
        "--address-for", metavar="HOSTNAME", help="Print address for HOSTNAME"
    )

    parser.add_argument(
        "--list-used",
        action="store_true",
        help="List used IP addresses and identifiers",
    )
    parsed = parser.parse_args()
    return parsed


def ip_pool_main():
    options = parse_args()
    try:
        pool = IPAddressPool(options.pool_db_json)
        if options.initialize:
            pool.initialize(options.initialize)

        if options.release_address:
            hostname = options.release_address
            pool.release_address(hostname)

        if options.new_address:
            hostname = options.new_address
            addr = pool.new_address(hostname)
            print(addr)

        if options.address_for:
            hostname = options.address_for
            addr = pool.address_for(hostname)
            print(addr)

        if options.list_used:
            used_addrs: Dict = pool.used_addresses()
            for host, addr in used_addrs.items():
                print(f"{host}: {addr}")

    except IPAddressPoolException as e:
        print(e, file=sys.stderr)
        return -1
    return 0


if __name__ == "__main__":
    exit(ip_pool_main())
