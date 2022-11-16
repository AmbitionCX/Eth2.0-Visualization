const createConnectionPool = require('@databases/pg');
const {sql} = require('@databases/pg');
const axios = require('axios');
require('dotenv').config();

const getDepositCount = async (num) => {
	const beacon_blocks = 'http://localhost:5051/eth/v2/beacon/blocks/';
	let url = beacon_blocks + num;
	try {
		const response = await axios.get(url);
		return Number(response.data.data.message.body.eth1_data.deposit_count);
	} catch (error) {
		return getDepositCount(num-1);
	}
}

const getInvalidBlocks = async (epoch) => {
	let start_slot = epoch * 32;
	let stop_slot = start_slot + 32;
	let invalidBlocks = 0;
	const beacon_blocks = 'http://localhost:5051/eth/v1/beacon/headers/';
	for (let i = start_slot; i < stop_slot; i++){
		let url = beacon_blocks + i;
		try{
			let response = await axios.get(url);
		} catch (error) {
			invalidBlocks++;
		}
	}
	return invalidBlocks;
}

async function write_overview() {
	const db = createConnectionPool(process.env.POSTGRES_ENDPOINT);

	// const getInvalidBlocks = async (epoch) => {
	// 	let start_slot = epoch * 32;
	// 	let stop_slot = start_slot + 32;
	// 	let numbers = await db.query(sql`SELECT COUNT(*) FROM c_block_status WHERE f_slot>=${start_slot} AND f_slot<${stop_slot} AND f_canonical IS NOT TRUE`);
	// 	return numbers;
	// }

	for ( let day = 631; day < 633; day++ ){
		let epoch = 0;
		let invalid_blocks = [];
		let deposits = [];
		let start_epoch = day * 225;
		let previous_deposit = 0;
		for (epoch = start_epoch; epoch < start_epoch + 225; epoch++){

			let block_num = await getInvalidBlocks(epoch);
			invalid_blocks.push(Number(block_num));

			let start_slot = epoch * 32;
			let deposit_1 = await getDepositCount(start_slot+8);
			let deposit_2 = await getDepositCount(start_slot+16);
			let deposit_3 = await getDepositCount(start_slot+24);
			let deposit = Math.max(deposit_1,deposit_2,deposit_3);
			if (deposit < previous_deposit) { deposit = previous_deposit; }
			deposits.push(deposit);
			previous_deposit = deposit;
		}

		await db.query(sql`
			INSERT INTO c_overview (f_days, f_blocks, f_deposits)
			VALUES (${day}, ${invalid_blocks}, ${deposits})
		`);

	} // for
	await db.dispose();
}

write_overview().catch( (err) => {
	console.error(err);
	process.exit(1);
})
