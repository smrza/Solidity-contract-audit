// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

interface IVoteD21 {
    struct Voter {
        bool rightToVote;
        address firstPositive; 
        uint8 votes;
    }

    struct Subject {
        string name;
        int256 votes;
    }

    // Add a new subject into the voting system using the name.
    function addSubject(string memory name) external;

    // Add a new voter into the voting system
    function addVoter(address addr) external;

    // Get addresses of all registered subjects
    function getSubjects() external view returns (address[] memory);

    // Get the subject details.
    function getSubject(address addr) external view returns (Subject memory);

    // Vote positive for the subject.
    function votePositive(address addr) external;

    // Vote negative for the subject.
    function voteNegative(address addr) external;

    // Get remaining time to the voting end in seconds.
    function getRemainingTime() external view returns (uint256);
}