#!/bin/sh

metadata="curl -s http://169.254.169.254/latest/meta-data"

# region & hostname
region=`${metadata}/placement/availability-zone`
hostname=`${metadata}/hostname`

# OS
if [ `which yum` ]; then
	if [ -f '/etc/redhat-release' ]; then
		OS=`cat /etc/redhat-releas`
	elif [ -f '/etc/system-release' ]; then
		OS=`cat /etc/system-release`
	else
		OS=`uname -r | awk -F '.' '{print $5}'`
	fi
elif [ `which apt-get` ]; then
	OS=`cat /etc/issue`
fi

# Tomcat check
tomcatps=`ps aux | egrep -E 'java.*Dcatalina.base=' | grep -v grep`
tomcatcount=`ps aux | egrep -E 'java.*Dcatalina.base=' | grep -v grep | wc -l`

if [ ${tomcatcount} -gt 0 ]; then
	tomcatvrl=()
	if [ ${tomcatcount} -gt 1 ]; then
		for ((i=0; i<${tomcatcount};i++)) 
		do
			if [ ${i} -eq 0 ];then
                                tomcatbase=`echo "${tomcatps}" | head -n 1 | awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                        elif [[ ${i} -gt 0 ]] && [[ ${i} -lt `expr ${tomcatcount} - 1` ]]; then
                                headcount=`expr 1 + ${i}`
                                tomcatbase=`echo "${tomcatps}" | head -n ${headcount} | tail -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                        elif [ ${i} -eq `expr ${tomcatcount} - 1` ];then
                                tomcatbase=`echo "${tomcatps}" |tail -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                        fi

                        if [ -d ${tomcatbase} ]; then
                                tomcatvr=`sh ${tomcatbase}/bin/version.sh | grep '^Server number'`
                        fi
                        tomcatvrl+=("${tomcatvr}")

		done
	else
		tomcatbase=`echo "${tomcatps}" |head -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
		if [ -d ${tomcatbase} ]; then
			tomcatvr=`sh ${tomcatbase}/bin/version.sh | grep '^Server number'`
		fi
		tomcatvrl+=("${tomcatvr}")
	fi
fi


if [ ${tomcatcount} -gt 0 ]; then
	tomcatnum=`expr ${tomcatcount} - 1`
else
	tomcatnum=0
fi

# Apache check	

apacheps=`ps aux | egrep -E 'httpd' | grep -v grep | awk '{print $11}' | grep -v '^$' | sort | uniq |sort`
apachecount=`ps aux | egrep -E 'httpd' | grep -v grep | awk '{print $11}' | grep -v '^$' | sort | uniq |sort |wc -l`

if [ ${apachecount} -gt 0 ]; then
	apachevrl=()
	if [ ${apachecount} -gt 0 ]; then
		for ((j=0; j<${apachecount};j++))
		do
			if [ ${j} -eq 0 ]; then
				apachecheck=`echo "${apacheps}" | head -n 1`
			elif [[ ${j} -gt 0 ]] && [[ ${i} -lt `expr ${apachecount} - 1` ]]; then
				headcount=`expr 1 + ${i}`
				apachecheck=`echo "${apacheps}" | head -n ${headcount} | tail -n 1`
			elif [ ${j} -eq `expr ${apachecount} - 1` ]; then
				apachecheck=`echo "${apacheps}" | tail -n 1`
			fi

			if [ -f ${apachecheck} ]; then
				apachever=`${apachecheck} -version | grep '^Server version'`
			fi
			apachevrl+=("${apachever}")
		done
	else
		apachecheck=`echo "${apacheps}"`
		if [ -f ${apachecheck} ]; then
			apachever=`${apachecheck} -version | grep '^Server version'`
		fi
		apachevrl+=("${apachever}")
	fi
fi

if [ ${apachecount} -gt 0 ]; then
	apachenum=`expr ${apachecount} - 1`
else
	apachenum=0
fi


if [[ ${tomcatvrl[${tomcatnum}]} ]] || [[ ${apachevrl[${apachenum}]} ]]; then
	echo "${region},${hostname},${tomcatvrl[${tomcatnum}]},${apachevrl[${apachenum}]}"
fi
