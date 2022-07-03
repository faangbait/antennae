#!/bin/bash

################################################################################
# This script securely shreds its parent folder on an NVME device.
#
# Usage: sudo ./shred.sh
# Or Simply: ./shred.sh (with passwordless sudo)
#
# It has no warnings.
# It requires superuser to wipe anything.
# Do not put this in /usr/bin. You will eventually delete something important.
################################################################################

# Get the directory to be shredded
ME=$(pwd)

# We'll store the shredder middleware in an unambiguous folder like ~/tmpfs24640
TMPDIR=${HOME}/tmpfs${RANDOM}
mkdir -p ${TMPDIR}

# Mount that directory as a tmpfs filesystem
sudo mount -t tmpfs -o size=1M tmpfs ${TMPDIR}
sudo chown $(whoami) ${TMPDIR}

# Write a middleware script into the tmpdir using a HEREREF
cat > ${TMPDIR}/shred << EOF
#!/bin/bash

# Remove the directory to be shredded
rm -rf ${ME}

# Trim the filesystem. Works on mdadm raid1/10 or any single NVME device.
fstrim $(dirname ${ME})
wait

# Fill the drive with junk, then remove the junk
dd if=/dev/zero of=${ME}
rm ${ME}

# Clean up the middleware
umount ${TMPDIR}
rm -rf ${TMPDIR}

EOF

# Make the middleware executable
chmod +x ${TMPDIR}/shred

# Run it in the background
sudo ${TMPDIR}/shred &
