tomcatcount=`cat i | egrep -E 'java.*Dcatalina.base=' | wc -l`

if [ ${tomcatcount} > 0 ]; then
	tomcatvrl=()
        if [ ${tomcatcount} > 1 ]; then
		for ((i=0; i<${tomcatcount};i++)) 
                do
			if [ ${i} == 0 ];then
				tomcatbase=`cat i | grep -E 'java.*Dcatalina.base=' | head -n 1 | awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
			elif [[ ${i} > 0 ]] && [[ ${i} < `expr ${tomcatcount} - 1` ]]; then
				headcount=`expr 1 + ${i}`
				tomcatbase=`cat i | grep -E 'java.*Dcatalina.base=' | head -n ${headcount} | tail -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
			elif [ ${i} == `expr ${tomcatcount} - 1` ];then
				tomcatbase=`cat i | grep -E 'java.*Dcatalina.base=' |tail -n 1| awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
			fi

			if [ -d ${tomcatbase} ]; then
				tomcatvr=`sh ${tomcatbase}/bin/version.sh | grep '^Server number'`
			else
				tomcatvr+="directory not found"
			fi
			tomcatvrl+=("${tomcatvr}")
                done
        else
                tomcatbase=`cat i | grep -E 'java.*Dcatalina.base=' | awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
                if [ -d ${tomcatbase} ]; then
			tomcatver=`${tomcatbase}/bin/version.sh | grep '^Server number'`
		else
			tomcatvr="directory not found"
                fi
		tomcatvrl+=("${tomcatvr}")
	fi
	echo ${tomcatvrl[`expr ${tomcatcount} - 1`]}
fi
