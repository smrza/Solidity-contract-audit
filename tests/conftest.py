import pytest
from brownie import chain



### Initialize contract from first account
@pytest.fixture
def D21ContractActive(D21, accounts):
    contract = D21.deploy({'from': accounts[0]})
    return contract

### Initialize and expire contract from first account
@pytest.fixture(scope="module")
def D21ContractExpired(D21, accounts):
    contract = D21.deploy({'from': accounts[0]})
    chain.sleep(604801)
    chain.mine()
    return contract