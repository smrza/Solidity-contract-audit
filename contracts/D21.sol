// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;
import "./IVoteD21.sol";

contract D21 is IVoteD21 {
    address immutable owner; 
    uint256 immutable endTime;

    mapping(address => Voter) voters;
    mapping(address => Subject) subjects;
    address[] subjectsAddresses;


    constructor() {
        owner = msg.sender;
        endTime = block.timestamp + 1 weeks;
    }

    // Add a new subject into the voting system using the name.
    function addSubject(string memory _name) external {
        // for some reason does not work without if condition
        if(keccak256(bytes(subjects[msg.sender].name)) != (keccak256(bytes(""))) ){
            require(false, "U have already registered a subject");
        }
        
        subjects[msg.sender] = Subject(_name, 0);
        subjectsAddresses.push(msg.sender);
    }

    // Add a new voter into the voting system
    function addVoter(address addr) external {
        require(msg.sender == owner, "Only owner can give right to vote.");
        voters[addr] = Voter(true, address(0x0), 0);
    }

    // Get addresses of all registered subjects
    function getSubjects() external view returns (address[] memory) {
        require(subjectsAddresses.length > 0, "There is no subject yet");
        return subjectsAddresses;
    }

    // Get the subject details.
    function getSubject(address addr) external view returns (Subject memory){
        require(keccak256(bytes(subjects[addr].name)) != (keccak256(bytes(""))), "There is no registered subject on the given address");
        return subjects[addr];
    }

    // Vote positive for the subject.
    function votePositive(address addr) external {
        require(getRemainingTime() > 0, "Voting time has finished!");  
        require(keccak256(bytes(subjects[addr].name)) != (keccak256(bytes(""))), "There is no registered subject on the given address");
        require(voters[msg.sender].rightToVote, "U dont have right to vote");
        require(voters[msg.sender].firstPositive != addr, "U already voted positively for this subject");
        require(voters[msg.sender].votes < 2, "U already voted positively twice");
        
        voters[msg.sender].firstPositive = addr;
        voters[msg.sender].votes += 1;
        subjects[addr].votes++;
    }

    // Vote negative for the subject.
    function voteNegative(address addr) external {
        require(getRemainingTime() > 0, "Voting time has finished!");   
        require(keccak256(bytes(subjects[addr].name)) != (keccak256(bytes(""))), "There is no registered subject on the given address");
        require(voters[msg.sender].rightToVote, "U dont have right to vote");
        require(voters[msg.sender].votes == 2, "For the permission to vote negatively, U have to vote positively twice, first");
        
        voters[msg.sender].votes++;
        subjects[addr].votes--;
    }

    // Get remaining time to the voting end in seconds.
    function getRemainingTime() public view returns (uint256) {
        require((endTime - block.timestamp) > 0, "Voting time has finished!");
        return (endTime - block.timestamp);
    }
}