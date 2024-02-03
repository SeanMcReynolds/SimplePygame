import pygame, sys, random, math

def random_color():
    return (random.randint(100,255),random.randint(100,255),random.randint(100,255), 180)
def solid_rand_color():
    return (random.randint(100,255),random.randint(100,255),random.randint(100,255), 255)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super(Player, self).__init__()
        self.count = 0
        self.image = pygame.Surface((100,100), pygame.SRCALPHA, 32)
        self.color = solid_rand_color()
        self.image.convert_alpha()
        self.image.fill(color)
        self.radius = 40
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(40,1190),random.randint(40,590)))
    
    def move(self, deltax, deltay):
        if self.rect.left < 0 or self.rect.right>1200:
            deltax *= -3
        if self.rect.top < 0 or self.rect.bottom > 600:
            deltay *= -3

        self.rect.centerx += deltax
        self.rect.centery += deltay
    
    def collision(self, other):
        if math.dist((self.rect.center), (other.rect.center)) <= self.radius + other.radius:
            return True
        else:
            return False
    def relocate(self):
        self.rect.center = (random.randint(10,1190),random.randint(10,590))
        
class Food(pygame.sprite.Sprite):
    # Constructor
    def __init__(self):
        super(Food, self).__init__()
        self.color = random_color()
        self.radius = 10
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(10,1190),random.randint(10,590)))
    def relocate(self):
        self.rect.center = (random.randint(10,1190),random.randint(10,590))
        
class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.player1_score = 0
        self.player2_score = 0
        self.font = pygame.font.Font(None, 32)

    def draw(self):
        p1_score_text = self.font.render(f"Player 1: {self.player1_score}", True, (255, 255, 255))
        p2_score_text = self.font.render(f"Player 2: {self.player2_score}", True, (255, 255, 255))
        self.screen.blit(p1_score_text, (10, 10))
        self.screen.blit(p2_score_text, (10, 50))

    def increase_player1_score(self, points):
        self.player1_score += points
    
    def increase_player2_score(self, points):
        self.player2_score += points

    def p1_win(self):
        player_1_win = self.font.render(f"Player 1 Wins!", True, (255, 255, 255))
        text_rect = player_1_win.get_rect(center=(1200/2, 600/2))
        self.screen.blit(player_1_win, text_rect)
    
    def p2_win(self):
        player_2_win = self.font.render(f"Player 2 Wins!", True, (255, 255, 255))
        text_rect = player_2_win.get_rect(center=(1200/2, 600/2))
        self.screen.blit(player_2_win, text_rect)




# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("first to 100")

# Create clock to later control frame rate
clock = pygame.time.Clock()

meals = pygame.sprite.Group()
for i in range(100):
    meals.add(Food())

p1 = Player(1100,300, solid_rand_color())
p2 = Player(100,300, solid_rand_color())
players = pygame.sprite.Group()
players.add(p1)
players.add(p2)

objects = pygame.sprite.Group()
objects.add(meals)
objects.add(players)

scoreboard = Scoreboard(screen)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))

        # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Update rectangle position based on key presses
    # if keys[pygame.K_LEFT]:
    #     sq.rect.x -= 2
    # if keys[pygame.K_RIGHT]:
    #     sq.rect.x += 2
    # if keys[pygame.K_UP]:
    #     sq.rect.y -= 2
    # if keys[pygame.K_DOWN]:
    #     sq.rect.y += 2
    
    if keys[pygame.K_LEFT]:
        p1.move(-4,0)
    if keys[pygame.K_RIGHT]:
        p1.move(4,0)
    if keys[pygame.K_UP]:
        p1.move(0,-4)
    if keys[pygame.K_DOWN]:
        p1.move(0,4)
    
    if keys[pygame.K_a]:
        p2.move(-4,0)
    if keys[pygame.K_d]:
        p2.move(4,0)
    if keys[pygame.K_w]:
        p2.move(0,-4)
    if keys[pygame.K_s]:
        p2.move(0,4)
        
    




    for player in players:
        food_collisions = pygame.sprite.spritecollide(player, meals, True)
        for food in food_collisions:
            new_food = Food()
            meals.add(new_food)
            if player == p1:
                scoreboard.increase_player1_score(1)
            elif player == p2:
                scoreboard.increase_player2_score(1)
        for other in players:
            if player != other and player.rect.colliderect(other.rect):
                screen.fill((255,0,0))
                player.relocate()
        if scoreboard.player1_score >= 100:
            scoreboard.p1_win()
        if scoreboard.player2_score >= 100:
            scoreboard.p2_win()

    meals.draw(screen)
    players.draw(screen)
    scoreboard.draw()

    # Update the display
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
