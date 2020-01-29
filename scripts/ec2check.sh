#!/bin/sh

metadata="curl -s http://169.254.169.254/latest/meta-data"


region=`${metadata}/placement/availability-zone`
hostname=`${metadata}/hostname`
instancetype=`${metadata}/instance-type`
diskinfos=${metadata}/block-device-mapping/
privateip=`${metadata}/local-ipv4`
iamrule=`${metadata}/iam/info | grep Arn | awk -F '/' '{print $NF}' | awk -F '"' '{print $1}'`

# region change
if [ `echo ${region} | grep ap-northeast-2` ]; then
	region='apne2'
fi

# OS
if [ `which yum` ]; then
	if [ -f '/etc/redhat-release' ]; then
		OS=`cat /etc/redhat-release`
	else
		OS=`uname -r | awk -F '.' '{print $5}'`
	fi
elif [ `which apt-get` ]; then
	OS=`cat /etc/issue`
fi

# Disk Check
for disk in `${diskinfos} | grep -v ami`
do
	diskinfo=`${diskinfos}${disk} | awk -F '/' '{if($1 != dev) {print "/dev/"$1} else {print $0}}'`
	if [ -L ${diskinfo} ]; then
		diskinfo=`ls -l ${diskinfo} | awk -F '-> ' '{print "/dev/"$NF}'`
	fi

	# Swap Check
	if [ `swapon | grep ${diskinfo} | wc -l` != 0 ]; then
		Swap=`swapon | grep ${diskinfo} | awk '{print $3}'` 
	fi

	# Root Partition
	if [ `mount | grep ${diskinfo} | awk '{if($3 == "/") print $0}' | wc -l` != 0 ]; then
		rootvolume=`fdisk -l ${diskinfo} | grep GiB | awk '{print $3}'`
	else
		DATAVolume=`fdisk -l ${diskinfo} | grep GiB | awk '{print $3}'`
	fi

done

echo "1,prd,${region},${hostname},${OS},${instancetype},${privateip},${rootvolume},${iamrule},${DATAVolume},${Swap}"
