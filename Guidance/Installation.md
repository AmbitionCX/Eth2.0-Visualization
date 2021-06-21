# How to install Geth and Interact with the Mainnet

By ChenXuan @2021-06-09

## Install on Ubuntu via PPAs

The following steps will install **the latest version** of go-ethereum with the built-in launchpad PPAs (Personal Package Archives). It is **the easiset way** to install Geth.

1. `sudo add-apt-repository -y ppa:ethereum/ethereum`
2. `sudo apt-get update && sudo apt-get install ethereu`
3. `geth version`

## Download standalone bundle

The following steps will download standalone bundles, which allow to: 1)**install a specific version of Geth**; 2)**install on machines without Internet access**; 3)**disable automatic updates** and manually manage Geth veriosn

1. Go to [download page](https://geth.ethereum.org/downloads/).
2. Select bundle according to your OS (Linux)
3. Select a proper  archive (64bit), click to download.
4. `tar -xzvf DOWNLOADED_FILE.tar.gz` and enter the unzip folder
5. move `geth` to `/usr/local/bin`
6. `geth version`

## Enter Geth JavaScript Console

Run the follwing command to run `Geth`, entering JavaScript console and trying to connect with the Mainnet with default configurations.

`geth console`

Add some configurations flags inside the command

````bash
geth --mainnet --networkid 1 --datadir "/home/chen/node/database" --identity "Node-1" --ipcpath "/home/chen/node/database/geth.ipc" --port "8545" --verbosity 3 --syncmode "fast" console
````

* `--datadir` Where your data (blocks, transactions) are stored
* `--port` The port to communicate with other peers in P2P way
* `--verbosity` The logging degree in the JavaScript console. 0: silent, 1: error, 2: warn, 3: info, 4: debug, 5: detail (default: 3)
* `--syncmode` **fast**: download full blocks and states; **full** (archive): download full blocks and execute blocks to get states; **light**: download current state only; (default: fast)

Until now, You can run Geth and keep synchronized with the latest blocks.

## More configurations

#### Geth exposes three interfaces to interact with: IPC, HTTP or WebSockets

1. The IPC interface is enabled by default and exposes all the APIs supported.

   * `--ipcdisable` Disable the IPC server

   * `--ipcapi` APIs offered over the IPC interface 

     (default: `admin,debug,eth,miner,net,personal,shh,txpool,web3`)

   * `--ipcpath` Filename for IPC socket/pipe

     (default: `./ethereum/geth/geth.ipc`)

2. HTTP and WS interfaces need to manually be enabled and only expose a subset of APIs due to security reasons

   * `--http` Enable the HTTP-RPC server

   * `--http.addr` HTTP-RPC server listening interface (default: `localhost`)

   * `--http.port` HTTP-RPC server listening port (default: `8545`)

   * `--http.api` APIs offered over the HTTP-RPC interface (default: `eth,net,web3`)

   * `--http.corsdomain` List of domains from which to accept HTTP requests

     

   * `--ws` Enable the WS-RPC server

   * `--ws.addr` WS-RPC server listening interface (default: `localhost`)

   * `--ws.port` WS-RPC server listening port (default: `8546`)

   * `--ws.api` APIs offered over the WS-RPC interface (default: `eth,net,web3`)

   * `--ws.origins` Origins from which to accept websockets requests

#### Export current Geth configuration file

````bash
geth --mainnet --networkid 1 --datadir "/home/chen/node/database" --identity "Node-1" --ipcpath "/home/chen/node/database/geth.ipc" --port "8545" --verbosity 3 --syncmode "fast" dumpconfig > config.toml
````

#### Start Geth with `Toml`configurations

`geth --config config.toml`

## Run Geth as a systemd service

1. Create a file `geth.service` in `/etc/systemd/system`

   ````bash
   [Unit]
   Description=Ethereum Go Client
   
   [Service]
   Type=simple
   User=chen
   Restart=always
   RestartSec=30
   ExecStart=/bin/bash /home/newdisk/blockchain/start.sh
   
   [Install]
   WantedBy=default.target
   ````

2. Ensure the target service are executable

   ````bash
   # Ensure the target service are executable
   sudo chmod +x 
   
   # Reload systemd service files to include new service
   sudo systemctl daemon-reload

3. Enable the service

   ```bash
   # Enable and disable the service restart on system reboot
   sudo systemctl enable geth.service
   sudo systemctl disable geth.service
   
   # Start and stop the service
   sudo systemctl start geth.service
   sudo systemctl stop geth.service
   
   # Current status the service
   sudo systemctl status geth.service
   ```

