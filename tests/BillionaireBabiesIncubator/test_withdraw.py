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


def test_get_remaining_mints(deployed_contract):
    deployed_contract.preSaleMint(5, accounts_merkle_proof[0], {"value": web3.toWei("1", "ether")})

    pre_balance = web3.fromWei(accounts[0].balance(), "ether")
    deployed_contract.withdrawFunds()
    after_balance = web3.fromWei(accounts[0].balance(), "ether")
    assert after_balance - pre_balance == 1


def test_only_owner_can_withdraw(deployed_contract):
    with reverts("Ownable: caller is not the owner"):
        deployed_contract.withdrawFunds({"from": accounts[1]})