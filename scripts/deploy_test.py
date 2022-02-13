from brownie import accounts, network, Test, config
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_test():
    account = get_account()
    test = Test.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("deployed test!")
    return test


def get_state():
    # account = get_account()
    test = Test[-1]
    state = test.get_state()
    # tx1.wait(1)
    print(state)


def open_state():
    account = get_account()
    test = Test[-1]
    tx = test.open({"from": account})
    tx.wait(1)
    print("State is open now!")


def close_state():
    account = get_account()
    test = Test[-1]
    tx = test.close({"from": account})
    tx.wait(1)
    print("State is closed!")


def main():
    deploy_test()
    get_state()
    # open_state()
    close_state()
