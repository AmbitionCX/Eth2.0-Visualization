const createConnectionPool = require('@databases/pg');
const {sql} = require('@databases/pg');
require('dotenv').config();

const db = createConnectionPool(process.env.POSTGRES_ENDPOINT);

const hexLookup = {
  '0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
};

function hexToBinary(string) {
	let binary = '';
	for (let i = 0, len = string.length; i < len; i++) {
		binary += hexLookup[string[i]];
	}
	return binary;
}

function arrayUnique(array) {
	let a = array.concat();
	for(let i = 0; i < a.length; ++i) {
		for(let j = i + 1; j < a.length; ++j) {
			if(a[i] === a[j])	a.splice(j--, 1);
		}
	}
	return a;
}

const getAttestationForSlot = async (slot) => {
	try {
		let attestations = await db.query(sql`SELECT * FROM t_attestations WHERE f_slot=${slot} ORDER BY f_inclusion_index ASC`);
		return attestations;
	} catch (error) {
		return error;
	}
}

const getCanonicalRoot = async (slot) => {
	let root;
	if (slot === 0) {
		const buffered = Buffer.from("4d611d5b93fdab69013a7f0a2f961caca0c853f87cfe9595fe50038163079360", 'hex');
		root = [{f_root: buffered}];
	} else { 
		root = await db.query(sql`SELECT f_root FROM t_blocks WHERE f_slot=${slot}`);
		if (root.length == 0) { root = await getCanonicalRoot(slot - 1); }
	}
	return root;
}

const checkIfHeaderCorrect = async (slot, root) => {
	try {
		let correct_root = await db.query(sql`SELECT f_root FROM t_blocks WHERE f_slot=${slot}`);
		if (root.equals(correct_root[0].f_root)){
			return true;
		} else {
			return false;
		}
	} catch (error) {
		return false;
	}
}

const checkIfTargetCorrect = async (epoch, root) => {
	let checkpoint = epoch * 32;
	let correct_root = await getCanonicalRoot(checkpoint);
	if (root.equals(correct_root[0].f_root)){
		return true;
	} else {
		return false;
	}
}

const getCommittee = async (slot, index) => {
	let committee;
	try {
		committee = await db.query(sql`SELECT f_committee FROM t_beacon_committees WHERE f_slot=${slot} AND f_index=${index}`);
		return committee[0].f_committee;
	} catch (error) {
		return null;
	}
}

const getBalance = async (index, slot) => {
	let balance;
	let epoch = Math.floor(slot/32);
	try {
		let response = await db.query(sql`SELECT f_effective_balance FROM t_validator_balances WHERE f_validator_index=${index} AND f_epoch=${epoch}`);
		balance = response[0].f_effective_balance;
		return balance;
	} catch (error) {
		return 32000000000;
	}
}

const write_main_table = async () => {
	for ( let i = 2187; i < 1000030; i++ ){

		let slot = i;
		let epoch = Math.floor(slot/32);
		
		var casper_y = [];
		var casper_y_balance = 0;
		var casper_n = [];
		var casper_n_balance = 0;
		var not_vote = [];
		var not_vote_balance = 0;
		var ghost_selection = [];
		let committee = [];

		let attestations = await getAttestationForSlot(i);
		if (attestations.length === 0) { continue; }
		
		for (let j = 0; j < attestations.length; j++) {

			let current_attestation = attestations[j];
			let inclusion_slot = current_attestation.f_inclusion_slot;
			let committee_index = current_attestation.f_committee_index;
			// let aggregation_bits = current_attestation.f_aggregation_bits;
			let aggregation_indices = current_attestation.f_aggregation_indices;
			let header_slot = current_attestation.f_slot;
			let header_root = current_attestation.f_beacon_block_root;
			let target_epoch = current_attestation.f_target_epoch;
			let target_root = current_attestation.f_target_root;
			// let isCanonical = current_attestation.f_canonical;
			// let targetCorrect = current_attestation.f_target_correct;
			// let headCorrect = current_attestation.f_head_correct;
			let targetCorrect = await checkIfTargetCorrect(target_epoch, target_root);
			let headCorrect = await checkIfHeaderCorrect(header_slot, header_root);
			let attestation_balance = 0;

			if (committee[committee_index] == null) {
				committee[committee_index] = await getCommittee(i, committee_index);
			}
			// let bits = hexToBinary(aggregation_bits.substring(2));
			for (let k = 0; k < aggregation_indices.length; k++){
				let validator = aggregation_indices[k];
				let validator_balance = 0;
				validator_balance = await getBalance(validator, i);
				if (validator_balance > 32000000000 ) { validator_balance = 32000000000; }
				attestation_balance += validator_balance;

				let index0 = committee[committee_index].indexOf(validator);
				if (index0 > -1) { 
					committee[committee_index].splice(index0, 1);
					if (targetCorrect){
						casper_y.push(validator);
						casper_y_balance += validator_balance;
					} else {
						casper_n.push(validator);
						casper_n_balance += validator_balance;
					}
				}
			}
			let ghost = {
				root: header_root,
				inclusion_slot: inclusion_slot,
				committee_index: committee_index,
				canonical: headCorrect,
				balance: attestation_balance
			};
			ghost_selection.push(ghost);
		}

		not_vote = [].concat.apply([], committee);
		not_vote = arrayUnique(not_vote);
		for (let m = 0; m < not_vote.length; m++) {
			let not_vote_validator = not_vote[m];
			let not_balance = await getBalance(not_vote_validator, i);
			not_vote_balance += not_balance;
		}

		await db.query(sql`
		INSERT INTO s_main_table (f_epoch, f_slot, f_casper_y, f_casper_y_balance, f_casper_n, f_casper_n_balance, f_not_vote, f_not_vote_balance, f_ghost_selection)
		VALUES (${epoch}, ${slot}, ${casper_y}, ${casper_y_balance}, ${casper_n}, ${casper_n_balance}, ${not_vote}, ${not_vote_balance}, ${JSON.stringify(ghost_selection)})
		`);
	} // for
	await db.dispose();
}

write_main_table().catch( (err) => {
	console.error(err);
	process.exit(1);
})
