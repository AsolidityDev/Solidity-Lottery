from brownie import (
    accounts,
    config,
    network,
    MockV3Aggregator,
    Contract,
    interface,
    LinkToken,
)
from web3 import Web3


DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache_local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]


def get_account(index=None, id=None):

    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]


contract_to_mock = {"eth_usd_price": MockV3Aggregator, "link_token": LinkToken}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise it will deploy a mock version of that contract and return
    that mock contract.

        Args:
            Contract_name (string)

        Returns:
            brownie.network.contract.projectcontract: the most recent deployed version of this contract.
    """

    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mock()
            # price_feed_address = config["networks"][network.show_active()]["eth_usd_price"]
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mock():
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying mock...")
    mock_aggregator = MockV3Aggregator.deploy(
        DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": account}
    )
    link_token = LinkToken.deploy({"from": account})
    print("Mock deployed")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("funded contracts!")
    return tx
