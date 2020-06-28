#! /usr/bin/bash
if test "`whoami`" == "root" ; then
	cp -rfv ../../MyMoneyMaker /opt/
	ln -sf /opt/MyMoneyMaker/app/MyMoneyMaker.desktop /usr/share/applications/
else
	echo "you are not root!"
fi
