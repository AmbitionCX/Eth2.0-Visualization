Prometheus中的监控数据有四种数据类型：次数(Counter)，当前值(Gauge)，累计值(Histogram)，总值(Summary)。我们能从Prysm传递给Prometheus的metrics里读取到的数据有如下：

* aggregated_attestations_in_pool_total

* attestation_cache_hit

* attestation_cache_miss

* attestation_cache_size

* attestation_inclusion_delay_slots_bucket

* attestation_inclusion_delay_slots_count

* attestation_inclusion_delay_slots_sum

* attester_slashings_included_total

* bcnode_disk_beaconchain_bytes_total

* beacon_clock_time_slot

* beacon_current_justified_epoch

* beacon_current_justified_root

* beacon_finalized_epoch

* beacon_finalized_root

* beacon_head_slot

* beacon_prev_epoch_active_gwei

* beacon_prev_epoch_head_gwei

* beacon_prev_epoch_source_gwei

  当前值；上一个epoch中，用来给attestation投票的钱，单位是gwei。

* beacon_prev_epoch_target_gwei

* beacon_previous_justified_epoch

* beacon_previous_justified_root

  当前值；

* beacon_reorg_total

* beacon_slot

* beacon_state_count

* beacondb_all_deposits

* beacondb_pending_deposits

* block_arrival_latency_milliseconds_bucket
* block_arrival_latency_milliseconds_count
* block_arrival_latency_milliseconds_sum



本地boltDB相关的参数：

* bolt_bucket_buckets
* bolt_bucket_depth
* bolt_bucket_inlined_buckets
* bolt_bucket_inlined_buckets_in_use_bytes
* bolt_bucket_keys
* bolt_bucket_logical_branch_pages
* bolt_bucket_logical_leaf_pages
* bolt_bucket_physical_branch_overflow_pages
* bolt_bucket_physical_branch_pages_allocated_bytes
* bolt_bucket_physical_branch_pages_in_use_bytes
* bolt_bucket_physical_leaf_overflow_pages
* bolt_bucket_physical_leaf_pages_allocated_bytes
* bolt_bucket_physical_leaf_pages_in_use_bytes
* bolt_db_freelist_free_page_allocated_bytes
* bolt_db_freelist_free_pages
* bolt_db_freelist_in_use_bytes
* bolt_db_freelist_pending_pages
* bolt_db_open_read_tx
* bolt_db_read_tx_total
* bolt_tx_cursors_total
* bolt_tx_node_rebalance_seconds_total
* bolt_tx_node_rebalances_total
* bolt_tx_nodes_allocated_total
* bolt_tx_nodes_dereferenced_total
* bolt_tx_nodes_spilled_seconds_total
* bolt_tx_nodes_spilled_total
* bolt_tx_nodes_split_total
* bolt_tx_pages_allocated_bytes_total
* bolt_tx_pages_allocated_total
* bolt_tx_write_seconds_total
* bolt_tx_writes_total





* check_point_state_cache_hit
* check_point_state_cache_miss
* committee_cache_hit
* committee_cache_miss
* current_eth1_data_deposit_count
* expired_aggregated_atts_total
* expired_block_atts_total
* expired_unaggregated_atts_total



本地运行Prysm的go进程统计：

* go_gc_duration_seconds
* go_gc_duration_seconds_count
* go_gc_duration_seconds_sum
* go_goroutines
* go_info
* go_maxprocs
* go_memstats_alloc_bytes
* go_memstats_alloc_bytes_total
* go_memstats_buck_hash_sys_bytes
* go_memstats_frees_total
* go_memstats_gc_cpu_fraction
* go_memstats_gc_sys_bytes
* go_memstats_heap_alloc_bytes
* go_memstats_heap_idle_bytes
* go_memstats_heap_inuse_bytes
* go_memstats_heap_objects
* go_memstats_heap_released_bytes
* go_memstats_heap_sys_bytes
* go_memstats_last_gc_time_seconds
* go_memstats_lookups_total
* go_memstats_mallocs_total
* go_memstats_mcache_inuse_bytes
* go_memstats_mcache_sys_bytes
* go_memstats_mspan_inuse_bytes
* go_memstats_mspan_sys_bytes
* go_memstats_next_gc_bytes
* go_memstats_other_sys_bytes
* go_memstats_stack_inuse_bytes
* go_memstats_stack_sys_bytes
* go_memstats_sys_bytes
* go_threads





* head_finalized_epoch

  当前值；最新的被确定下来的epoch的编号，一般最近的两个epoch被留作观察，倒数第三个为finalized

* head_finalized_root

* hot_state_cache_hit

* hot_state_cache_miss

* infostream_eth1_blocktime_cache_hits

* infostream_eth1_blocktime_cache_misses

* infostream_eth1_deposit_cache_hits

* infostream_eth1_deposit_cache_misses

  次数；从Eth1.0的deposit合约里，持续的获取validator质押的information。其中缺失的validator的cache

* log_entries_total

* next_slot_cache_hit

* next_slot_cache_miss

* num_pending_attester_slashings

* num_pending_proposer_slashings

* number_of_times_resynced





* p2p_attestation_subnet_attempted_broadcasts
* p2p_attestation_subnet_recovered_broadcasts
* p2p_peer_count
* p2p_repeat_attempts
* p2p_topic_peer_count





* powchain_block_number
* powchain_header_cache_hit
* powchain_header_cache_miss
* powchain_header_cache_size
* powchain_missed_deposit_logs
* powchain_sync_eth1_connected
* powchain_sync_eth1_fallback_configured

* powchain_sync_eth1_fallback_connected

  当前值，当前是否连接着eth1的fallback端口：0=false, 1=true.

* powchain_valid_deposits_received





* process_cpu_seconds_total

* process_max_fds

* process_open_fds

* process_resident_memory_bytes

* process_start_time_seconds

* process_virtual_memory_bytes

* process_virtual_memory_max_bytes

* proposer_indices_cache_hit

* proposer_indices_cache_miss

  次数；对于每个proposer，都会计算一个随即的indices，所有的indices都应该传给beacon chain。

* proposer_slashings_included_total



本地执行Prysm过程中，protocol buffers (serializing structured data)相关的参数

* proto_array_attestation_processed_count
* proto_array_block_processed_count
* proto_array_head_changed_count
* proto_array_head_requested_count
* proto_array_head_slot
* proto_array_node_count
* proto_array_pruned_count





* prysm_version
* replay_blocks_count_bucket
* replay_blocks_count_count
* replay_blocks_count_sum
* scrape_duration_seconds
* scrape_samples_post_metric_relabeling
* scrape_samples_scraped
* scrape_series_added
* skip_slot_cache_hit
* skip_slot_cache_miss
* unaggregated_attestations_in_pool_total
