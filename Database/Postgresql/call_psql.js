const createConnectionPool = require('@databases/pg');
const {sql} = require('@databases/pg');
const axios = require('axios');
require('dotenv').config();

async function connect() {
	const db = createConnectionPool(process.env.POSTGRES_ENDPOINT);
	await db.query(sql.file('./main_table.sql'));
	// let res = await db.query(sql`SELECT f_effective_balance FROM t_validator_balances WHERE f_validator_index=2234 AND f_epoch=80000 LIMIT 10`);
	// console.log(res);
/*	var canonical, block_root;
	for (let i = 1627081; i < 3326600; i++ ){
		let response = await callTekuApi(i);
		if (response.status == "404"){
			canonical = 'f';
			block_root = "NULL";
		} else {
			canonical = response.canonical;
			block_root = response.root;
		}
		await db.query(sql`
			INSERT INTO c_block_status(f_slot, f_canonical, f_block_root)
			VALUES (${i}, ${canonical}, ${block_root})
		`);
	}*/
	await db.dispose();
}

async function callTekuApi(num) {
	const endpoint = 'http://localhost:5051/eth/v2/beacon/blocks/';
	const suffix = '/validator_balances';
	let url = endpoint + num;
	try {
		const response = await axios.get(url);
		return Number(response.data.data.message.body.eth1_data.deposit_count);
	} catch (error) {
		console.log("get error");
		return callTekuApi(num - 1);
	}
}

connect().catch( (err) => {
	console.error(err);
	process.exit(1);
})

// callTekuApi(1).then( (res) => { console.log(res); } );
