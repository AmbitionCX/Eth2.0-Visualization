CREATE TABLE IF NOT EXISTS eth.attester_slashings
(
    epoch UInt32,
    slot UInt32,
    block_root FixedString(66),

) ENGINE = MergeTree()
ORDER BY (slot)
PRIMARY KEY (slot, block_root)