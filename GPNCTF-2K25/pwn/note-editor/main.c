#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>


#define NOTE_SIZE 1024
struct Note {
    char* buffer;
    size_t size;
    uint32_t budget; 
    uint32_t pos; 
};
typedef struct Note Note;

#define SCANLINE(format, args) \
    ({ \
    char* __scanline_line = NULL; \
    size_t __scanline_length = 0; \
    getline(&__scanline_line, &__scanline_length, stdin); \
    sscanf(__scanline_line, format, args); \
    })

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void reset(Note* note) {
    memset(note->buffer, 0, note->size);
    note->budget = note->size;
    note->pos = 0;
}

void append(Note* note) {
    printf("Append something to your note (%u bytes left):\n", note->budget);
    fgets(note->buffer + note->pos, note->budget, stdin);
    uint32_t written = strcspn(note->buffer + note->pos, "\n") + 1;
    note->budget -= written;
    note->pos += written;
}

void edit(Note* note) {
    printf("Give me an offset where you want to start editing: ");
    uint32_t offset;
    SCANLINE("%u", &offset);
    printf("How many bytes do you want to overwrite: ");
    int64_t length;
    SCANLINE("%ld", &length);
    if (offset <= note->pos) {
        uint32_t lookback = (note->pos - offset); 
        if (length <= note->budget + lookback) {  
            fgets(note->buffer + offset, length + 2, stdin); // plus newline and null byte
            uint32_t written = strcspn(note->buffer + offset, "\n") + 1;
            if (written > lookback) {
                note->budget -= written - lookback;
                note->pos += written - lookback;
            }
        }
    } else {
        printf("Maybe write something there first.\n");
    }
}

void truncate(Note* note) {
    printf("By how many bytes do you want to truncate?\n");
    uint32_t length;
    SCANLINE("%u", &length);
    if (length > note->pos) {
        printf("You did not write that much, yet.\n");
    } else {
        note->pos -= length;
        memset(note->buffer + note->pos, 0, length);
        note->budget += length;
    }
}

uint32_t menu() {
    uint32_t choice;
    printf(
        "Choose your action:\n"
        "1. Reset note\n"
        "2. View current note\n"
        "3. Append line to note\n"
        "4. Edit line at offset\n"
        "5. Truncate note\n"
        "6. Quit\n"
    );
    SCANLINE("%u", &choice);
    return choice;
}

int main() {
    Note note;
    char buffer[NOTE_SIZE];
    
    note = (Note) {
        .buffer = buffer,
        .size = sizeof(buffer),
        .pos = 0,
        .budget = sizeof(buffer)
    };

    setup();
    reset(&note);
    printf("Welcome to the terminal note editor as a service.\n");
    
    while (1)
    {
        uint32_t choice = menu();
        switch (choice)
        {
        case 1:
            reset(&note);
            break;
        case 2:
            printf("Current note content:\n\"\"\"\n");
            puts(note.buffer);
            printf("\"\"\"\n");
            break;
        case 3:
            append(&note);
            break;
        case 4:
            edit(&note);
            break;
        case 5:
            truncate(&note);
            break;
        case 6: // fall trough to exit
            printf("Bye\n");
            return 0;
        default:
            printf("Exiting due to error or invalid action.\n");
            exit(1);
        }
    }
}