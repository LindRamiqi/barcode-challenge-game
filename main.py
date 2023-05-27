import pygame
import random

# Initialize Pygame
pygame.init()

# Set the width and height of the game window
window_width = 1920
window_height = 1080

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)

# icon = pygame.image.load("solvit_icon.png")
# pygame.display.set_icon(icon)

# Set the game speed and score
game_speed = 1
score = 0

username = ""
company = ""
email = ""
telefoni = ""

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Barcode Challenge Game")


def store_contact(emri, kompania, imella, telefon, pikt):
    with open("storage/index.txt", "r") as f:
        contact_index = int(f.read())

    with open("storage/contact.txt", "a") as file:
        file.write(f"{contact_index}:{emri},{kompania},{imella},{telefon},[Score:{pikt}]\n")
        contact_index += 1

    with open("storage/index.txt", "w") as fil:
        fil.write(contact_index.__str__())


def store_highscore_in_file(dictionary, fn="storage/high.txt", top_n=10):
    with open(fn, "w") as f:
        for idx, (name, pts) in enumerate(sorted(dictionary.items(), key=lambda x: -x[1])):
            f.write(f"{name}:{pts}\n")
            if top_n and idx == top_n - 1:
                break


def add_score(scores, name, piket):
    scores[name] = piket


def load_highscore_from_file(fn="storage/high.txt"):
    hs = {}
    try:
        with open(fn, "r") as f:
            for line in f:
                name, _, points = line.partition(":")
                if name and points:
                    hs[name] = int(points)
    except FileNotFoundError:
        return {}
    return hs


high_scores = load_highscore_from_file()


def draw_start_screen():
    global username, company, email, telefoni, high_scores
    """Display the start screen."""

    name_box = pygame.Rect(125, 225, 475, 60)
    company_box = pygame.Rect(125, 350, 475, 60)
    email_box = pygame.Rect(125, 475, 475, 60)
    telefoni_box = pygame.Rect(125, 600, 475, 60)

    font_box = pygame.font.SysFont(None, 40)
    font_small = pygame.font.SysFont(None, 40)

    splash_screen = pygame.image.load("images/splash_screen.png")
    window.blit(splash_screen, (0, 0))

    # Draw the high scores
    high_scores = load_highscore_from_file()
    print(high_scores)

    i = 0
    for k, v in high_scores.items():
        high_score_i = f"{i + 1:>2}."
        high_score_name = f"{k:<28}"
        high_scoresz = f"{v:>6}"

        font = pygame.font.Font(None, 50)

        text_i = font.render(high_score_i, True, white)
        text_name = font.render(high_score_name, True, white)
        text_score = font.render(high_scoresz, True, white)

        window.blit(text_i, (1310, 352 + i * 61))
        window.blit(text_name, (1375, 352 + i * 61))
        window.blit(text_score, (1730, 352 + i * 61))
        i += 1

    pygame.display.update()

    username = ""
    company = ""
    email = ""
    telefoni = ""

    name_active = False
    company_active = False
    email_active = False
    telefoni_active = False

    game_started = True

    while game_started:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SEMICOLON:
                game_started = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if name_box.collidepoint(mouse_position):
                    name_active = True
                else:
                    name_active = False
                if company_box.collidepoint(mouse_position):
                    company_active = True
                else:
                    company_active = False
                if email_box.collidepoint(mouse_position):
                    email_active = True
                else:
                    email_active = False
                if telefoni_box.collidepoint(mouse_position):
                    telefoni_active = True
                else:
                    telefoni_active = False
            if event.type == pygame.KEYDOWN:
                print(event.unicode, event.unicode.isalpha())
                if name_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_TAB:
                        name_active = False
                        company_active = True
                    else:
                        username = username + event.unicode
                elif company_active:
                    if event.key == pygame.K_BACKSPACE:
                        company = company[:-1]
                    elif event.key == pygame.K_TAB:
                        company_active = False
                        email_active = True
                    else:
                        company = company + event.unicode
                elif email_active:
                    if event.key == pygame.K_BACKSPACE:
                        email = email[:-1]
                    elif event.key == pygame.K_TAB:
                        email_active = False
                        telefoni_active = True
                    else:
                        email = email + event.unicode
                elif telefoni_active:
                    if event.key == pygame.K_BACKSPACE:
                        telefoni = telefoni[:-1]
                    elif event.key == pygame.K_TAB:
                        name_active = True
                        telefoni_active = False
                    else:
                        telefoni = telefoni + event.unicode

        if name_active:
            color_name = pygame.Color('yellow')
        else:
            color_name = pygame.Color('black')
        if company_active:
            color_company = pygame.Color('yellow')
        else:
            color_company = pygame.Color('black')
        if email_active:
            color_email = pygame.Color('yellow')
        else:
            color_email = pygame.Color('black')
        if telefoni_active:
            color_telefoni = pygame.Color('yellow')
        else:
            color_telefoni = pygame.Color('black')

        window.blit(font_small.render("Your name:", True, 'white'), (name_box.x, name_box.y - 35))
        pygame.draw.rect(window, color_name,
                         (name_box.left - 5, name_box.top - 5, name_box.width + 10, name_box.height + 10))
        pygame.draw.rect(window, white, name_box)

        window.blit(font_small.render("Company name:", True, 'white'), (company_box.x, company_box.y - 35))
        pygame.draw.rect(window, color_company,
                         (company_box.left - 5, company_box.top - 5, company_box.width + 10, company_box.height + 10))
        pygame.draw.rect(window, white, company_box)

        window.blit(font_small.render("Your email:", True, 'white'), (email_box.x, email_box.y - 35))
        pygame.draw.rect(window, color_email,
                         (email_box.left - 5, email_box.top - 5, email_box.width + 10, email_box.height + 10))
        pygame.draw.rect(window, white, email_box)

        window.blit(font_small.render("Contact number:", True, 'white'), (telefoni_box.x, telefoni_box.y - 35))
        pygame.draw.rect(window, color_telefoni, (
            telefoni_box.left - 5, telefoni_box.top - 5, telefoni_box.width + 10, telefoni_box.height + 10))
        pygame.draw.rect(window, white, telefoni_box)

        surf_name = font_box.render(username, True, 'black')
        surf_company = font_box.render(company, True, 'black')
        surf_email = font_box.render(email, True, 'black')
        surf_telefoni = font_box.render(telefoni, True, 'black')

        window.blit(surf_name, (name_box.x + 5, name_box.y + 15))
        window.blit(surf_company, (company_box.x + 5, company_box.y + 15))
        window.blit(surf_email, (email_box.x + 5, email_box.y + 15))
        window.blit(surf_telefoni, (telefoni_box.x + 5, telefoni_box.y + 15))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SEMICOLON]:
            break


