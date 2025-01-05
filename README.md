


 Configuration
===============

Create docker container; assuming it will be named "smarthome-tesla" and mount
/data to a volume.

Generate keypair:

$ docker exec -it smarthome-tesla tesla-keygen -key-file /data/private_key.kem -output /data/public_key.pem create

Register with car:

1. docker exec -it smarthome-tesla tesla-control -ble -key-file /data/private_key.pem -vin XXXXX add-key-request /data/public_key.pem owner cloud_key
2. Authenticate in the car with NFC key card

