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


def test_get_remaining_mints_by_address(deployed_contract):
    deployed_contract.preSaleMint(2, accounts_merkle_proof[0], {"value": web3.toWei("2", "ether")})
    assert deployed_contract.getPreSaleAddressRemainingMints(accounts[0]) == 3
    assert deployed_contract.getPublicSaleAddressRemainingMints(accounts[0]) == 5


def test_view(deployed_contract):
    assert deployed_contract.preSaleOpen() == True
    assert deployed_contract.publicSaleOpen() == False