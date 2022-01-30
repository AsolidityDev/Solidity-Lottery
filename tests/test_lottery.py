from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy_lottery import deploy_lottery
from brownie import network, accounts, Lottery, exceptions
from web3 import Web3
import pytest

# test to check how much eth is $50
# should be around 0.019


def test_get_entrance_lottery():
    account = get_account()
    deploy_lottery()
    lottery = Lottery[-1]
    assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")
