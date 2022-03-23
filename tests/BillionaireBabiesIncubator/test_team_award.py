import pytest
from brownie import BillionaireBabiesIncubator, network, accounts, reverts, web3
from .merkle_proofs import accounts_merkle_proof


# deployed contract with sale started
@pytest.fixture
def deployed_contract():
    if network.show_active() not in ["development"] or "fork" in network.show_active():
        pytest.skip("Only for local testing")
    nft_contract = BillionaireBabiesIncubator.deploy(accounts[0], {"from": accounts[0]})
    return nft_contract


def test_team_award(deployed_contract):
    deployed_contract.teamAward()
    assert deployed_contract.balanceOf(accounts[0], 1) == 50


def test_cannot_team_award_twice(deployed_contract):
    deployed_contract.teamAward()
    assert deployed_contract.balanceOf(accounts[0], 1) == 50
    with reverts("dev: team award claimed"):
        deployed_contract.teamAward()


def test_team_award_cap_count(deployed_contract):
    deployed_contract.teamAward()
    assert deployed_contract.tokenCount() == 50
