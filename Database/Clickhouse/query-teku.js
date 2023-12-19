const clickhouse = require('./clickhouse');
const axios = require('axios');
require('dotenv').config();

const teku_endpoint = process.env.TEKU_ENDPOINT;

async function getBeaconBlock(block_num) {
	const api = '/eth/v2/beacon/blocks/';
	let url = teku_endpoint + api + block_num;
	try {
		const response = await axios.get(url);
		return response.data.data.message;
	} catch (error) {
		// console.log(error);
		return null;
	}
}

async function getBeaconHeader(block_num) {
	const api = '/eth/v1/beacon/headers/';
	let url = teku_endpoint + api + block_num;
	try {
		const response = await axios.get(url);
		return response.data.data;
	} catch (error) {
		// console.log(error);
		return null;
	}
}

const write_teku_block = async () => {
	for ( let i = 5140000; i < 5141000; i++ ){

        let block_header = await getBeaconHeader(i);
		if (block_header == null) { continue; }
        let block_root = block_header.root;
		let is_canonical = block_header.canonical;

		let block_data = await getBeaconBlock(i);
		let slot = block_data.slot;
		let proposer_index = block_data.proposer_index;
		let state_root = block_data.state_root;
        let parent_root = block_data.parent_root;
        let eth1_block_hash = block_data.body.eth1_data.block_hash;
        let eth1_deposit_count = block_data.body.eth1_data.deposit_count;
        let eth1_deposit_root = block_data.body.eth1_data.deposit_root;
		let attestations_data = block_data.body.attestations;

		let parent_block = await getBeaconHeader(parent_root);
		let parent_slot = parent_block.header.message.slot;

		let attestations_value = [];
		for (let j = 0; j < attestations_data.length; j++){
			let ats = {
				"inclusion_slot": slot,
				"inclusion_block_root": block_root,
				"inclusion_index": j,
				"slot": attestations_data[j].data.slot,
				"committee_index": attestations_data[j].data.index,
				"aggregation_bits": attestations_data[j].aggregation_bits,
				"beacon_block_root": attestations_data[j].data.beacon_block_root,
				"source_epoch": attestations_data[j].data.source.epoch,
				"source_root": attestations_data[j].data.source.root,
				"target_epoch": attestations_data[j].data.target.epoch,
				"target_root": attestations_data[j].data.target.root,
			};
			attestations_value.push(ats);
		}

        let beacon_block_value = [{
            "slot": slot,
            "proposer_index": proposer_index,
            "block_root": block_root,
            "is_canonical": is_canonical,
            "state_root": state_root,
            "parent_root": parent_root,
            "parent_slot": parent_slot,
            "eth1_block_hash": eth1_block_hash,
			"eth1_deposit_count": eth1_deposit_count,
			"eth1_deposit_root": eth1_deposit_root,
        }]

        await clickhouse.insert({
            table: 'eth.beacon_block',
            values: beacon_block_value,
            format: 'JSONEachRow',
            clickhouse_settings: {
                wait_end_of_query: 1,
            },
        })

		await clickhouse.insert({
            table: 'eth.attestations',
            values: attestations_value,
            format: 'JSONEachRow',
            clickhouse_settings: {
                wait_end_of_query: 1,
            },
        })
    }
}

const read_beacon_block = async () => {
    let query_data = await clickhouse.query({
        query: 'select * from eth.beacon_block limit 1',
        format: 'JSONEachRow',
    });
    let beacon_block_data = await query_data.json();
    return beacon_block_data;
}


read_beacon_block()
.then( result => console.log(result) )
.catch( (err) => {
	console.error(err);
	process.exit(1);
})