const createConnectionPool = require('@databases/pg');
const {sql} = require('@databases/pg');
const axios = require('axios');
require('dotenv').config();

const endpoint = 'http://localhost:5051/eth/v1/beacon/headers/';

async function connect() {
	const db = createConnectionPool(process.env.POSTGRES_ENDPOINT);
	// const results = await db.query(sql.file('./createTb.sql'));
	var canonical, block_root;
	for (let i = 3435500; i < 3438900; i++ ){
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
	}
	await db.dispose();
}

async function callTekuApi(num) {
	try {
		let url = endpoint + num;
		const response = await axios.get(url);
		return response.data.data;
	} catch (error) {
		return error.response.data;
	}
}

connect().catch( (err) => {
	console.error(err);
	process.exit(1);
})