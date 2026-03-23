set -e

docker compose up -d
docker exec -i esphome_builder bash << 'EOF'
set -e

BUILT_OTA="/config/.esphome/build/neato-vacuum/.pioenvs/neato-vacuum/firmware.ota.bin"
cd /config

rm -f dev.ota.bin
esphome compile .local.yaml
cp $BUILT_OTA dev.ota.bin
chown 1000:1000 dev.ota.bin

curl -v -X POST "http://192.168.205.199/update" \
  -H "Accept: application/octet-stream" \
  -F "update=@./dev.ota.bin;type=application/octet-stream"
EOF