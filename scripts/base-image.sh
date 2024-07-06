source scripts/machine.sh

export DISK_NAME=base-image.qcow2
export MACHINE_NAME=base-image
export DISK_SIZE=30G
export IMAGE_NAME="alpine-standard-3.20.0-x86_64.iso"


cleanup_machine
create_machine

