import qwstpad
import random
import time


class game_state:
    TITLE = 0
    GAMEPLAY = 1
    DEATH_ANIM = 2
    GAMEOVER = 3


class player_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32

        self.vy = 0
        self.vx = 0
        self.airborne = False
        self.dead = False

        self.animation = sqirl_run

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @r.setter
    def r(self, a):
        self.x = a - self.w

    @b.setter
    def b(self, a):
        self.y = a - self.h

    @property
    def bounding_box(self):
        return rect(self.x + 8, self.y + 20, self.w - 16, self.h - 20)

    def is_standing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b == platform.y:
            return True
        return False

    def is_landing(self, platform):
        if self.r < platform.x or self.x > platform.r:
            return False
        if self.b < platform.y and self.b + self.vy >= platform.y:
            return True
        return False

    def is_airborne(self):
        airborne = True
        for platform in platforms:
            if self.is_standing(platform):
                airborne = False
        self.airborne = airborne

    def update(self):
        self.is_airborne()

        if self.airborne or self.dead or controls["DROP"]:
            self.vy += 1
        else:
            if controls["JUMP"]:
                self.vy = -10

            if controls["JUMP_RIGHT"]:
                self.vx = max(self.vx, 3)

            elif controls["JUMP_LEFT"]:
                self.vx = min(self.vx, -3)

            elif controls["MOVE_RIGHT"]:
                self.vx += 1.5

            elif controls["MOVE_LEFT"]:
                self.vx -= 1.5

            if self.vx > 0:
                self.vx -= 0.5
            elif self.vx < 0:
                self.vx += 0.5

        if not self.dead:
            for platform in platforms:
                if self.is_landing(platform):
                    self.b = platform.y
                    self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.x = clamp(self.x, 0, screen.width - self.w)

        self.draw()

    def reset(self):
        self.x = 20
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.dead = False
        self.animation = sqirl_run

    def death(self):
        self.b = screen.height - 1
        self.vx = 0
        self.vy = -12
        self.dead = True
        self.animation = sqirl_die

    def draw(self):
        if self.airborne and current_game_state == game_state.GAMEPLAY:
            frame = 2
        elif self.dead:
            frame = frame_counter % 3
        else:
            frame = frame_counter % 7
        screen.blit(self.animation.sprite(frame, 0), rect(self.x, self.y + 2, self.w, self.h))


class platform_base:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.w = random.randint(int(screen.width / 2), screen.width)
        self.h = 10
        self.keepout = 5

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x - self.keepout, self.y - self.keepout, self.w + (2 * self.keepout), self.h + (2 * self.keepout))

    def update(self):
        global score

        self.x -= foreground_scroll_speed

        if self.r <= 0:
            self.reset()
            while self.check_collisions():
                self.reset()
            score += 1
            if random.randint(0, 2):
                self.spawn_acorn()
        self.draw()

    def reset(self):
        self.x = screen.width
        self.y = random.randint(24, 110)
        self.w = random.randint(int(screen.width / 2), screen.width)

    def check_collisions(self):
        for platform in platforms:
            if platform.id == self.id:
                continue
            if self.bounding_box.intersects(platform.bounding_box):
                return True
        return False

    def spawn_acorn(self):

        acorn = acorn_base(random.randint(self.x, self.r - 10), self.y - 10)
        acorns.append(acorn)

    def draw(self):
        screen.pen = brush.image(branch, mat3().translate(self.x, self.y))
        player_box = shape.rectangle(self.x, self.y, self.w, self.h)
        screen.shape(player_box)


class acorn_base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def bounding_box(self):
        return rect(self.x, self.y, self.w, self.h)

    def move(self):
        self.x -= foreground_scroll_speed
        self.draw()

    def update(self):
        global score

        if self.bounding_box.intersects(player.bounding_box):
            acorns.remove(self)
            score += 3

        elif self.r < 0:
            acorns.remove(self)

    def draw(self):
        screen.blit(acorn_sml, vec2(self.x, self.y))


def centre_text(message, y):
    text_w, text_h = screen.measure_text(message)

    x = (screen.width - text_w) / 2

    screen.text(message, vec2(x, y))


def draw_background(scroll=True):
    global background_scroll_amount

    background_a_pos = background_scroll_amount
    background_b_pos = background_scroll_amount + background.width

    if scroll:
        background_scroll_amount -= background_scroll_speed
        background_scroll_amount %= -background.width

    screen.blit(background, vec2(background_a_pos, 0))
    screen.blit(background, vec2(background_b_pos, 0))


def draw_score():

    x = screen.width - 16
    y = 3

    acorn_coords = vec2(x, y)
    screen.blit(acorn_lg, acorn_coords)

    score_w, score_h = screen.measure_text(str(score))

    screen.font = score_font
    screen.pen = color.black

    x -= score_w
    y -= 5
    screen.text(str(score), vec2(x, y))

    x -= 2
    y -= 2
    screen.pen = color.brown
    screen.text(str(score), vec2(x, y))


def init_gamepad():
    global gamepad
    gamepads = qwstpad.Gamepadhelper()
    for i in gamepads.pads:
        if i is not None:
            gamepad = i
            return i
    return None


