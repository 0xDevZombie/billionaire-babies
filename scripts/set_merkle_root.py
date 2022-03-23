#!/usr/bin/python3
import os
from brownie import BillionaireBabiesIncubator, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    deployed_contract = BillionaireBabiesIncubator[len(BillionaireBabiesIncubator) - 1]
    deployed_contract.setMerkleRoot("0x67780c7bbb74d44b329769c0fdbba0db3b5890d455ec06a268c9963f01abe88d", {"from": dev})

