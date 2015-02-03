#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "exif.h"
#include <wand/MagickWand.h>

double compare(char* imagen1,char* imagen2)
{
   MagickWand *img1 = NULL,*img2 = NULL,*m_wand = NULL;
   double distortion = 0.0;

   MagickWandGenesis();
   img1 = NewMagickWand();
   img2 = NewMagickWand();
   MagickReadImage(img1, imagen1);
   MagickReadImage(img2,imagen2);
   MagickResizeImage(img2,MagickGetImageWidth(img1),MagickGetImageHeight(img1),LanczosFilter,1.0);
   MagickGetImageDistortion(img1,img2,PeakSignalToNoiseRatioMetric,&distortion);
   // must be > 20 to be the same

   /* Tidy up */
   img1 = DestroyMagickWand(img1);
   img2 = DestroyMagickWand(img2);
   MagickWandTerminus();
  
  return distortion;
}

void setMeta(const char *img1, const char *img2, char *copy, char *desc)
{
    TagNodeInfo *tag;
    int sts, result;
    void **ifdTableArray = createIfdTableArray(img1, &result);

    if (ifdTableArray != NULL) {
        if (queryTagNodeIsExist(ifdTableArray, IFD_0TH, TAG_Copyright)) {
            removeTagNodeFromIfdTableArray(ifdTableArray, IFD_0TH, TAG_Copyright);
        }
        if (queryTagNodeIsExist(ifdTableArray, IFD_0TH, TAG_UserComment)) {
            removeTagNodeFromIfdTableArray(ifdTableArray, IFD_0TH, TAG_UserComment);
        }
    } else { // Exif segment not exists
        // create new IFD table
        ifdTableArray = insertIfdTableToIfdTableArray(NULL, IFD_0TH, &result);
        if (!ifdTableArray) {
            printf("insertIfdTableToIfdTableArray: ret=%d\n", result);
            printf("error");
            return;
        }
    }
    // create a tag info1
    tag = createTagInfo(TAG_Copyright, TYPE_ASCII, strlen(copy), &result);
    if (!tag) {
        printf("createTagInfo: ret=%d\n", result);
        freeIfdTableArray(ifdTableArray);
        printf("error");
        return;
    }
    // set tag data
    strcpy((char*)tag->byteData, copy);
    // insert to IFD table
    insertTagNodeToIfdTableArray(ifdTableArray, IFD_0TH, tag);
    freeTagInfo(tag);
    // create a tag info2
    
    tag = createTagInfo(TAG_UserComment, TYPE_ASCII, strlen(desc), &result);
    if (!tag) {
        printf("createTagInfo: ret=%d\n", result);
        freeIfdTableArray(ifdTableArray);
        printf("error");
        return;
    }
    // set tag data
    strcpy((char*)tag->byteData, desc);
    // insert to IFD table
    insertTagNodeToIfdTableArray(ifdTableArray, IFD_0TH, tag);
    freeTagInfo(tag);

    // write file
    sts = updateExifSegmentInJPEGFile(img1, img2, ifdTableArray);

    if (sts < 0) {
        printf("updateExifSegmentInJPEGFile: ret=%d\n", sts);
    }
    freeIfdTableArray(ifdTableArray);
}

int main(int argc, char* argv[])
{
    setMeta(argv[1], argv[2], "HOLA", "ADIOS");

    return 0;
}
