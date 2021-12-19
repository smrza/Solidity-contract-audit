import brownie
import pytest



### addSubject
# U1
# Add 3 subjects
def test_addSubject_anyone(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test1", {'from': accounts[1]})
    D21ContractActive.addSubject("Test2", {'from': accounts[2]})
    D21ContractActive.addSubject("Test3", {'from': accounts[3]})
    assert D21ContractActive.getSubject(accounts[1])[0] == "Test1", "Wrong subject name."
    assert D21ContractActive.getSubject(accounts[2])[0] == "Test2", "Wrong subject name."
    assert D21ContractActive.getSubject(accounts[3])[0] == "Test3", "Wrong subject name."
    assert D21ContractActive.getSubject(accounts[1])[1] == 0, "Subject is supposed to have 0 votes by default."
    assert D21ContractActive.getSubject(accounts[2])[1] == 0, "Subject is supposed to have 0 votes by default."
    assert D21ContractActive.getSubject(accounts[3])[1] == 0, "Subject is supposed to have 0 votes by default."
    assert accounts[1] in D21ContractActive.getSubjects(), "Subject address was not found in subjectsAddresses"
    assert accounts[2] in D21ContractActive.getSubjects(), "Subject address was not found in subjectsAddresses"
    assert accounts[3] in D21ContractActive.getSubjects(), "Subject address was not found in subjectsAddresses"

# U2
# Add a subject from the same account
def test_addSubject_same(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test", {'from': accounts[1]})
    assert D21ContractActive.getSubject(accounts[1])[0] == "Test", "Wrong subject name."
    assert D21ContractActive.getSubject(accounts[1])[1] == 0, "Subject is supposed to have 0 votes by default."
    assert accounts[1] in D21ContractActive.getSubjects(), "Subject address was not found in subjectsAddresses"
    with brownie.reverts("U have already registered a subject"):
        D21ContractActive.addSubject("Test", {'from': accounts[1]})

# BUG
# U3
# Add subject after elections end
def test_addSubject_expired(D21ContractExpired, accounts):
    D21ContractExpired.addSubject("Test", {'from': accounts[1]})
    assert D21ContractExpired.getSubject(accounts[1])[0] == "Test", "Wrong subject name."
    assert D21ContractExpired.getSubject(accounts[1])[1] == 0, "Subject is supposed to have 0 votes by default."
    assert accounts[1] in D21ContractExpired.getSubjects(), "Subject address was not found in subjectsAddresses"



### addVoter
# U4
# Adding voter from owner
def test_addVoter_owner(D21ContractActive, accounts):
    D21ContractActive.addVoter(accounts[1], {'from': accounts[0]})
    D21ContractActive.addVoter(accounts[2], {'from': accounts[0]})
    D21ContractActive.addVoter(accounts[3], {'from': accounts[0]})

# U5
# Adding voter from nonOwner
def test_addVoter_nonOwner(D21ContractActive, accounts):
    with brownie.reverts("Only owner can give right to vote."):
        D21ContractActive.addVoter(accounts[1], {'from': accounts[1]})
    with brownie.reverts("Only owner can give right to vote."):
        D21ContractActive.addVoter(accounts[2], {'from': accounts[2]})
    with brownie.reverts("Only owner can give right to vote."):
        D21ContractActive.addVoter(accounts[3], {'from': accounts[3]})

# BUG
# U6
# Adding a voter already registered, thus resetting their vote count
# Owner can reset their own vote count or reset votes of a friend
def test_addVoter_readd(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test1", {'from': accounts[1]})
    D21ContractActive.addSubject("Test2", {'from': accounts[2]})
    D21ContractActive.addSubject("Test3", {'from': accounts[3]})
    D21ContractActive.addVoter(accounts[0], {'from': accounts[0]})
    D21ContractActive.addVoter(accounts[4], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[4]})
    D21ContractActive.votePositive(accounts[2], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[2], {'from': accounts[4]})
    D21ContractActive.voteNegative(accounts[3], {'from': accounts[0]})
    D21ContractActive.voteNegative(accounts[3], {'from': accounts[4]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 2, "Subject is supposed to have 2 votes."
    assert D21ContractActive.getSubject(accounts[2])[1] == 2, "Subject is supposed to have 2 votes."
    assert D21ContractActive.getSubject(accounts[3])[1] == -2, "Subject is supposed to have -2 votes."
    D21ContractActive.addVoter(accounts[0], {'from': accounts[0]})
    D21ContractActive.addVoter(accounts[4], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[4]})
    D21ContractActive.votePositive(accounts[2], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[2], {'from': accounts[4]})
    D21ContractActive.voteNegative(accounts[3], {'from': accounts[0]})
    D21ContractActive.voteNegative(accounts[3], {'from': accounts[4]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 4, "Subject is supposed to have 4 votes."
    assert D21ContractActive.getSubject(accounts[2])[1] == 4, "Subject is supposed to have 4 votes."
    assert D21ContractActive.getSubject(accounts[3])[1] == -4, "Subject is supposed to have -4 votes."

# BUG
# U7
# Adding voter after elections have ended
def test_addVoter_expired(D21ContractExpired, accounts):
    D21ContractExpired.addVoter(accounts[1], {'from': accounts[0]})
    D21ContractExpired.addVoter(accounts[2], {'from': accounts[0]})
    D21ContractExpired.addVoter(accounts[3], {'from': accounts[0]})



### getSubjects
# U8
# Get subjects if there are none registered yet
def test_getSubjects_empty(D21ContractActive, accounts):
    with brownie.reverts("There is no subject yet"):
        D21ContractActive.getSubjects({'from': accounts[0]})

# U9
# Get registered subjects
def test_getSubjects_registered(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test1", {'from': accounts[1]})
    D21ContractActive.addSubject("Test2", {'from': accounts[2]})
    D21ContractActive.addSubject("Test3", {'from': accounts[3]})
    subjects = D21ContractActive.getSubjects()
    assert subjects[0] == accounts[1], "Wrong subject address."
    assert subjects[1] == accounts[2], "Wrong subject address."
    assert subjects[2] == accounts[3], "Wrong subject address."



### getSubject
# U10
# Get a non registered subject
def test_getSubject_empty(D21ContractActive, accounts):
    with brownie.reverts("There is no registered subject on the given address"):
        D21ContractActive.getSubject(accounts[0], {'from': accounts[0]})

# U11
# Get a registered subject
def test_getSubject_registered(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test", {'from': accounts[0]})
    subject = D21ContractActive.getSubject(accounts[0])
    assert subject[0] == "Test", "Wrong subject name."
    assert subject[1] == 0, "Subject is supposed to have 0 votes by default."



### votePositive
# BUG
# U12
# Vote positive integer error
def test_votePositive_expired(D21ContractExpired, accounts):
    with brownie.reverts("Integer overflow"):
        D21ContractExpired.votePositive(accounts[0], {'from': accounts[9]})

# U13
def test_votePositive_expired_v2(D21ContractExpired, accounts):
    with pytest.raises(brownie.exceptions.VirtualMachineError):
        assert D21ContractExpired.votePositive(accounts[0], {'from': accounts[9]}), "This is supposed to fail."

# U14        
#Vote positive for a non registered subject
def test_votePositive_nonRegistered(D21ContractActive, accounts):
    with brownie.reverts("There is no registered subject on the given address"):
        D21ContractActive.votePositive(accounts[0], {'from': accounts[1]})

# U15
#Vote positive from an account which does not have a right to vote
def test_votePositive_noRightToVote(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test", {'from': accounts[1]})
    with brownie.reverts("U dont have right to vote"):
        D21ContractActive.votePositive(accounts[1], {'from': accounts[0]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 0, "Subject should still have 0 votes."

# U16
#Vote positive successfully
def test_votePositive_success(D21ContractActive, accounts):
    D21ContractActive.addVoter(accounts[1], {'from': accounts[0]})
    D21ContractActive.addSubject("Test", {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[0], {'from': accounts[1]})
    assert D21ContractActive.getSubject(accounts[0])[1] == 1, "Subject should have 1 votes."

# U17
#Vote positive for the same subject
def test_votePositive_sameSubject(D21ContractActive, accounts):
    D21ContractActive.addVoter(accounts[1], {'from': accounts[0]})
    D21ContractActive.addSubject("Test", {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[0], {'from': accounts[1]})
    with brownie.reverts("U already voted positively for this subject"):
        D21ContractActive.votePositive(accounts[0], {'from': accounts[1]})
    assert D21ContractActive.getSubject(accounts[0])[1] == 1, "Subject should still have 1 votes."

# U18
#Vote positive more than twice
def test_votePositive_moreThanTwice(D21ContractActive, accounts):
    D21ContractActive.addVoter(accounts[1], {'from': accounts[0]})
    D21ContractActive.addSubject("Test1", {'from': accounts[3]})
    D21ContractActive.addSubject("Test2", {'from': accounts[4]})
    D21ContractActive.addSubject("Test3", {'from': accounts[5]})
    D21ContractActive.votePositive(accounts[3], {'from': accounts[1]})
    D21ContractActive.votePositive(accounts[4], {'from': accounts[1]})
    with brownie.reverts("U already voted positively twice"):
        D21ContractActive.votePositive(accounts[5], {'from': accounts[1]})
    assert D21ContractActive.getSubject(accounts[5])[1] == 0, "Subject should still have 0 votes."



### voteNegative
# BUG
# U19
# Vote negative integer error
def test_voteNegative_expired(D21ContractExpired, accounts):
    with brownie.reverts("Integer overflow"):
        D21ContractExpired.voteNegative(accounts[0], {'from': accounts[9]})

# U20
def test_voteNegative_expired_v2(D21ContractExpired, accounts):
    with pytest.raises(brownie.exceptions.VirtualMachineError):
        assert D21ContractExpired.voteNegative(accounts[0], {'from': accounts[9]}), "This is supposed to fail."

# U21
# Vote negative for a non registered subject
def test_voteNegative_nonRegistered(D21ContractActive, accounts):
    with brownie.reverts("There is no registered subject on the given address"):
        D21ContractActive.voteNegative(accounts[1], {'from': accounts[0]})

# U22
# Vote negative from an account which does not have the right to vote
def test_voteNegative_noRightToVote(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test", {'from': accounts[1]})
    with brownie.reverts("U dont have right to vote"):
        D21ContractActive.voteNegative(accounts[1], {'from': accounts[9]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 0, "Subject should still have 0 votes."

# U23
# Vote negative sooner than voting positive twice
def test_voteNegative_noTwoPositiveVotes(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test", {'from': accounts[1]})
    D21ContractActive.addVoter(accounts[1], {'from': accounts[0]})
    with brownie.reverts("For the permission to vote negatively, U have to vote positively twice, first"):
        D21ContractActive.voteNegative(accounts[1], {'from': accounts[1]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 0, "Subject should still have 0 votes."

# U24
# Vote negative successfully
def test_voteNegative_success(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test1", {'from': accounts[1]})
    D21ContractActive.addSubject("Test2", {'from': accounts[2]})
    D21ContractActive.addSubject("Test3", {'from': accounts[3]})
    D21ContractActive.addVoter(accounts[0], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[2], {'from': accounts[0]})
    D21ContractActive.voteNegative(accounts[3], {'from': accounts[0]})
    assert D21ContractActive.getSubject(accounts[3])[1] == -1, "Subject should have -1 votes."

# U25
# Vote negative twice
def test_voteNegative_twice(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test1", {'from': accounts[1]})
    D21ContractActive.addSubject("Test2", {'from': accounts[2]})
    D21ContractActive.addSubject("Test3", {'from': accounts[3]})
    D21ContractActive.addVoter(accounts[0], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[2], {'from': accounts[0]})
    D21ContractActive.voteNegative(accounts[3], {'from': accounts[0]})
    with brownie.reverts("For the permission to vote negatively, U have to vote positively twice, first"):
        D21ContractActive.voteNegative(accounts[3], {'from': accounts[0]})
    assert D21ContractActive.getSubject(accounts[3])[1] == -1, "Subject should still have -1 votes."

# U26
# Vote negative for subject already voted positive for
def test_voteNegative_sameSubject(D21ContractActive, accounts):
    D21ContractActive.addSubject("Test1", {'from': accounts[1]})
    D21ContractActive.addSubject("Test2", {'from': accounts[2]})
    D21ContractActive.addVoter(accounts[0], {'from': accounts[0]})
    D21ContractActive.votePositive(accounts[1], {'from': accounts[0]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 1, "Subject should have 1 votes."
    D21ContractActive.votePositive(accounts[2], {'from': accounts[0]})
    D21ContractActive.voteNegative(accounts[1], {'from': accounts[0]})
    assert D21ContractActive.getSubject(accounts[1])[1] == 0, "Subject should have 0 votes."



### getRemainingTime
# U27
# Get remaining time successfully
def test_getRemainingTime_success(D21ContractActive, accounts):
    D21ContractActive.getRemainingTime({'from': accounts[0]})

# BUG
# U28
# Get remaining integer error
def test_getRemainingTime_fail(D21ContractExpired, accounts):
    with pytest.raises(brownie.exceptions.VirtualMachineError):
        assert D21ContractExpired.getRemainingTime({'from': accounts[1]}), "This is supposed to fail."



### Tests bounds to fail
# U29
# Get remaining time, fail
def test_getRemainingTime_boundToFail(D21ContractExpired, accounts):
    D21ContractExpired.getRemainingTime({'from': accounts[0]})

# U30
# Vote negative expired, fail
def test_voteNegative_fail(D21ContractExpired, accounts):
    D21ContractExpired.voteNegative(accounts[0], {'from': accounts[9]})
# U31
# Vote positive expired, fail
def test_votePositive_fail(D21ContractExpired, accounts):
    D21ContractExpired.votePositive(accounts[0], {'from': accounts[9]})