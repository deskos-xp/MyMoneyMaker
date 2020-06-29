#! /usr/bin/bash
if test "`whoami`" == "root" ; then
	rm -rf /opt/MyMoneyMaker
	rm /usr/share/applications/MyMoneyMaker.desktop
else
	echo "you are not root!"
fi
