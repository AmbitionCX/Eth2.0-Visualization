CREATE TABLE IF NOT EXISTS eth.eth1_block
(
    block_number UInt32,
    block_hash FixedString(66),
    parent_hash FixedString(66),
    gas_limit UInt32,
    gas_used UInt32,
    base_fee_per_gas UInt64,
    transactions Array(FixedString(66)),
    `timestamp` DateTime('Asia/Shanghai'),
) ENGINE = MergeTree()
ORDER BY (block_number, block_hash)
PRIMARY KEY (block_number, block_hash)