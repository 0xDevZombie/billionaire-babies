#!/usr/bin/python3
import os
from brownie import BillionaireBabiesIncubator, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    deployed_contract = BillionaireBabiesIncubator[len(BillionaireBabiesIncubator) - 1]
    deployed_contract.teamAward({"from": dev})

