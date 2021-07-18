Prometheus中的监控数据有四种数据类型：次数(Counter)，当前值(Gauge)，累计值(Histogram)，总值(Summary)。我们能从Prysm传递给Prometheus的metrics里读取到的数据有如下：（boltDB和go相关的参数对可视化无益，忽略）
* attestation_cache_hit
  当前值；attestation缓存大小
* attestation_cache_miss
  当前值；缺失的attestation缓存大小
* attestation_inclusion_delay_slots
  累计值；attestation block的slot和当前最新的block slot之间的差值 
* attester_slashings_included_total
  次数；block中的slashing数量
* bcnode_disk_beaconchain_bytes_total
  当前值；Beacon chain的本地节点的数据库使用的硬盘存储空间（bytes）
* beacon_clock_time_slot
  累计值；根据初始时间和当前的时间计算出来的当前slot
* beacon_current_justified_epoch
  当前值；Beacon chain现在最新的justified的epoch
* beacon_current_justified_root
  当前值；Beacon chain现在最新的justified的root
* beacon_finalized_epoch
  当前值；Beacon chain现在最新的finalized的epoch
* beacon_finalized_root
  当前值；Beacon chain现在最新的finalized的root
* beacon_head_slot
  当前值；最新block的slot值
* beacon_prev_epoch_active_gwei
  当前值；上一个epoch中，所有“活跃”的钱，单位是gwei。
* beacon_prev_epoch_head_gwei
  当前值；上一个epoch中，用来给attestation head投票的钱，单位是gwei。
* beacon_prev_epoch_source_gwei
  当前值；上一个epoch中，用来给attestation source投票的钱，单位是gwei。
* beacon_prev_epoch_target_gwei
  累计值；上一个epoch中，用来给attestation target投票的钱，单位是gwei。
* beacon_previous_justified_epoch
  当前值；上一次justified的block位于哪个epoch
* beacon_previous_justified_root
  当前值；当一个epoch结束的时候，如果它的checkpoint(该epoch的第一个block)获得了2/3以上的同意，那这个checkpoint就被justified，这个参数记录了上一次justified的block的state root
* beacon_reorg_total
  次数；beacon chain发生reorganization的次数
* beacon_slot
  当前值；最新的slot
* beacon_state_count
  当前值；beacon chain里的state对象数量
* beacondb_all_deposits
  次数；beaconDB指的是beacon chain的“数据库”或者“共识”，同步于所有运行beacon chain的设备上的memory中，而不是指某一个具体设备上的数据库。这个参数指的是所有质押的Ether数量。
* beacondb_pending_deposits
  次数；这个参数指的是所有pending的Ether数量（向Eth1.0的合约提交了，但还没被Eth2.0捕捉到）
* block_arrival_latency_milliseconds
  累计值；block的传播时间（ms），从block生成，到传播到我们的节点所用的时间


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
  次数；beacon chain的cache中，存在的checkpoint的数量
* check_point_state_cache_miss
  次数；beacon chain的cache中，缺少的checkpoint的数量
* committee_cache_hit
  次数；committee的缓存数量
* committee_cache_miss
  次数；committee的缓存缺少的次数
* current_eth1_data_deposit_count
  当前值；Eth1.0合约里，质押的人数
* expired_aggregated_atts_total
  次数；因为过期而被删除的打包的attestation数量
* expired_block_atts_total
  次数；我们这个节点里，过期的，被删掉的attestations的数量
* expired_unaggregated_atts_total
  次数；因为过期而被删除调的，没有打包的attestation数量


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
  当前值；最新的被确定下来的head state root
* hot_state_cache_hit
  The total number of cache hits on the hot state cache.
* hot_state_cache_miss
  The total number of cache misses on the hot state cache.
* infostream_eth1_blocktime_cache_hits
  次数；Eth1.0的区块的blocktime会发送给Eth2.0的客户端，这个参数代表了成功发送的次数。
* infostream_eth1_blocktime_cache_misses
  次数；blocktime没有成功发送的次数。
* infostream_eth1_deposit_cache_hits
  次数；从Eth1.0的deposit合约里，持续的获取validator质押的information。其中成功接收的validator的cache的数量
* infostream_eth1_deposit_cache_misses
  次数；缺失的validator的cache的数量
* log_entries_total
  次数；log里message的数量
* next_slot_cache_hit
  次数；对于下一个slot，生成（并经过验证）的block state cache的数量
* next_slot_cache_miss
  次数；对于下一个slot，缺少的block state cache的数量
* num_pending_attester_slashings
  当前值；节点中，排队等待中的对于attester的slashings的数量
* num_pending_proposer_slashings
  当前值；节点中，排队等待中的对于proposer的slashings的数量
