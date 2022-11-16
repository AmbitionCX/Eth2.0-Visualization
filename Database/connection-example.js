const createConnectionPool = require('@databases/pg');
const {sql} = require('@databases/pg');
const PrometheusQuery = require('prometheus-query');
const dotenv = require('dotenv').config();
const axios = require('axios');

// template connection to Infura Eth2.0 endpoint
var infuraEndPoint = `https://${process.env.PROJECT_ID}:${process.env.PROJECT_SECRET}@eth2-beacon-mainnet.infura.io`;
var infuraApiPath = '/eth/v1/beacon/genesis';
var infuraUrl = infuraEndPoint + infuraApiPath;

async function getRestApi(url) {
	try{
		const response = await axios.get(url);
		console.log(response.data);
	} catch (error) {
		console.log(error);
	}
}

getRestApi(infuraUrl);

// template connection to PostgreSQL on local server
var postgresEndPoint = process.env.POSTGRES_ENDPOINT;
var tempSql = './temp.sql';

async function getPostgreSql(endpoint, action) {
	const postgresDB = createConnectionPool(endpoint);
	const results = await postgresDB.query(sql.file(action));
	console.log(results);
	await postgresDB.dispose();
}

getPostgreSql(postgresEndPoint, tempSql).catch( (err) => {
	console.error(err);
	process.exit(1);
})

// template connection to Prometheus, a real-time streaming database
const prometheusEndPoint = new PrometheusQuery.PrometheusDriver({
	endpoint: "http://localhost:9091",
	baseURL: "/api/v1"
})

const justified_epoch = 'beacon_current_justified_epoch{instance="localhost:8008",job="teku-client"}';
const justified_root = 'beacon_current_justified_root{instance="localhost:8008",job="teku-client"}';
const finalized_epoch = 'beacon_finalized_epoch{instance="localhost:8008",job="teku-client"}';
const finalized_root = 'beacon_finalized_root{instance="localhost:8008",job="teku-client"}';

async function getPrometheus(task) {
	try {
		const responses = await prom.instantQuery(task);
		for (res in responses.result) { console.log(responses.result[res].value.value); }
	} catch (error) {
		console.log(error);
	};
}

getPrometheus(justified_epoch);

