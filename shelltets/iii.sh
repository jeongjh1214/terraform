tomcatcount=`cat i | egrep -E 'java.*Dcatalina.base=' | wc -l`

test=`cat i | egrep -E 'java.*Dcatalina.base='`

for a in ${test}
do
	echo ${a}
done


for i in `cat i | egrep -E 'java.*Dcatalina.base='`
do
#        tomcatbase=`echo ${i} | grep -E 'java.*Dcatalina.base=' | awk -F 'Dcatalina.base=' '{print $NF}' | awk '{print $1}'`
#	echo -e ${tomcatbase}
#	if [ -d ${tomcatbase} ]; then
#                tomcatvr=`${tomcatbase}/bin/version.sh | grep '^Server number'`
#	else
#		tomcatvr="directory not found"
#	fi
done
