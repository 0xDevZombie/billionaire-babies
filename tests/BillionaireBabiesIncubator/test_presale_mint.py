import pytest
from brownie import BillionaireBabiesIncubator, network, accounts, reverts, web3
from .merkle_proofs import accounts_merkle_proof


# deployed contract with sale started
@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = BillionaireBabiesIncubator.deploy(accounts[0], {"from": accounts[0]})
    nft_contract.setMerkleRoot('0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    nft_contract.setPreSaleMintPrice(web3.toWei("0.2", "ether"))
    nft_contract.togglePreSaleOpen()
    return nft_contract


def test_cannot_more_then_allowance(deployed_contract):
    deployed_contract.preSaleMint(5, accounts_merkle_proof[0], {"value": web3.toWei("1", "ether")})
    with reverts("dev: amount would exceed address allowance"):
        deployed_contract.preSaleMint(1, accounts_merkle_proof[0], {"value": web3.toWei("0.2", "ether")})


def test_cannot_more_then_allowance_2(deployed_contract):
    with reverts("dev: amount would exceed address allowance"):
        deployed_contract.preSaleMint(6, accounts_merkle_proof[0], {"value": web3.toWei("2.2", "ether")})


def test_mint_separate_tx(deployed_contract):
    deployed_contract.preSaleMint(2, accounts_merkle_proof[0], {"value": web3.toWei("1", "ether")})
    deployed_contract.preSaleMint(3, accounts_merkle_proof[0], {"value": web3.toWei("1", "ether")})

    assert deployed_contract.balanceOf(accounts[0], 1) == 5


# def test_cannot_mint_more_then_cap(deployed_contract):
#     for x in range(3):
#         deployed_contract.preSaleMint(5, accounts_merkle_proof[x],
#                                       {"from": accounts[x], "value": web3.toWei("2", "ether")})
#     with reverts("dev: mint would exceed max token supply"):
#         deployed_contract.preSaleMint(3, accounts_merkle_proof[3],
#                                       {"from": accounts[3], "value": web3.toWei("1.2", "ether")})

def test_cannot_mint_under_price(deployed_contract):
    with reverts("dev: msg.value too low"):
        deployed_contract.preSaleMint(2, accounts_merkle_proof[0], {"value": web3.toWei("0.2", "ether")})
    with reverts("dev: msg.value too low"):
        deployed_contract.preSaleMint(1, accounts_merkle_proof[0], {"value": web3.toWei("0.19", "ether")})
