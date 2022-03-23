#!/usr/bin/python3
import os
from brownie import BillionaireBabiesIncubator, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    BillionaireBabiesIncubator.deploy("0x61F35A60Fa294DdC40efE5F4C16536D3e61b3D84", {"from": dev}, publish_source=True)

