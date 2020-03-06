#!/bin/sh

metadata="curl -s http://169.254.169.254/latest/meta-data"

# region & hostname
region=`${metadata}/placement/availability-zone`
hostname=`${metadata}/hostname`

# OS
if [ `which yum` ]; then
	if [ -f '/etc/redhat-release' ]; then
		OS=`cat /etc/redhat-releas`
	else
		OS=`uname -r | awk -F '.' '{print $5}'`
	fi
elif [ `which apt-get` ]; then
	OS=`cat /etc/issue`
fi

# Tomcat check

tomcatcount=`ps aux | egrep -E 'java.*Dcatalina.base=' | grep -v grep | wc -l`

if [ ${tomcatcount} -gt 0 ]; then
	tomcatvrl=()
	if [ ${tomcatcount} -gt 1 ]; then
		for ((i=0; i<${tomcatcount};i++)) 
		do
			if [ ${i} -eq 0 ];then
                                tomcatbase=`ps aux | grep -E 'java.*Dcatalina.base=' |grep -v grep | head -n 1 | awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                        elif [[ ${i} -gt 0 ]] && [[ ${i} -lt `expr ${tomcatcount} - 1` ]]; then
                                headcount=`expr 1 + ${i}`
                                tomcatbase=`ps aux | grep -E 'java.*Dcatalina.base=' |grep -v grep | head -n ${headcount} | tail -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                        elif [ ${i} -eq `expr ${tomcatcount} - 1` ];then
                                tomcatbase=`ps aux | grep -E 'java.*Dcatalina.base=' |grep -v grep |tail -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                        fi

                        if [ -d ${tomcatbase} ]; then
                                tomcatvr=`sh ${tomcatbase}/bin/version.sh | grep '^Server number'`
                        else
                                tomcatvr+="Directory not found"
                        fi
                        tomcatvrl+=("${tomcatvr}")

		done
	else
		tomcatbase=`ps aux | grep -E 'java.*Dcatalina.base=' |grep -v grep | awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
		if [ -d ${tomcatbase} ]; then
			tomcatvr=`sh ${tomcatbase}/bin/version.sh | grep '^Server number'`
		else
			tomcatvr="Directory not found"
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

apachecount=`ps aux | egrep -E 'httpd' | grep -v grep | wc -l`

if [ ${apachecount} -gt 0 ]; then
	apachecheck=`ps aux | grep -E httpd | grep -v grep | tail -n 1 | awk '{print $11}'`
	if [ -f ${apachecheck} ]; then
		apachever=`${apachecheck} -version | grep '^Server version'`
	fi
fi



echo "${region},${hostname},${tomcatvrl[${tomcatnum}]},${apachever}" 
