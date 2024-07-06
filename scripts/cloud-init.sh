disks=(
    "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-nocloud-amd64.qcow2"
)

for disk in "${disks[@]}"; do
    wget -O ../.cache/cloud-disks $disk
done