#include "imports/stdlib.tact";

// AetherGovernance - 48h Timelock with community voting
@name("AetherGovernance")
@interface("AetherGovernanceInterface") {

    // Governance state
    proposals: map<Int, Cell>;
    proposalCounter: Int;
    
    // Voting parameters
    votingPeriod: Int;
    timelockPeriod: Int;
    
    // Token balances for voting
    tokenBalances: map<Address, Int>;
    
    // Received messages
    receive(msg: Cell) = {
        // Parse incoming message
        let cs = msg.begin_parse();
        let op = cs.load_uint(8);
        
        // Handle different operations
        if (op == 0x1) { // Create proposal
            return self.handle_create_proposal(cs);
        } else if (op == 0x2) { // Vote on proposal
            return self.handle_vote(cs);
        } else if (op == 0x3) { // Execute proposal
            return self.handle_execute(cs);
        }
        
        // Default: return error
        return begin_cell()
            .store_uint(0xFF, 8) // Error code
            .end_cell();
    }
    
    // Create new proposal
    handle_create_proposal(cs: Slice) = {
        let title = cs.load_string(256);
        let description = cs.load_string(1024);
        let target = cs.load_msg_addr();
        let value = cs.load_coins();
        let payload = cs.load_ref();
        
        // Create proposal
        let proposalId = self.proposalCounter + 1;
        let proposal = begin_cell()
            .store_string(title)
            .store_string(description)
            .store_slice(target)
            .store_coins(value)
            .store_ref(payload)
            .store_uint(now(), 64) // Created at
            .store_uint(0, 64) // Executed at
            .store_uint(0, 32) // Votes for
            .store_uint(0, 32) // Votes against
            .store_bool(false) // Executed
            .end_cell();
        
        self.proposals.set(proposalId, proposal);
        self.proposalCounter = proposalId;
        
        return begin_cell()
            .store_uint(0x01, 8) // Success
            .store_uint(proposalId, 32)
            .end_cell();
    }
    
    // Vote on proposal
    handle_vote(cs: Slice) = {
        let proposalId = cs.load_uint(32);
        let vote = cs.load_uint(8); // 1 = for, 2 = against
        let voter = cs.load_msg_addr();
        let votingPower = cs.load_uint(64);
        
        // Get proposal
        let proposalOpt = self.proposals.get(proposalId);
        if (proposalOpt == null) {
            return begin_cell()
                .store_uint(0x02, 8) // Proposal not found
                .end_cell();
        }
        
        let proposal = proposalOpt.begin_parse();
        let title = proposal.load_string(256);
        let description = proposal.load_string(1024);
        let target = proposal.load_msg_addr();
        let value = proposal.load_coins();
        let payload = proposal.load_ref();
        let createdAt = proposal.load_uint(64);
        let executedAt = proposal.load_uint(64);
        let votesFor = proposal.load_uint(32);
        let votesAgainst = proposal.load_uint(32);
        let executed = proposal.load_bool();
        
        // Check if voting period is active
        let nowTime = now();
        if (nowTime - createdAt > self.votingPeriod) {
            return begin_cell()
                .store_uint(0x03, 8) // Voting period ended
                .end_cell();
        }
        
        // Update vote counts
        if (vote == 1) {
            votesFor = votesFor + votingPower;
        } else if (vote == 2) {
            votesAgainst = votesAgainst + votingPower;
        }
        
        // Update proposal
        let updatedProposal = begin_cell()
            .store_string(title)
            .store_string(description)
            .store_slice(target)
            .store_coins(value)
            .store_ref(payload)
            .store_uint(createdAt, 64)
            .store_uint(executedAt, 64)
            .store_uint(votesFor, 32)
            .store_uint(votesAgainst, 32)
            .store_bool(executed)
            .end_cell();
        
        self.proposals.set(proposalId, updatedProposal);
        
        return begin_cell()
            .store_uint(0x04, 8) // Success
            .store_uint(proposalId, 32)
            .store_uint(votesFor, 32)
            .store_uint(votesAgainst, 32)
            .end_cell();
    }
    
    // Execute proposal
    handle_execute(cs: Slice) = {
        let proposalId = cs.load_uint(32);
        
        // Get proposal
        let proposalOpt = self.proposals.get(proposalId);
        if (proposalOpt == null) {
            return begin_cell()
                .store_uint(0x05, 8) // Proposal not found
                .end_cell();
        }
        
        let proposal = proposalOpt.begin_parse();
        let title = proposal.load_string(256);
        let description = proposal.load_string(1024);
        let target = proposal.load_msg_addr();
        let value = proposal.load_coins();
        let payload = proposal.load_ref();
        let createdAt = proposal.load_uint(64);
        let executedAt = proposal.load_uint(64);
        let votesFor = proposal.load_uint(32);
        let votesAgainst = proposal.load_uint(32);
        let executed = proposal.load_bool();
        
        // Check if already executed
        if (executed) {
            return begin_cell()
                .store_uint(0x06, 8) // Already executed
                .end_cell();
        }
        
        // Check voting results
        if (votesFor <= votesAgainst) {
            return begin_cell()
                .store_uint(0x07, 8) // Proposal rejected
                .end_cell();
        }
        
        // Check timelock
        let nowTime = now();
        if (nowTime - createdAt < self.timelockPeriod) {
            return begin_cell()
                .store_uint(0x08, 8) // Timelock not expired
                .end_cell();
        }
        
        // Mark as executed
        let executedProposal = begin_cell()
            .store_string(title)
            .store_string(description)
            .store_slice(target)
            .store_coins(value)
            .store_ref(payload)
            .store_uint(createdAt, 64)
            .store_uint(nowTime, 64)
            .store_uint(votesFor, 32)
            .store_uint(votesAgainst, 32)
            .store_bool(true)
            .end_cell();
        
        self.proposals.set(proposalId, executedProposal);
        
        return begin_cell()
            .store_uint(0x09, 8) // Success
            .store_slice(target)
            .store_coins(value)
            .store_ref(payload)
            .end_cell();
    }
    
    // Get proposal
    get_proposal(proposalId: Int) = {
        return self.proposals.get(proposalId);
    }
    
    // Get all proposals
    get_all_proposals() = {
        return begin_cell()
            .store_dict(self.proposals)
            .end_cell();
    }
}

// Constructor
constructor() = {
    // Initialize governance
    self.proposals = empty_map();
    self.proposalCounter = 0;
    self.votingPeriod = 7 * 24 * 60 * 60; // 7 days
    self.timelockPeriod = 2 * 24 * 60 * 60; // 48 hours
    self.tokenBalances = empty_map();
}