def parse_controls():
    global gamepad

    if gamepad:
        try:
            gamepad.update_buttons()
        except OSError:
            gamepad = init_gamepad()
    else:
        gamepad = init_gamepad()

    if gamepad:
        controls["MOVE_LEFT"] = gamepad.held("L")
        controls["MOVE_RIGHT"] = gamepad.held("R")
        controls["DROP"] = gamepad.held("D") and gamepad.pressed("A")
        controls["JUMP"] = gamepad.pressed("A")
        controls["JUMP_LEFT"] = gamepad.held("L") and gamepad.pressed("A")
        controls["JUMP_RIGHT"] = gamepad.held("R") and gamepad.pressed("A")
        controls["ANY_KEY"] = gamepad.pressed()
    else:
        controls["MOVE_LEFT"] = badge.held(BUTTON_A)
        controls["MOVE_RIGHT"] = badge.held(BUTTON_B)
        controls["DROP"] = badge.held(BUTTON_DOWN) and badge.pressed(BUTTON_C)
        controls["JUMP"] = badge.pressed(BUTTON_C)
        controls["JUMP_LEFT"] = badge.held(BUTTON_A) and badge.pressed(BUTTON_C)
        controls["JUMP_RIGHT"] = badge.held(BUTTON_B) and badge.pressed(BUTTON_C)
        controls["ANY_KEY"] = badge.pressed()


def init_platforms():
    global platforms
    platforms = [platform_base("a", 0, 50), platform_base("b", 40, 80), platform_base("c", 80, 110)]


background = image.load("assets/background.png")
branch = image.load("assets/branch.png")
sqirl_run = image.load("assets/running.png").spritesheet(7, 1)
sqirl_die = image.load("assets/death.png").spritesheet(4, 1)
acorn_sml = image.load("assets/acorn_sml.png")
title = image.load("assets/title.png")
gameover = image.load("assets/gameover.png")
title_font = font.yesterday
acorn_lg = image.load("assets/acorn_lg.png")
score_font = font.futile

gamepad = None
controls = {}

foreground_scroll_speed = 4
background_scroll_speed = 1
background_scroll_amount = 0
title_scroll_amount = 0

frame_counter = 0
player = player_base(20, 0)
platforms = []
acorns = []
current_game_state = game_state.TITLE
score = 0
last_frame = badge.ticks
last_anim_frame = badge.ticks
badge.default_clear = None

save_state = {"highscore": 0}
State.load("acorn_highway", save_state)

init_gamepad()
init_platforms()


def title_loop():
    global current_game_state, title_scroll_amount

    draw_background()

    screen.blit(title, vec2(0, 0))

    branch_y = 73
    branch_tex_matrix = mat3().translate(title_scroll_amount, branch_y)
    title_scroll_amount -= foreground_scroll_speed
    title_scroll_amount %= branch.width

    branch_bar = shape.rectangle(0, branch_y, screen.width, 10)
    screen.pen = brush.image(branch, branch_tex_matrix)
    screen.shape(branch_bar)

    sqirl_x = (screen.width - 32) / 2
    sqirl_y = 43
    frame = frame_counter % 7
    screen.blit(sqirl_run.sprite(frame, 0), rect(sqirl_x, sqirl_y, 32, 32))

    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)

    highscoretext = f"High score: {str(save_state["highscore"])}"
    centre_text(highscoretext, 85)

    if controls["ANY_KEY"]:
        current_game_state = game_state.GAMEPLAY


def gameplay_loop():
    global current_game_state

    draw_background()

    player.update()

    for acorn in acorns:
        acorn.move()

    for acorn in acorns:
        acorn.update()

    for platform in platforms:
        platform.update()

    draw_score()

    if player.b >= screen.height:
        player.death()
        current_game_state = game_state.DEATH_ANIM


def death_anim_loop():
    global current_game_state

    draw_background(False)

    player.update()

    for platform in platforms:
        platform.draw()

    draw_score()

    if player.b >= screen.height:
        current_game_state = game_state.GAMEOVER


def game_over_loop():
    global current_game_state, score

    screen.blit(gameover, vec2(0, 0))

    screen.font = title_font
    screen.pen = color.white

    if int(badge.ticks / 500) % 2:
        restarttext = "Press any button!"
        centre_text(restarttext, 100)

    scoretext = f"Your score: {str(score)}"
    centre_text(scoretext, 87)

    if score >= save_state["highscore"]:
        highscoretext = "High score!"
        save_state["highscore"] = score
        State.save("acorn_highway", save_state)
    else:
        highscoretext = f"High score: {str(save_state["highscore"])}"

    centre_text(highscoretext, 74)

    if controls["ANY_KEY"]:
        player.reset()
        init_platforms()
        score = 0
        acorns.clear()
        current_game_state = game_state.TITLE


while True:
    ticks = time.ticks_ms()

    if ticks - last_frame > 33:
        badge.poll()
        parse_controls()

        if current_game_state == game_state.TITLE:
            title_loop()
        elif current_game_state == game_state.GAMEPLAY:
            gameplay_loop()
        elif current_game_state == game_state.DEATH_ANIM:
            death_anim_loop()
        elif current_game_state == game_state.GAMEOVER:
            game_over_loop()

        if ticks - last_anim_frame > 83:
            frame_counter += 1
            last_anim_frame = ticks

        last_frame = ticks

        display.update()
