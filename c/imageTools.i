%module imageTools

%{
#define SWIG_FILE_WITH_INIT
#include "imageTools.h"
%}

double compare(char *imagen1, char *imagen2);
void setMeta(const char *img1, const char *img2, char *copy, char *desc);
