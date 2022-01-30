from brownie import accounts, network, Lottery, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mock,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_lottery():
    account = get_account()
    # need to pass the price feed address in fundme contract
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price"]
    else:
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address

    lottery = Lottery.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {lottery.address}")


def main():
    deploy_lottery()
