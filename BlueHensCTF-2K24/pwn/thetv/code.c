#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>

void promptChannel(void) {
    printf("Switch to what channel?\n>  ");
    return;
}

void programModePrompt(void) {
    printf("You enter programming mode, and hear the remote say: Please say what option you want to select: Account Options, Channel Info, Security, or More Options.\n>  ");
    return;
}

void printTv(void) {
    puts(" _______________");
    puts("|,----------.  |");
    puts("||           |=| |");
    puts("||          || | |");
    puts("||       . _o| | | __");
    puts("|`-----------\' |/ /~/");
    puts(" ~~~~~~~~~~~~~~~ / /");
    puts("                 ~~");
    return;
}


void flushGetChar(void) {
  int c;
  
  do {
    c = getchar();
  } while (c != 10);
  return;
}



void printTitle(void) {
    putchar(10);
    puts("  _______ _            _________      __");
    puts(" |__   __| |          |__   __\\ \\    / /");
    puts("    | |  | |__   ___     | |   \\ \\  / / ");
    puts("    | |  | \'_ \\ / _ \\    | |    \\ \\/ /  ");
    puts("    | |  | | | |  __/    | |     \\  /   ");
    puts("    |_|  |_| |_|\\___|    |_|      \\/    ");
    putchar(10);
    return;
}

void printMode(void) {
    printf("Which mode? Programming (p) or Channel Switching (c)? p/c\n>  ");
    return;
}

void printChoice(void) {
    printf("Change the channel? (y/n)\n>  ");
    return;
}

void printChannels(void) {
    int local_c;
    for (local_c = 0; local_c < 6; local_c = local_c + 1) {
        printf("Channel %d: %s\n", (ulong)(local_c + 1), *(undefined8 *)(channels + (long)local_c * 8));
    }
    putchar(10);
    return;
}

bool checkPin(int param_1) {
    return (long)param_1 == *(long *)**(undefined8 **)*pin;
}

void alwaysFails(void) {
    puts("Sorry, I did not get that. Please try again later.");
    return;
}

int main(void) {
    int userInput;
    time_t currentTime;
    int selectedChannel;
    int enteredPin;
    uint remainingAttempts = 3;
    int pinCheckResult;
    FILE *flagFile;
    char userMessage[72];

    setvbuf(stdout, NULL, _IONBF, 0);
    srand((uint)time(NULL));
    pin = &local_68;

    printTitle();
    printTv();
    puts("The gentleman living at house 777 just got a new remote! He\'s ready to test it out and see what all the rage is about! It\'s programmable!");
    puts(".. but his cable service only has 6 channels\n");
    printChannels();

    while (1) {
        printMode();
        userInput = getchar();
        flushGetChar();

        if ((char)userInput == 'p') {
            programModePrompt();
            fgets(userMessage, 65, stdin);
            printf("You say: %s", userMessage);
            puts("... you hear the remote say\n");
            alwaysFails(); // prints "Sorry, I did not get that. Please try again later.
        } else {
            printChoice(); // prints "Change the channel? (y/n)\n>  "
            userInput = getchar();
            flushGetChar();

            if ((char)userInput != 'y') {
                puts("You shut off your TV in frustration... bummer, you just got a new remote :(");
                exit(0);
            }

            promptChannel(); // "Switch to what channel?\n>  "
            fflush(stdin);
            __isoc99_scanf("%d", &selectedChannel);

            if (selectedChannel == 6) {
                if (remainingAttempts == 0) {
                    printf("You see a message pop up on the screen: 'YOU ARE LOCKED OUT, WHO LET BRO COOK");
                } else {
                    remainingAttempts--;
                    puts("It\'s prompting for a pin... you forgot the pin... but you still try anyway.\n");
                    printf("Enter the pin: ");
                    __isoc99_scanf("%d", &enteredPin);
                    pinCheckResult = checkPin(enteredPin);

                    if (pinCheckResult != 0) break;
                    printf("Aghhhh the pin failed! You see something pop up on the screen: %d TRIES LEFT\n\n", (ulong)remainingAttempts);
                }
            }
        }
    }

    puts("It worked?!? You must\'ve said open-sesame before you entered the pin.");
    flagFile = fopen("flag.txt", "r");
    if (!flagFile) {
        puts("Error reading flag... notify organizers");
        exit(420);
    }

    while ((userInput = fgetc(flagFile)) != -1) putchar(userInput);
    fclose(flagFile);

    return 0;
}