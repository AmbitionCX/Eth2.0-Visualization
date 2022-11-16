CREATE TABLE IF NOT EXISTS eth.beacon_block
(
    slot UInt32,
    proposer_index UInt32,
    block_root FixedString(66),
    is_canonical Bool,
    state_root FixedString(66),
    parent_root FixedString(66),
    parent_slot UInt32,
    eth1_block_hash FixedString(66),
    eth1_deposit_count UInt32,
    eth1_deposit_root FixedString(66),
) ENGINE = MergeTree()
ORDER BY (slot, block_root)
PRIMARY KEY (slot, block_root)
