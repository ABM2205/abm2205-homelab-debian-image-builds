MACHINE_MEMORY="8G"
MACHINE_CORES="16"


function timestamp(){
    echo $(date +%s)
}

function print_msg(){
    echo "[$(timestamp)] $1"
}

# $1 disk name
# $3 disk size
# $2 source disk directory
function create_qcow_disk(){
    echo "Creating disk $1"
    qemu-img create -f qcow2 $2/$1 $3
}


# $1 source disk path
# $2 new disk path
# $3 new disk size
function copy_cloud_disk(){

    qemu-img create -b "$1" -F qcow2 -f qcow2 "$2" $3
}

function wait_for_ssh(){
    while ! nc -z localhost $1; do
        sleep 1
    done
}

# $1 machine name
# $2 disk path
# $3 port
function start_cloud_machine(){
    print_msg "Creating machine $1"

    print_msg "Starting machine $1"
    qemu-system-x86_64 \
        -name $1\
        -m 8G \
        -smp 8 \
        -hda $2 \
        -net nic -net user,hostfwd=tcp::$3-:22 \
        -enable-kvm \
        -nographic
}

function start_ssh_machine(){
    print_msg "Starting machine $1"
    qemu-system-x86_64 \
        -name $1 \
        -m 8G \
        -smp 8 \
        -hda $2 \
        -enable-kvm \
        -net nic -net user,hostfwd=tcp::$3-:22 \
        -display none \
        -serial none \
        -monitor none &
}

function start_test_machine(){
    print_msg "Starting machine $1"
    qemu-system-x86_64 \
        -name $1 \
        -m 8G \
        -smp 8 \
        -hda $2 \
        -enable-kvm \
        -net nic -net user,hostfwd=tcp::$3-:22 \
        -vnc :1
}

function kill_build_machines(){
        machines=$(ps -ef | grep -v grep | grep $1 | awk '{print $2}')
        echo "Killing running build machines..."
        echo $(ps -ef | grep -v grep | grep $1)
        for pid in $machines; 
        do kill -9 $pid;
        done;
        kill -9 $(ss -lptn 'sport = :2222' | perl -nle 'print $1 if /pid=(\d+)/')
}



function create_raw_disk() {
    SIZE_IN_GIGS=$2 * 1073741824
    dd if=/dev/zero of=$1 bs=1024k seek=25600 count=0
}

function commit_and_create_disk(){
    qemu-img commit $1
    rm $1
    mv $2 $3/$4-$(timestamp).qcow2
}