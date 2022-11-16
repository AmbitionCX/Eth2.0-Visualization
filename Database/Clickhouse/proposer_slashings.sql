CREATE TABLE IF NOT EXISTS eth.proposer_slashings
(
    epoch UInt32,
    slot UInt32,
    block_root FixedString(66),

) ENGINE = MergeTree()
ORDER BY (slot)
PRIMARY KEY (slot, block_root)