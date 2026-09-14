import pygame
from PIL import Image

# Initialize pygame
pygame.init()

# Load GIF and get frames
gif = Image.open("images/giphy.gif")
frames = []
try:
    while True:
        frames.append(gif.copy())
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

# Set up display
screen = pygame.display.set_mode(frames[0].size)
clock = pygame.time.Clock()

# Display frames
running = True
frame_idx = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display the current frame
    frame = frames[frame_idx]
    mode = frame.mode
    size = frame.size
    data = frame.tobytes()
    image = pygame.image.fromstring(data, size, mode)
    screen.blit(image, (0, 0))
    pygame.display.flip()

    # Advance to the next frame
    frame_idx = (frame_idx + 1) % len(frames)
    clock.tick(10)  # Adjust for the GIF's frame rate

pygame.quit()
