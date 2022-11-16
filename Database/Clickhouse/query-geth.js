const { ethers } = require("ethers");
require('dotenv').config();

const geth_endpoint = process.env.GETH_ENDPOINT;
const provider = new ethers.providers.JsonRpcProvider(geth_endpoint);

provider.getBlockNumber().then( result => { console.log(result); })