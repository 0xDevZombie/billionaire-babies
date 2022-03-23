import pytest
from brownie import BillionaireBabiesIncubator, BillionaireBabies, network, accounts, reverts, web3
from tests.BillionaireBabiesIncubator.merkle_proofs import accounts_merkle_proof

# deployed contract with sale started
@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    bbi = BillionaireBabiesIncubator.deploy(accounts[0], {"from": accounts[0]})
    bbi.setMerkleRoot('0x021a103e62c519a6bd4a9f46959b21a5c06255736055a2c943bacdd7eadfe6fc')
    bbi.togglePreSaleOpen()
    bb = BillionaireBabies.deploy(bbi, {"from": accounts[0]})

    return (bbi, bb)


def test_can_mint(deployed_contract):
    bbi, bb = deployed_contract
    bbi.preSaleMint(1, accounts_merkle_proof[0], {"value": web3.toWei("0.1", "ether")})
    bbi.setApprovalForAll(bb, True)
    bb.safeMint()

    assert bbi.balanceOf(accounts[0], 1) == 0
    assert bb.balanceOf(accounts[0]) == 1

def test_cant_mint_without(deployed_contract):
    bbi, bb = deployed_contract
    # bbi.preSaleMint(1, accounts_merkle_proof[0], {"value": web3.toWei("0.1", "ether")})
    bbi.setApprovalForAll(bb, True)
    with reverts("dev: no token"):
        bb.safeMint()