def font_style(size):
    return pygame.font.SysFont(None, size)


def generate_random_letter():
    """Generate a random letter from A to Z."""
    # return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return random.choice("A")


def generate_random_barcode(letter):
    barcode = pygame.image.load("barcodes/barcode_" + letter + ".png")
    barcode_scaled = pygame.transform.scale(barcode, (100, 100))
    return barcode_scaled


def draw_text(text, x, y, size):
    """Draw the given text at the specified position on the screen."""
    text_surface = font_style(size).render(text, True, black)
    window.blit(text_surface, (x, y))


def game_over():
    """Display the final score and quit the game."""
    window.fill(white)
    draw_text("Game Over!", 675, 400, 150)
    draw_text("Score: " + str(score), 850, 550, 75)
    pygame.display.update()
    pygame.time.wait(3000)


def generate_random_position(barcode):
    x = random.randrange(250, window_width - barcode.get_width())
    y = random.randrange(250, window_height - barcode.get_height())
    return x, y


def game_loop():
    # Set up the timer
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    game_duration = 60000  # 60 seconds

    """Main game loop."""
    global score, high_scores, email, company, telefoni
    score = 0
    letter = generate_random_letter()
    barcode = generate_random_barcode(letter)
    print(letter)

    # Start position for the first letter
    x = random.randrange(0, window_width - barcode.get_width())
    y = random.randrange(0, window_height - barcode.get_height())
    #
    # try:
    #     with open("high_scores.pkl", "rb") as file:
    #         high_scores = pickle.load(file)
    # except FileNotFoundError:
    #     pass

    running = True
    game_flow = 1
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode == letter:
                    x, y = generate_random_position(barcode)
                    if game_flow != 1:
                        y = 0

                    score += 1

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time < 20000:
            game_flow = 1
        elif 20000 <= elapsed_time < 40000:
            game_flow = 2
            y += random.randrange(8, 18)

        elif 40000 <= elapsed_time < game_duration:
            game_flow = 3

            y += random.randrange(8, 18)
            x -= random.randrange(8, 13)

        # Check if the game time has reached the duration
        elif elapsed_time >= game_duration:
            running = False

            # Check if the current score is a high score
            if score > 0:
                add_score(high_scores, username, score)
                store_highscore_in_file(high_scores)
                store_contact(username, company, email, telefoni, score)
                # high_scores.append(score)
                # high_scores.sort(reverse=True)
                # high_scores = high_scores[:10]  # Keep only the top 10 scores
                #
                # # Save the updated high scores
                # with open("high_scores.pkl", "wb") as file:
                #     pickle.dump(high_scores, file)

        # Clear the screen
        window.fill(white)

        # Move the letter downwards
        # y += game_speed

        # Draw the letter on the screen

        window.blit(barcode, (x, y))

        # Draw the timer
        remaining_time = max(0, game_duration - elapsed_time)
        seconds = remaining_time / 1000
        timer_text = f"Time: {seconds:.2f}s"
        font = pygame.font.Font(None, 50)
        text_surface = font.render(timer_text, True, (0, 0, 0))
        window.blit(text_surface, (10, 50))

        # If the letter reaches the bottom of the screen, generate a new letter
        if y > window_height or x < -100:

            x = random.randrange(0, window_width - 250)
            y = 0
            if game_flow == 3:
                x = random.randrange(300, window_width - 250)
            letter = generate_random_letter()
            barcode = generate_random_barcode(letter)

        # Display the current score
        draw_text("Score: " + str(score), 10, 10, 50)

        # Update the display
        pygame.display.update()

        # Set the frames per second
        clock.tick(60)
    game_over()


def main():
    while True:
        draw_start_screen()
        game_loop()


main()
