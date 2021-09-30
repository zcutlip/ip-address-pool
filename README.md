# IP Address Pool

## Description

This is a tool to generate a list of IP addresses and track which ones are used. For example, tooling that generates VPN profiles can request a new address, and this will hand out the next available one and make a note of it. When an address is no longer required, it can be returned to the pool.

Currently only supports IPv4.

## Example Usage

Usage:

```Console
$ ip-pool --help
usage: ip-pool [-h] [--initialize CIDR_ADDRESS] [--new-address HOSTNAME] [--release-address HOSTNAME]
               [--address-for HOSTNAME]
               pool_db_json

positional arguments:
  pool_db_json          Path to IP pool database json file

optional arguments:
  -h, --help            show this help message and exit
  --initialize CIDR_ADDRESS
                        Initialize IP pool with the provided CIDR address/netmask
  --new-address HOSTNAME
                        Allocate next unused address to HOSTNAME
  --release-address HOSTNAME
                        Release address for HOSTNAME and return it to the pool
  --address-for HOSTNAME
                        Print address for HOSTNAME
```

The following will initialize a new IP address pool, but not allocate any addresses:

```Console
$ ip-pool ./pool.json --initialize "192.168.8.1/24"
$ cat pool.json
{
  "ip_version": 4,
  "network": "192.168.8.0/24",
  "hostnames": {}
}
```

Request a new address for hostname (or other identifier) `server_1`:

```Console
$ ip-pool ./pool.json --new-address server_1
192.168.8.1/24
```

Return a new address for hostname `server_1`:

```Console
$ ip-pool ./pool.json --release-address server_1
```

Reassign an address from host_2 to host_3:

```Console
$  ip-pool ./pool.json --release-address host_2 --new-address host_3
192.168.8.2/24
```

Get the address for `host_3`:

```Console
$ ip-pool pool.json --address-for host_3
192.168.8.2/24
```

List all addresses and their identifiers in use:

```Console
 $ ip-pool pool.json --list-used
host_1: 192.168.8.1/24
host_3: 192.168.8.2/24
```
