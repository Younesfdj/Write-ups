#ifndef BMP_H_
#define BMP_H_

#include <stddef.h>
#include <stdint.h>

#define MAGIC 0x4d42
#define BITCOUNT_ALLOWED 1
#define BIPLANES 1

// hope one day i'll make a true BMP parser
#define UNCOMPRESSED 0
#define RLE_8 1
#define RLE_4 2
#define BITFILEDS 3

#define RESERVED 0
// needs to be 2 since we are only loading 1 bits per pixel BMP
#define CLR_USED 2
#define DATA_OFFSET                                                            \
  0x3e // i think it shouldn't be fix but for the sake of simplicity we will
       // make it so

#define MAX_DATA 0xb00

typedef struct __attribute__((__packed__)) {
  uint16_t bfType;
  uint32_t bfSize;
  uint16_t bfReserved1;
  uint16_t bfReserved2;
  uint32_t bfOffBits;
} file_header;

typedef struct __attribute__((__packed__)) {
  uint32_t biSize;
  uint32_t biWidth;
  uint32_t biHeight; // this should actually not be unsigned but i don't care
  uint16_t biPlanes;
  uint16_t biBitCount;
  uint32_t biCompression;
  uint32_t biSizeImage;
  uint32_t biXPelsPerMeter;
  uint32_t biYPelsPerMeter;
  uint32_t biClrUsed;
  uint32_t biClrImportant;
} image_header;

// this struct has a fixed size because we are only dealing with 1 bit per pixel
// BMPs
typedef struct __attribute__((__packed__)) {
  uint32_t color1;
  uint32_t color2;
} color_palette;

// tiny BMP (｡◕‿‿◕｡)
typedef struct __attribute__((__packed__)) {
  char data[MAX_DATA];
} pixel_data;

typedef struct __attribute__((__packed__)) {
  file_header header;
  image_header image;
  color_palette palette;
  pixel_data data;
} bmp_t;

void validate_file_header(file_header *file, size_t input_size);
void validate_image_header(image_header *bmp, size_t input_size);

void print_file_header(file_header *file);
void print_image_header(image_header *file);
void send_bmp(bmp_t *bmp);
size_t load_data(bmp_t *data, char *buff);
void load_flag();

#endif
