from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrace_fee = fund_me.getEntranceFee() + 100
    txn_1 = fund_me.fund({"from": account, "value": entrace_fee})
    txn_1.wait(1)
    assert fund_me.addressAmountMap(account.address) == entrace_fee
    txn_2 = fund_me.withdraw({"from": account})
    assert fund_me.addressAmountMap(account.address) == 0

    txn_2.wait(1)


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Omly for local testing.")
    # account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # fund_me.withdraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
