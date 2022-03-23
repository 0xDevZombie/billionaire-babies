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
    return nft_contract


def test_cannot_premint_when_not_open(deployed_contract):
    with reverts("dev: premint not open"):
        deployed_contract.preSaleMint(1, accounts_merkle_proof[0], {"value": web3.toWei("0.2", "ether")})


def test_cannot_more_then_allowance(deployed_contract):
    with reverts("dev: public mint not open"):
        deployed_contract.publicMint(1, {"value": web3.toWei("0.2", "ether")})
