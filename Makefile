DESTDIR=$HOME/bin
TARGET=psmcdata
install:
	mkdir -p $DESTDIR
	cp -p psmcdata.py $DESTDIR/$TARGET
	chmod +x $DESTDIR/$TARGET
