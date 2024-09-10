# To install grafana, Mimir and Bravis health monitoring. run this command in the root directory
ansible-playbook --connection=local --inventory 127.0.0.1, monitoring.yml

#Link for  node exporter dashboard for the machine's metrics 
## URL - http://13.60.241.234:3000/d/edx6vpx85hm9sd/nodes?orgId=1&from=now-15m&to=now
## user - admin
## pass - admin
