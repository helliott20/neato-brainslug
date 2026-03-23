set -e

docker compose up -d
docker exec -i esphome_builder bash << 'EOF'
set -e

BUILT_FACTORY="/config/prebuilt/.esphome/build/neato-vacuum/.pioenvs/neato-vacuum/firmware.factory.bin"
BUILT_OTA="/config/prebuilt/.esphome/build/neato-vacuum/.pioenvs/neato-vacuum/firmware.ota.bin"


cd /config/prebuilt

esphome compile gen3-esp32.yaml
cp $BUILT_FACTORY ./nbs-gen3-esp32.factory.bin
cp $BUILT_OTA ./nbs-gen3-esp32.ota.bin

esphome compile gen3-esp32s3.yaml
cp $BUILT_FACTORY ./nbs-gen3-esp32s3.factory.bin
cp $BUILT_OTA ./nbs-gen3-esp32s3.ota.bin

esphome compile gen3-esp32c3.yaml
cp $BUILT_FACTORY ./nbs-gen3-esp32c3.factory.bin
cp $BUILT_OTA ./nbs-gen3-esp32c3.ota.bin

esphome compile gen2-esp32.yaml
cp $BUILT_FACTORY ./nbs-gen2-esp32.factory.bin
cp $BUILT_OTA ./nbs-gen2-esp32.ota.bin

esphome compile gen2-esp32s3.yaml
cp $BUILT_FACTORY ./nbs-gen2-esp32s3.factory.bin
cp $BUILT_OTA ./nbs-gen2-esp32s3.ota.bin

esphome compile gen2-esp32c3.yaml
cp $BUILT_FACTORY ./nbs-gen2-esp32c3.factory.bin
cp $BUILT_OTA ./nbs-gen2-esp32c3.ota.bin
EOF