const clickhouse = require('./clickhouse');
const axios = require('axios');
require('dotenv').config();

const teku_endpoint = process.env.TEKU_ENDPOINT;

async function callTekuApi() {

	const api = '/eth/v1/beacon/genesis';
	let url = teku_endpoint + api;
	try {
		const response = await axios.get(url);
		return response.data.data;
	} catch (error) {
		console.log(error);
	}
}

callTekuApi().then( result => { console.log(result); } )