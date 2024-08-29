/**
 * @title ContractName
 * @dev ContractDescription
 * @custom:dev-run-script file_path
 */
// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

contract MyContract {
    uint256 public peopleCount = 0;
    uint256 _flag;
    mapping(string => Person) public people;
    mapping(address => Block) public merkletree;

    address owner; // owner is recognized by his address
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    struct Person {
        uint256 peopleCount; // 
        string _name; // aa
        uint256 _reputation; // 6
        string _uniqueID; // ac1
    }

    struct Block {
        string _message; // abc
        uint256 _nonce; // 123
        //uint _reputation;
        string _uniqueID; // ac1
        uint256 _timestamp; // 40
        address _blockAddress; // 0x1234567890123456789012345678901234567890
    }

    //    struct RetrieveBlock {
    //        string _uniqueID;
    //        BlockHash[] _blockhash;
    //    }

    //    struct BlockHash {
    //        address _Address;
    //    }

    constructor() public {
        owner = msg.sender;
    }

    function addPerson(
        string memory _name,
        uint256 _reputation,
        string memory _uniqueID,
        address _blockhash
    ) public onlyOwner {
        // here _blockhash = _blockAddress of addBlock - represents hash of the latest block added by node
        string memory message = "abc";
        string memory uniqueID = "ac1";
        uint256 nonce = 123;
        uint256 reputation = 6;
        uint256 timestamp = 40; //block.timestamp
        bytes32 hash = 0x7465737400000000000000000000000000000000000000000000000000000000;
        string memory secret = "aa";
        //

        // decrypt _h and give values
        _flag = verifyNode(hash, message, uniqueID, nonce, reputation, timestamp);

        //if ((_flag == 1) && (people[_uniqueID]._reputation > 5)) {
        if ((_flag == 1) && (_reputation > 5)) {    
            people[_uniqueID] = Person(
                peopleCount,
                _name,
                _reputation,
                _uniqueID
            );

            //incrementRep(people[_uniqueID]._reputation);
            people[_uniqueID]._reputation = people[_uniqueID]._reputation + 1;
            incrementCount();
        } else {
            //decrementRep(people[_uniqueID]._reputation);
            people[_uniqueID]._reputation = people[_uniqueID]._reputation - 1;
        }
    }

    // add block with zpk
    function addBlock(
        string memory _message,
        uint256 _nonce,
        string memory _uniqueID,
        uint256 _timestamp,
        address _blockAddress // 0x1234567890123456789012345678901234567890
    ) public onlyOwner {
        uint256 _FLAG;

        string memory secret = "aa";
        //string memory pass;
        //_blockAddress = 0x1234567890123456789012345678901234567890
        _FLAG = guessPassword(secret);

        if (_FLAG == 1) {
            merkletree[_blockAddress] = Block(
                _message,
                _nonce,
                _uniqueID,
                _timestamp,
                _blockAddress
            );
        }
    }

    //    function viewBlock (string memory _uniqueID, address _blockAddress) public onlyOwner {
    //
    //    }

    function incrementCount() internal {
        peopleCount += 1;
    }

    //    function computeZPK(string memory _message, string memory _uniqueID, uint _nonce, uint _reputation, uint _timestamp) internal {
    //        bytes32 h = keccak256(_message, _uniqueID, _nonce, _timestamp);
    //        //encrypt E(h, message, uniqueID, nonce, timestamp)
    //    }

    function verifyNode(
        bytes32 h,
        string memory _message,
        string memory _uniqueID,
        uint256 _nonce,
        uint256 _reputation,
        uint256 _timestamp
    //) internal onlyOwner returns (uint256, bytes32) {
    ) internal onlyOwner returns (uint256) {    
        //uint _flag;
        //decrypt D(h, message, uniqueID, nonce, timestamp)

        // assume message is decrypted by base station. So, declare all the values here
        //uint flag = 1;
        string memory message = "abc";
        string memory uniqueID = "ac1";
        uint256 nonce = 123;
        uint256 reputation = 6;
        uint256 timestamp = 40;
        bytes32 h = 0x7465737400000000000000000000000000000000000000000000000000000000;
        //

        //bytes32 _h = keccak256(abi.encodePacked(_message, _uniqueID, _nonce, _timestamp));
        bytes32 _h = 0x7465737400000000000000000000000000000000000000000000000000000000;
        if (h == _h) {
            _flag = 1;
        } else {
            _flag = 0;
        }

        //return (_flag, _h);
        return (_flag);
    }

    // guess password for authentication using ZPK
    function guessPassword(string memory _guessPassword)
        public
        onlyOwner
        returns (uint256)
    {
        string memory _secret = "aa";
        uint256 _FLAG;

        bytes32 _h = keccak256(abi.encodePacked(_secret));
        bytes32 PASS = keccak256(abi.encodePacked(_guessPassword));
        if (PASS == _h) {
            _FLAG = 1;
        } else {
            _FLAG = 0;
        }

        return (_FLAG);
    }

    //    function incrementRep(uint _reputation) internal onlyOwner returns(uint) {
    //        _reputation += 1;  // reputation of only particular device should be changed
    //        return _reputation;
    //    }

    //    function decrementRep(uint _reputation) internal onlyOwner returns(uint) {
    //        _reputation -= 1;  // reputation of only particular device should be changed
    //    }
}