* number_of_times_resynced
  次数；我们这个节点重新同步的次数。重新同步可能因为节点下线，或者同步错误。


* p2p_attestation_subnet_attempted_broadcasts
  次数；尝试广播的attestation的数量
* p2p_attestation_subnet_recovered_broadcasts
  次数；一个节点广播attestation，但是没有一个peer可以接收到他广播的信息，attestation就会被重复广播直到某个peer接收到。这个参数表示了重复的次数
* p2p_peer_count
  当前值；我们这个Eth2.0的节点的peer数量，和Eth1.0的概念一样。
* p2p_repeat_attempts
  次数；尝试连接peer的次数
* p2p_topic_peer_count
  当前值；订阅某个topic的peer的数量


* powchain_block_number
  Eth1.0当前的block number
* powchain_header_cache_hit
  次数；从Eth1.0的block header发送出去的请求（调用质押合约而触发的请求）被接收到的数量
* powchain_header_cache_miss
  次数；从Eth1.0的block header发送出去的请求没有被接收的数量
* powchain_header_cache_size
  当前值；Eth1.0的header缓存数量
* powchain_missed_deposit_logs
  次数；察觉到的（Eth1.0上发送来的）缺失的质押的数量
* powchain_sync_eth1_connected
  当前值；当前是否连接着Eth1.0节点
* powchain_sync_eth1_fallback_configured
  当前值；当前是否配置了eth1的fallback端口，我设置了一个infura端口作为fallback endpoint。
* powchain_sync_eth1_fallback_connected
  当前值；当前是否连接着eth1的fallback端口：0=false, 1=true。
* powchain_valid_deposits_received
  次数；Eth1.0的合约里，收到的合法的质押数量


* process_cpu_seconds_total
  次数；总计的system和user的CPU time（seconds）
* process_max_fds
  当前值；最多能够创建的file descriptors的数量
* process_open_fds
  当前值；当前创建的file descriptors的数量
* process_resident_memory_bytes
  当前值；占用的内存空间
* process_start_time_seconds
  当前值；Prysm启动的时候的unix time
* process_virtual_memory_bytes
  当前值；目前正在使用中的虚拟内存的数量（bytes）
* process_virtual_memory_max_bytes
  当前值；最多能使用的虚拟内存的数量（bytes）

* proposer_indices_cache_hit
  次数；对于每个proposer，都会计算一个随即的indices，所有的indices都应该传给beacon chain。beacon chain收到的proposer信息的数量
* proposer_indices_cache_miss
  次数；beacon chain缺失的proposer信息的数量
* proposer_slashings_included_total
  次数；区块中，关于proposer的slashing数量
  

本地执行Prysm过程中，protocol buffers (serializing structured data)相关的参数
* proto_array_attestation_processed_count
  次数；我们这个节点通过attestation来检查是否有分叉的次数。
* proto_array_block_processed_count
  次数；一个block被执行查看fork choice的次数（如果某个block有不同的意见，就有可能因此而产生分叉，beacon chain要选择其中一个，防止分叉）
* proto_array_head_changed_count
  次数；一个block header被改变的次数
* proto_array_head_requested_count
  次数；一个block被请求查看的次数
* proto_array_head_slot
  当前值；当前head的slot number
* proto_array_node_count
  The number of nodes in the DAG array based store structure.
  

* prysm_version
* replay_blocks_count_count
  累计值；当前需要重新回访来生成state的区块数量
* skip_slot_cache_hit
  次数；被跳过的slot（没有达成共识），获得的缓存
* skip_slot_cache_miss
  次数；被跳过的slot（没有达成共识），缺失的缓存
* aggregated_attestations_in_pool_total
  当前值；在同一个committee中的validator，作出的votes，可以被aggregated（打包）成一个签名，这是一个优化措施。这个参数表达了被打包的attestation的数量。
* unaggregated_attestations_in_pool_total
  当前值；没有被打包的attestation的数量。
* validator_count
  当前值；validator的数量
* validators_total_balance
  当前值；所有validator的总的余额（GWei）
* validators_total_effective_balance
  当前值；validator的总的可以生效的钱的数量（GWei）


其中，重要的参数有:

参与者数据：

* Current epoch: beacon_current_justified_epoch
* Finalized epoch: beacon_finalized_epoch
* Current slot: beacon_slot
* Finalized slot: 32 * beacon_finalized_epoch
* Current validators: validator_count
* Pending validators: beacondb_pending_deposits
* Total voted Ether: validators_total_balance
* Total eligible Ether: validators_total_effective_balance

区块数据：

* Historical blocks:
  * Epoch of this block: 
  * Slot of this block: 
  * Timestamp of this block: 
  * Status of this block: 
  * Attestation in this block: 

Slashing相关数据：

（暂时还未同步完）
