const PrometheusQuery = require('prometheus-query');
const prom = new PrometheusQuery.PrometheusDriver({
	endpoint: "http://localhost:9091",
	baseURL: "/api/v1"
})

const justified_epoch = 'beacon_current_justified_epoch{instance="localhost:8008",job="teku-client"}';
const justified_root = 'beacon_current_justified_root{instance="localhost:8008",job="teku-client"}';
const finalized_epoch = 'beacon_finalized_epoch{instance="localhost:8008",job="teku-client"}';
const finalized_root = 'beacon_finalized_root{instance="localhost:8008",job="teku-client"}';

prom.instantQuery(justified_epoch).then((res) => {
	const series = res.result;
	series.forEach((serie) => {
		console.log("Value:", serie.value.value);
	});
}).catch(console.error);

async function getProm(task) {
	try {
		const res = await prom.instantQuery(task);
		for (re in res.result) { console.log(res.result[re].value.value); }		
	} catch (error) {
		console.log(error);
	}
}

getProm(justified_epoch);
