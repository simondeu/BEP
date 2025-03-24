
import pygame

def DrawNetwork(NetworkNodes, NetworkEdges):
   
    #Parameters
    EdgeWidth = 2
    NodeSize = 10

    # Initialize Pygame
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 16)

    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    edgeScreen = pygame.surface.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    nodeScreen = pygame.surface.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Pygame Template")

    i = 300
    for node in NetworkNodes:
        if "Internal" in node.name:
            node.coordinate = (i,HEIGHT//2)
            node.colour = (255,0,0)
            i += 200
            j = -50
            for node_ in node.neighbours:
                if "Internal" not in node_.name:
                    node_.colour = (0,0,255)
                    node_.coordinate = (node.coordinate[0] + j, node.coordinate[1] + 100)
                    j+=40

    # Clock to control frame rate
    clock = pygame.time.Clock()
    dragging = None

    # Game loop
    running = True
    while running:
        clock.tick(FPS)  # Limit the frame rate
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, circle in enumerate(NetworkNodes):
                    cx, cy = circle.coordinate
                    if (mx - cx) ** 2 + (my - cy) ** 2 <= NodeSize ** 2:
                        dragging = i
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = None
            elif event.type == pygame.MOUSEMOTION and dragging is not None:
                NetworkNodes[dragging].coordinate = event.pos
        
        # Game logic updates
        
        # Drawing
        screen.fill(WHITE)
        nodeScreen.fill((0,0,0,0))
        edgeScreen.fill((0,0,0,0))

        texts = []
        textCoordinates = []
        for node in NetworkNodes:
            pygame.draw.circle(nodeScreen, node.colour, node.coordinate, NodeSize)
            if "Internal" not in node.name:
                text = font.render(node.name, True, BLACK)
                texts.append(text)
                textCoordinates.append((node.coordinate[0], node.coordinate[1] - 30))
        for edge in NetworkEdges:
            pygame.draw.line(edgeScreen, (0,0,0), edge.u.coordinate, edge.v.coordinate, EdgeWidth)

        screen.blit(edgeScreen, (0,0))
        screen.blit(nodeScreen,(0,0))
        for i, text in enumerate(texts):
            screen.blit(text, textCoordinates[i])
        pygame.display.flip()  # Update the display

    # Quit Pygame
    pygame.quit()