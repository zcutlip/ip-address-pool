from argparse import ArgumentParser

from .ip_pool import IPAddressPool


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("pool_db_json", help="Path to ip pool database json file")
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
    parsed = parser.parse_args()
    return parsed


def ip_pool_main():
    options = parse_args()
    pool = IPAddressPool(options.pool_db_json)
    if options.initialize:
        pool.initialize(options.initialize)

    if options.new_address:
        hostname = options.new_address
        addr = pool.new_address(hostname)
        print(addr)


if __name__ == "__main__":
    exit(ip_pool_main())
