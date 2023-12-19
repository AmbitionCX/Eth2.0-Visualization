CREATE TABLE IF NOT EXISTS c_main_table_1 (
f_epoch integer NOT NULL,
f_slot integer NOT NULL PRIMARY KEY,
f_casper_y integer[],
f_casper_y_balance bigint,
f_casper_n integer[],
f_casper_n_balance bigint,
f_not_vote integer[],
f_not_vote_balance bigint,
f_ghost_selection json
);
