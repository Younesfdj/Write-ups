#include "BMP.h"
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

bmp_t FLAG;

// no relation with the challenge but that's very bad practice don't do that
#define DIE()                                                                  \
  puts("[!] very bad bmp");                                                    \
  exit(EXIT_FAILURE)

void validate_file_header(file_header *file, size_t input_size) {
  if (file->bfType != MAGIC) {
  }
  if (file->bfSize != input_size || file->bfSize <= DATA_OFFSET) {
    DIE();
  }
  if (file->bfReserved1 != RESERVED || file->bfReserved2 != RESERVED) {
    DIE();
  }
  if (file->bfOffBits != DATA_OFFSET) {
    DIE();
  }
}

void validate_image_header(image_header *image, size_t input_size) {
  if (image->biSize != sizeof(image_header)) {
    DIE();
  }
  if (image->biPlanes != BIPLANES) {
    DIE();
  }
  if (image->biBitCount != BITCOUNT_ALLOWED) {
    DIE();
  }
  if (image->biCompression > 3) {
    DIE();
  }

  // if uncompressed we don't care about the size
  if (image->biCompression != UNCOMPRESSED) {
    if (image->biSizeImage > (MAX_DATA - DATA_OFFSET)) {
      DIE();
    }
  }
  if (image->biClrUsed != CLR_USED) {
    DIE();
  }
}

void print_file_header(file_header *file) {
  puts("[*] FILE HEADER");
  printf("\tbfType      = 0x%04X\n"
         "\tbfSize      = 0x%08X\n"
         "\tbfReserved1 = 0x%04X\n"
         "\tbfReserved2 = 0x%04X\n"
         "\tbfOffBits   = 0x%08X\n\n",
         file->bfType, file->bfSize, file->bfReserved1, file->bfReserved2,
         file->bfOffBits);
}

void print_image_header(image_header *image) {
  puts("[*] IMAGE HEADER");
  printf("\tbiSize          = 0x%08X\n"
         "\tbiWidth         = 0x%08X\n"
         "\tbiHeight        = 0x%08X\n"
         "\tbiPlanes        = 0x%04X\n"
         "\tbiBitCount      = 0x%04X\n"
         "\tbiCompression   = 0x%08X\n"
         "\tbiSizeImage     = 0x%08X\n"
         "\tbiXPelsPerMeter = 0x%08X\n"
         "\tbiYPelsPerMeter = 0x%08X\n"
         "\tbiClrUsed       = 0x%08X\n"
         "\tbiClrImportant  = 0x%08X\n\n",
         image->biSize, image->biWidth, image->biHeight, image->biPlanes,
         image->biBitCount, image->biCompression, image->biSizeImage,
         image->biXPelsPerMeter, image->biYPelsPerMeter, image->biClrUsed,
         image->biClrImportant);
}

void send_bmp(bmp_t *bmp) {
  puts("[*] Raw BMP");
  write(STDOUT_FILENO, bmp, bmp->header.bfSize);
}

size_t load_data(bmp_t *data, char *buff) {
  size_t pixel_data_input = 0;
  if (data->image.biCompression != UNCOMPRESSED)
    pixel_data_input = data->image.biSizeImage;
  else {
    pixel_data_input =
        (data->image.biHeight * data->image.biWidth * data->image.biBitCount) /
        8;
  }

  memcpy(&(data->data), buff + data->header.bfOffBits, pixel_data_input);
  return pixel_data_input;
}

void load_flag() {
  FILE *flag_bmp = fopen("./flag.bmp", "rb");
  if (!flag_bmp) {
    perror("fopen flag failed");
    exit(EXIT_FAILURE);
  }
  if (fseek(flag_bmp, 0, SEEK_END) != 0) {
    perror("fseek failed");
    fclose(flag_bmp);
    exit(EXIT_FAILURE);
  }

  long filesize = ftell(flag_bmp);
  if (filesize == -1) {
    perror("ftell failed");
    fclose(flag_bmp);
    exit(EXIT_FAILURE);
  }

  rewind(flag_bmp);
  if (filesize > sizeof(bmp_t)) {
    puts("[*] Flag file too big");
    exit(EXIT_FAILURE);
  }
  fread(&FLAG, 1, filesize, flag_bmp);
}
