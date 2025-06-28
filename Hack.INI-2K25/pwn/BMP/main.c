#include "BMP.h"
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// i like specific random numbers
#define MAX_SIZE 0xb80

char *BUFFER = NULL;

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  load_flag();
  BUFFER = calloc(MAX_SIZE, 1);
  if (!BUFFER) {
    perror("malloc");
    exit(EXIT_FAILURE);
  }
}

int main(void) {
  bmp_t user_bmp;
  setup();
  puts("Ladies and gents give a very big thanks and a round of applause for "
       "this dumb and incomplete BMP parser");
  puts("Image (must be a 1 bit per pixel BMP file):");
  size_t input_size = read(STDIN_FILENO, BUFFER, MAX_SIZE);
  printf("input size is 0x%lx\n", input_size);
  if (!input_size) {
    perror("read");
    exit(EXIT_FAILURE);
  }
  memcpy(&(user_bmp.header), BUFFER, sizeof(file_header));
  validate_file_header(&(user_bmp.header), input_size);

  memcpy(&(user_bmp.image), BUFFER + sizeof(file_header), sizeof(image_header));
  validate_image_header(&(user_bmp.image), input_size);

  // if we reached this point i'll just load your colour palette once again i
  // don't care lol
  memcpy(&(user_bmp.palette),
         BUFFER + sizeof(file_header) + sizeof(image_header),
         sizeof(color_palette));

  // load  data since we have all the headers
  load_data(&user_bmp, BUFFER);

  // print some info
  print_file_header(&(user_bmp.header));
  print_image_header(&(user_bmp.image));

  puts("here goes your BMP file i'll give it back to you");
  send_bmp(&user_bmp);
}
