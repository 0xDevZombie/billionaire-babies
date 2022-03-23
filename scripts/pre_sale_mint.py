#!/usr/bin/python3
from brownie import BillionaireBabiesIncubator, accounts, network, config, web3


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    deployed_contract = BillionaireBabiesIncubator[len(BillionaireBabiesIncubator) - 1]

    deployed_contract.preSaleMint(4, ['0x776f09a9abb13d10c92ded9de2fa52dab93eab5db2ae1c05e39bc711a92b095c'],
                                  {"from": dev, "value": web3.toWei("0.1", "ether")})


