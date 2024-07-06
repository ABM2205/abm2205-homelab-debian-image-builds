export WORKSPACE=".."

print_msg(){
    echo "[$(date)] $1"
}

function create_new_disk(){
    mkdir -p $WORKSPACE/.cache/disks || true
    print_msg "Creating disk $DISK_NAME"
    print_msg $(qemu-img create -f qcow2 $WORKSPACE/.cache/disks/$DISK_NAME $DISK_SIZE)
}

function copy_cloud_disk(){

    base_disk="../.cache/cloud-disks/$SOURCE_DISK_NAME"
    new_disk="../.cache/cloud-disks/$DISK_NAME"

    print_msg "Creating disk $DISK_NAME"
    print_msg "$base_disk -> $new_disk"
    print_msg "DISK_SIZE: $DISK_SIZE"

    qemu-img create -b "$SOURCE_DISK_NAME" -F qcow2 -f qcow2 "$new_disk" $DISK_SIZE
}

function create_cloud_machine(){
    print_msg "Creating machine $MACHINE_NAME"

    print_msg "Starting machine $MACHINE_NAME"
    qemu-system-x86_64 \
        -name build-machine-$MACHINE_NAME \
        -m 2G \
        -hda $WORKSPACE/.cache/cloud-disks/$DISK_NAME \
        -net nic -net user,hostfwd=tcp::2222-:22 \
        -enable-kvm \
        -nographic
}

function create_ssh_machine(){
    print_msg "Starting machine $MACHINE_NAME"
    qemu-system-x86_64 \
        -name build-machine-$MACHINE_NAME \
        -m 2G \
        -hda $WORKSPACE/.cache/cloud-disks/$DISK_NAME \
        -enable-kvm \
        -net nic -net user,hostfwd=tcp::2222-:22 \
        -display none \
        -serial none &
}

function cleanup_machine(){
    rm -f /tmp/$MACHINE_NAME.in /tmp/$MACHINE_NAME.out || true
    rm -f $WORKSPACE/.cache/disks/* || true
    for pid in $(ps -ef | grep build-machine | awk '{print $2}'); do kill -9 $pid; done
}

function create_raw_disk() {
    SIZE_IN_GIGS=$2 * 1073741824
    dd if=/dev/zero of=$1 bs=1024k seek=25600 count=0
}