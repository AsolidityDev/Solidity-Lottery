from brownie import accounts, network, Lottery, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price").address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx1 = lottery.startLottery({"from": account})
    tx1.wait(1)
    print("Lottery started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx2 = lottery.enter({"from": account, "value": value})
    tx2.wait(1)
    print("You've entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund contract with link
    tx3 = fund_with_link(lottery.address)
    tx3.wait(1)

    # call the end of lottery function
    tx4 = lottery.endLottery({"from": account})
    tx4.wait(1)

    print(f"{lottery.recentWinner()} is the lottery winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
