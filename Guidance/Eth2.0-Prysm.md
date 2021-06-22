# 以太坊2.0客户端安装

By ChenXuan @2021-06-09

Eth2.0的客户端有很多个，不像Eth1.0，Geth一家独大。我们要安装的是Prysm。

## 安装Prysm

安装方法很简单，在`/home/newdisk/`下创建prysm文件夹，然后直接运行script。

```` bash
mkdir prysm && cd prysm
curl https://raw.githubusercontent.com/prysmaticlabs/prysm/master/prysm.sh --output prysm.sh && chmod +x prysm.sh
````

然后通过`prysm.sh beacon-chain --version`查看script能否运行。

通过这个script运行Prysm是自动更新至最新版本的。

## 运行Prysm

在`/home/newdisk/prysm`文件夹中运行`start.sh` 

````bash
#!/bin/bash

sudo /home/newdisk/prysm/prysm.sh beacon-chain --config-file=/home/newdisk/prysm/config.yaml
````

`config.yaml`

````yaml
datadir: '/home/newdisk/prysm/database'
verbosity: 'info'
log-format: 'text'
log-file: '/home/newdisk/prysm/prysm.log'
http-web3provider: '/home/newdisk/blockchain/geth.ipc'

monitoring-host: 127.0.0.1
monitoring-port: 8080
````
## 将Prysm设置成为systemd的一项服务运行在后台

1. Create a file `prysm.service` in `/etc/systemd/system`

   ````
   [Unit]
   Description=Prysm Beacon Chain Client
   After=network.target
   Wants=geth.service

   [Service]
   Type=simple
   User=root
   Restart=always
   RestartSec=10
   ExecStart=/bin/bash /home/newdisk/Eth-Vis/Prysm/start.sh

   [Install]
   WantedBy=default.target
   ````
2. 重新加载systemd服务列表，并启动prysm。service
   
