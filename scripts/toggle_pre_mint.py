#!/usr/bin/python3
import os
from brownie import BillionaireBabiesIncubator, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    deployed_contract = BillionaireBabiesIncubator[len(BillionaireBabiesIncubator) - 1]
    deployed_contract.togglePreSaleOpen( {"from": dev})

