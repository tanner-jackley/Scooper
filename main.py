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

button_w, button_h = 100, 50
button_color = BLUE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Circle")

scoop_radius = 50
scoop = pygame.Rect(WIDTH // 2 - scoop_radius, HEIGHT // 2 - scoop_radius, scoop_radius * 2, scoop_radius * 2)
scoop_color = BLACK

upgrade_button = pygame.Rect(WIDTH // 2 - (button_w * 1.5), HEIGHT // 2 + 65, button_w, button_h)
autoscoop_button = pygame.Rect(WIDTH // 2 + (button_w // 2), HEIGHT // 2 + 65, button_w, button_h)

clock = pygame.time.Clock()
running = True

scoop_count = 0
scoop_multiplyer = 1
current_upgrade_cost = 100
current_autoscoop_cost = 100

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
            if scoop.collidepoint(event.pos):
                scoop_count += scoop_multiplyer

            elif upgrade_button.collidepoint(event.pos) and scoop_count >= current_upgrade_cost:
                scoop_count -= current_upgrade_cost
                scoop_multiplyer *= 2
                current_upgrade_cost *= 5

    screen.fill(WHITE)

    pygame.draw.ellipse(screen, scoop_color, scoop)
    pygame.draw.rect(screen, button_color, upgrade_button)
    pygame.draw.rect(screen, button_color, autoscoop_button)
    drawText(screen, "Upgrade", WHITE, upgrade_button, font, True, None)
    drawText(screen, "Auto", WHITE, autoscoop_button, font, True, None)

    scoop_count_text = font.render(f"{scoop_count}", True, BLACK)
    scoop_multiplyer_text = font.render(f"x{scoop_multiplyer}", True, BLACK)
    upgrade_cost_text = font.render(f"Cost: {current_upgrade_cost}", True, BLACK)
    autoscoop_cost_text = font.render(f"Cost: {current_autoscoop_cost}", True, BLACK)
    screen.blit(scoop_count_text, (WIDTH // 2 - scoop_count_text.get_width() // 2, HEIGHT // 2 - scoop_radius - scoop_multiplyer_text.get_height() - 35))
    screen.blit(scoop_multiplyer_text, (WIDTH // 2 - scoop_multiplyer_text.get_width() // 2, HEIGHT // 2 - scoop_radius - 30))
    screen.blit(upgrade_cost_text, (WIDTH // 2 - (upgrade_cost_text.get_width() * 1.6), HEIGHT // 2 + scoop_radius + button_h + 35))
    screen.blit(autoscoop_cost_text, (WIDTH // 2 + (autoscoop_cost_text.get_width() // 1.6), HEIGHT // 2 + scoop_radius + button_h + 35))

    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
