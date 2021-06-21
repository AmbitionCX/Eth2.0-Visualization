# Prometheus数据库安装

1. Download suited file (https://prometheus.io/download/)
2. `tar -xzvf <prometheus-version>.tar.gz`
3. Edit `prometheus.yml` file:
````
  scrape_configs:
  - job_name: 'beacon-chain'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:8080']
````
