#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

// Define a struct using packed 32-bit integers
typedef struct {
    int health;
    int32_t coins;
    int32_t power;
} Stats;

typedef struct {
    float posX;
    float posY;
    Stats *stats;  // Pointer to player's stats
} Player;

void print_stats(Stats *s) {
    printf("Health: %d\n", s->health);
    printf("Coins:  %d\n", s->coins);
    printf("Power:  %d\n", s->power);
}

void print_player(Player *p) {
    printf("Position: (%.2f, %.2f)\n", p->posX, p->posY);
    print_stats(p->stats);
    printf("--------------------\n");
}

int main() {
    Stats player_stats = {100, 0, 10};
    Player player = {0.0f, 0.0f, &player_stats};
    char input;

    printf("Stat Tracker\n");
    printf("------------\n");
    printf("Controls:\n");
    printf("  h = +health, j = -health\n");
    printf("  c = +coins,  v = -coins\n");
    printf("  p = +power,  l = -power\n");
    printf("  w = up, s = down, a = left, d = right\n");
    printf("  q = quit\n\n");

    print_player(&player);

    while (1) {
        printf("Enter command: ");
        input = getchar();

        // Clear newline from stdin buffer
        while (getchar() != '\n');

        switch (input) {
            case 'h':
                player.stats->health += 1;
                break;
            case 'j':
                player.stats->health -= 1;
                break;
            case 'c':
                player.stats->coins += 1;
                break;
            case 'v':
                player.stats->coins -= 1;
                break;
            case 'p':
                player.stats->power += 1;
                break;
            case 'l':
                player.stats->power -= 1;
                break;
            case 'w':
                player.posY += 1.0f;
                break;
            case 's':
                player.posY -= 1.0f;
                break;
            case 'a':
                player.posX -= 1.0f;
                break;
            case 'd':
                player.posX += 1.0f;
                break;
            case 'q':
                printf("Exiting.\n");
                return 0;
            default:
                printf("Invalid input.\n");
        }

        print_player(&player);
    }

    return 0;
}
