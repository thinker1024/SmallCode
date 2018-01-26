#!/bin/bash

######################
## Version: V1.0    ##
## Author: Tao Yang ##
## Date: 2018.01    ##
######################

SDCARD=$1

echo ""
echo "WARNING!!!"
echo ""
echo -n "Continue [y/N]?"
read YN
#read -p "Continue [y/N]?" YN

if [ "$YN" == "N" ] || [ "$YN" == "n" ] || [ "$YN" == "" ]; then
	echo "Quitting..."
	exit 1
fi

umount ${SDCARD}*

dd if=u-boot.imx of=${SDCARD} bs=512 seek=2 conv=fsync 

SIZE=`fdisk -l $SDCARD | grep Disk | awk '{print $5}'`
#CYLINDERS=`echo $SIZE/255/63/512 | bc`

echo DISK SIZE -- $SIZE Bytes
#echo CYLINDERS -- $CYLINDERS

sfdisk --Linux --unit S ${SDCARD} << EOF
20480,225279,L,*
230000,,,-
EOF

mkfs.vfat -F 32 -n "boot" ${SDCARD}1
umount ${SDCARD}1
mkdir -p /mnt/boot
mount ${SDCARD}1 /mnt/boot
cp zImage imx6ul-14x14-gateway.dtb /mnt/boot

mkfs.ext4 -L "rootfs" ${SDCARD}2
umount ${SDCARD}2
mkdir -p /mnt/rootfs
mount ${SDCARD}2 /mnt/rootfs
cp -r ./rootfs/* /mnt/rootfs

umount ${SDCARD}*

echo Flash Done!!!
