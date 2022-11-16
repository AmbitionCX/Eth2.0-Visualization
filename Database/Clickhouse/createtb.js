const clickhouse = require('./clickhouse');
const fs = require('fs');

const beacon_block = fs.readFileSync('./beacon_block.sql').toString();
const attestations = fs.readFileSync('./attestations.sql').toString();
const eth1_block = fs.readFileSync('./eth1_block.sql').toString();

clickhouse.exec({
    query: attestations,
    clickhouse_settings: {
        wait_end_of_query: 1,
    },
})