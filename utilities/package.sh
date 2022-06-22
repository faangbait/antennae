# !/usr/bin/env bash
################################################################################
# Securely packages and unpackages subdirectories. 
#
# Note 1: You MUST repackage directories, or changes will be lost on reboot.
#
# Note 2: Do NOT create new subdirectories while packages are present. Instead,
#         unpackage, then create new subdirectories, then package.
#
# Note 3: Requires more free RAM than the size of the subdirectories; to disable
#         unpacking to RAM, uncomment the following line. This has never been
#         tested in edge cases where it might crash, so if you think you might 
#         be near the RAM limits, it's probably smart to comment out the rm -rf
#         lines just in case.
#
# Note 4: THIS IS DESTRUCTIVE. Test that your backups are working before use.
#
################################################################################

# UNPACK_TO_DISK=1 # Uncomment this if you DON'T want to unpack into RAM

set -e # Fail on errors

usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }

pack () { 
    for SUBDIR in *; do
        if [[ -d ${SUBDIR} ]]; then
            echo "Packaging ${SUBDIR}..."
            
            if [[ -f ${SUBDIR}.tar.gz.gpg ]]; then # Prevent overwriting
                mv ${SUBDIR}.tar.gz.gpg .backup-${SUBDIR}
            fi

            tar -czf - ${SUBDIR} | gpg -se -r $(whoami)  > ${SUBDIR}.tar.gz.gpg

            if [[ ${UNPACK_TO_DISK} -ne 1 ]]; then
                sudo umount ${SUBDIR}
            fi

            sudo rm -rf ${SUBDIR}
        fi
    done
}

unpack() {
    for PACKAGED in *.tar.gz.gpg; do # Loop through our packaged subdirectories
        SUBDIR=${PACKAGED%.tar.gz.gpg} # Get the directory name

        if [ -d ${SUBDIR} ]; then
            echo "Can't unpackage to ${SUBDIR} - already exists."
            exit 1
        fi

        mkdir -p ${SUBDIR}

        if [[ ${UNPACK_TO_DISK} -ne 1 ]]; then
            sudo mount -o sync -t ramfs ramfs ${SUBDIR}
            sudo chown $(whoami) ${SUBDIR}
        fi

        gpg --decrypt ${PACKAGED} | tar -xz

        mv ${PACKAGED} .backup-${SUBDIR}
    done
}


while getopts "pu" arg; do
    case $arg in
        p) # Force Package
            pack
            exit 0
            ;;
        u) # Force Unpackage
            unpack
            exit 0
            ;;
        *)
            usage
            exit 0
            ;;
    esac
done

if [[ $# -eq 0 ]]; then
    if [[ $(find . -maxdepth 1 -type d | wc -l) -ne 1 ]]; then
        pack
        exit 0
    elif [[ $(find *.tar.gz.gpg -maxdepth 1 -type f) ]]; then
        unpack
        exit 0
    fi
    echo "Nothing happened..."
fi
