from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy_lottery import deploy_lottery
from brownie import network, accounts, Lottery, exceptions
from web3 import Web3
import pytest
import brownie

# test to check how much eth is $50
# should be around 0.025 (in our local blockchain - mock contract)

# this is unit tests below


def test_get_entrance_lottery():
    # this line here will allow us to skip the test if this is done in a test/forked blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    deploy_lottery()
    lottery = Lottery[-1]
    print(lottery.address)
    entrance_fee = lottery.getEntranceFee()
    print(entrance_fee)
    expected_entrance_fee = Web3.toWei(0.025, "ether")

    assert expected_entrance_fee == entrance_fee
    # assert lottery.getEntranceFee() > Web3.toWei(0.019, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.020, "ether")


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()
    # lottery = Lottery[-1]
    print(lottery)
    # Act / Assert
    with brownie.reverts():
        # with pytest.reverts():
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
