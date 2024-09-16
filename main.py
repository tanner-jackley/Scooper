import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont('freesansbold', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Circle")

button_circle_radius = 50
button = pygame.Rect(WIDTH // 2 - button_circle_radius, HEIGHT // 2 - button_circle_radius, button_circle_radius * 2, button_circle_radius * 2)
button_color = BLACK

upgrade_w, upgrade_h = 100, 50
upgrade_button = pygame.Rect(WIDTH // 2 - (upgrade_w // 2), HEIGHT // 2 + 65, upgrade_w, upgrade_h)
upgrade_button_color = BLUE

clock = pygame.time.Clock()
running = True

total_button_score = 0
score_increment = 1
upgrade_cost = 100

# https://www.pygame.org/wiki/TextWrap
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.centerx - image.get_width() // 2, rect.centery - image.get_height() // 2))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                total_button_score += score_increment

            elif upgrade_button.collidepoint(event.pos) and total_button_score >= upgrade_cost:
                total_button_score -= upgrade_cost
                score_increment *= 2
                upgrade_cost *= 5

    screen.fill(WHITE)

    pygame.draw.ellipse(screen, button_color, button)
    pygame.draw.rect(screen, upgrade_button_color, upgrade_button)
    drawText(screen, "Upgrade", WHITE, upgrade_button, font, True, None)

    score_text = font.render(f"{total_button_score}", True, BLACK)
    increment_text = font.render(f"x{score_increment}", True, BLACK)
    cost_text = font.render(f"Cost: {upgrade_cost}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - button_circle_radius - increment_text.get_height() - 25))
    screen.blit(increment_text, (WIDTH // 2 - increment_text.get_width() // 2, HEIGHT // 2 - button_circle_radius - 25))
    screen.blit(cost_text, (WIDTH // 2 - cost_text.get_width() // 2, HEIGHT // 2 + button_circle_radius + upgrade_h + 45))

    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
