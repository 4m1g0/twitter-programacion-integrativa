all: _imageTools.so

imageTools_wrap.c : imageTools.i
	swig -python imageTools.i
	
imageTools_wrap.o : imageTools_wrap.c  
		gcc -fPIC -c imageTools.c exif.c imageTools_wrap.c -I /usr/include/python2.7/ `pkg-config --cflags --libs MagickWand`
		
_imageTools.so : imageTools_wrap.o imageTools.o exif.o
		gcc -shared imageTools.o exif.o imageTools_wrap.o -Xlinker -rpath /usr/lib -o _imageTools.so `pkg-config --cflags --libs MagickWand`
		
clean:
		rm -f imageTools_wrap.c *.o *.so *~

make install: _imageTools.so
		mv _imageTools.so ../tweetManager/
		mv imageTools.py ../tweetManager/
