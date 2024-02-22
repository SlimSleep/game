

import arcade
import arcade.gui as gui


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SKALE_MAP = 2
RIGHT_FACING = 0
LEFT_FACING = 1
SPEED = 5

GRAVITI = 1100
DEFAULT_DAMPING = 1
PLAYER_DAMPING = 0.4

PLAYER_FRACTION = 1
WALL_FRACTION = 0.7
DYNAMIC_ITEM_FRACTION = 0.6

PLAYER_MASS = 2.6

PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1900
PLAYER_MOVE_FORCE_ON_GROUND = 5000
PLAYER_JUMP_IMPULSE = 1490
def texture(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]
class Portal(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 3
        self.cur_texture = 0

        self.portal_texture = arcade.load_texture("cut_images_dj1aWWUuH7fZg1/image_part_001.png")
        self.texture = self.portal_texture

        self.runs = []

        for i in range(1, 10):
            textura = texture(f"cut_images_dj1aWWUuH7fZg1/image_part_00{i}.png")
            self.runs.append(textura)

    def update_animation(self, delta_time: float = 1 / 30):
        self.cur_texture = (self.cur_texture + 1) % 18
        self.texture = self.runs[self.cur_texture // 2][0]
class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.1
        self.cur_texture = 0

        self.coin_texture = arcade.load_texture("Silver/Silver_1.png")
        self.texture = self.coin_texture

        self.run = []

        for i in range(1, 11):
            textura = texture(f"Silver/Silver_{i}.png")
            self.run.append(textura)

    def update_animation(self, delta_time: float = 1 / 20):
        self.cur_texture = (self.cur_texture + 1) % 20
        self.texture = self.run[self.cur_texture // 2][0]

class Person(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.person_face = RIGHT_FACING
        self.cur_texture = 0
        self.scale = 1.6
        self.idle = True
        self.count = 0


        self.idles = arcade.load_texture("person/idle/Dude_Monster_Idle_4_1.png")
        self.texture = self.idles
        self.run_textures = []
        self.idle_texture = []

        for i in range(1, 5):
            texturka = texture(f"person/idle/Dude_Monster_Idle_4_{i}.png")
            self.idle_texture.append(texturka)


        for i in range(1, 7):
            texturka = texture(f"person/run/Dude_Monster_Run_6_{i}.png")
            self.run_textures.append(texturka)





    def update_animation(self, delta_time: float = 1 / 20):
        if self.change_x < 0 != (self.person_face == RIGHT_FACING):
            self.person_face = LEFT_FACING
        elif self.change_x > 0 != (self.person_face == LEFT_FACING):
            self.person_face = RIGHT_FACING
        self.count += 1
        if self.change_x == 0:
            self.cur_texture = (self.cur_texture + 1) % 8
            if self.count >= 6:
                self.texture = self.idle_texture[self.cur_texture // 2][self.person_face]
                self.count = 0

        if self.change_x != 0 and not self.idle:
            self.cur_texture = (self.cur_texture + 1) % 12
            if self.count >= 4:
                self.texture = self.run_textures[self.cur_texture//2][self.person_face]
                self.count = 0



class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.ground = None
        self.no_ground = None
        self.no_ground_1 = None
        self.no_ground_2 = None
        self.background = None
        self.background_1 = None
        self.person = None
        self.physics_engine = None
        self.left_pressed = False
        self.right_pressed = False
        self.camera = None
        self.coin_list = None
        self.block = None
        self.coin_len = None
        self.portal = None

        self.setup()

    def setup(self):
        map = "безымянный.json"
        tiled_map = arcade.load_tilemap(map, SKALE_MAP)
        self.ground = tiled_map.sprite_lists["Слой тайлов 1"]
        self.no_ground = tiled_map.sprite_lists["земля фон"]
        self.no_ground_1 = tiled_map.sprite_lists["забор"]
        self.no_ground_2 = tiled_map.sprite_lists["Забор"]
        self.background = arcade.load_texture("Final/Background_0.png")
        self.background_1 = arcade.load_texture("Final/Background_1.png")


        self.person = Person()
        self.person.center_x = 70
        self.person.center_y = 300
        corda = [(500, 750), (1225, 275), (1419, 275), (838, 802), (1032, 802), (2386, 732)]
        # corda = [(500, 250)]
        self.coin_list = arcade.SpriteList()
        for i in corda:
            coin = Coin()
            coin.position = i
            self.coin_list.append(coin)
        self.coin_len = len(self.coin_list)

        self.portal = Portal()
        self.portal.position = 2390, 320


        self.camera = arcade.Camera()

        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITI)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)
        self.physics_engine.add_sprite(self.person,
                                       friction=PLAYER_FRACTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        self.physics_engine.add_sprite_list(self.ground,
                                            friction=WALL_FRACTION,
                                            collision_type="ground",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.coin_list,
                                            friction=DYNAMIC_ITEM_FRACTION,
                                            collision_type="coin",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        def item_hit_handler(hero, item, _arbiter, _space, _data):
            item.kill()

        self.physics_engine.add_collision_handler("player", "coin",
                                              post_handler=item_hit_handler)

    def on_draw(self):
        self.clear()
        self.background.draw_sized(self.person.center_x, self.person.center_y,
                                SCREEN_WIDTH + 100, SCREEN_HEIGHT + 100)
        self.background_1.draw_sized(self.person.center_x, self.person.center_y,
                                SCREEN_WIDTH + 100, SCREEN_HEIGHT + 100)
        self.no_ground_1.draw()
        self.no_ground_2.draw()
        self.no_ground.draw()
        self.ground.draw()
        self.coin_list.draw()

        self.person.draw()
        if self.coin_len == 0:
            self.portal.draw()


    def on_update(self, delta_time: float):
        if self.person.center_y <= -100:
            rip = Rip()
            window.show_view(rip)
            self.person.center_y = SCREEN_HEIGHT // 2
            self.person.center_x = SCREEN_WIDTH // 2
        self.coin_len = len(self.coin_list)
        self.person.update_animation()
        if self.coin_len == 0:
            self.portal.update_animation()
        if self.coin_len == 0:
            if arcade.check_for_collision(self.person, self.portal):
                self.window.show_view(win_view)
                self.person.center_x = SCREEN_WIDTH // 2
                self.person.center_y = SCREEN_HEIGHT // 2

        for coin in self.coin_list:
            coin.update_animation()
        self.set_viewport()
        if self.left_pressed and not self.right_pressed:
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.person, force)
            self.physics_engine.set_friction(self.person, 0)
        elif self.right_pressed and not self.left_pressed:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.person, force)
            self.physics_engine.set_friction(self.person, 0)
        else:
            self.physics_engine.set_friction(self.person, 1.0)

        self.physics_engine.step()



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.person.change_x = -SPEED
            self.person.idle = False
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.person.change_x = SPEED
            self.person.idle = False
            self.right_pressed = True

        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            if self.physics_engine.is_on_ground(self.person):
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.person, impulse)



    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.person.change_x = 0
            self.left_pressed = False

        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.right_pressed = False
            self.person.change_x = 0




    def set_viewport(self):
        center_x = self.person.center_x
        center_y = self.person.center_y

        left = center_x - SCREEN_WIDTH / 2
        right = center_x + SCREEN_WIDTH / 2
        bottom = center_y - SCREEN_HEIGHT / 2
        top = center_y + SCREEN_HEIGHT / 2

        arcade.set_viewport(left, right, bottom, top)

class Menu_View(arcade.View):
    def __init__(self):
        super().__init__()
        self.game_view = None
        self.manager = gui.UIManager()
        self.manager.enable()

        self.game_box = gui.UIBoxLayout()
        play_anchor = gui.UIAnchorWidget(anchor_x="center",
                                         anchor_y="center",
                                         child=self.game_box)

        self.manager.add(play_anchor)

        start_key = gui.UIFlatButton(text="Играть", width=200)
        self.game_box.add(start_key.with_space_around(25))
        star_key = gui.UIFlatButton(text="Достижения", width=200)
        self.game_box.add(star_key.with_space_around(25))
        story_key = gui.UIFlatButton(text="История", width=200)
        self.game_box.add(story_key.with_space_around(25))

        start_key.on_click = self.on_click_start
        story_key.on_click = self.on_click_story

        self.backgrounds = arcade.load_texture("Final/Background_0.png")
        self.backgrounds_1 = arcade.load_texture("Final/Background_1.png")

    def on_click_start(self, event):
        level_view.manager.enable()
        window.show_view(level_view)
        self.manager.disable()

    def on_click_story(self, event):
        story = Story(menu_view)
        story.setup()
        window.show_view(story)
        self.manager.disable()



    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds)

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds_1)

        self.manager.draw()


class Levels(arcade.View):
    def __init__(self):
        super().__init__()
        self.backgrounds = arcade.load_texture("Final/Background_0.png")
        self.manager = gui.UIManager()
        self.manager.enable()

        self.game_box = gui.UIBoxLayout()
        play_anchor = gui.UIAnchorWidget(anchor_x="center",
                                         anchor_y="center",
                                         child=self.game_box)

        self.manager.add(play_anchor)

        start_key = gui.UIFlatButton(text="LEVEL-1", width=200)
        self.game_box.add(start_key.with_space_around(25))
        start_key_1 = gui.UIFlatButton(text="В разработке...", width=200)
        self.game_box.add(start_key.with_space_around(25))

        start_key.on_click = self.on_click_level

    def on_click_level(self, event):
        game = Game()
        window.show_view(game)
        self.manager.disable()


    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds)
        self.manager.draw()

class Rip(arcade.View):
    def __init__(self):
        super().__init__()
        self.backgrounds = arcade.load_texture("Final/Background_0.png")
        self.backgrounds_1 = arcade.load_texture("Final/Background_1.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds)

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds_1)

        arcade.draw_text("Вы проиграли", 300, SCREEN_HEIGHT // 2, (255, 255, 255), font_size=50)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        window.show_view(menu_view)
        menu_view.manager.enable()

class Win(arcade.View):
    def __init__(self):
        super().__init__()
        self.backgrounds = arcade.load_texture("Final/Background_0.png")
        self.backgrounds_1 = arcade.load_texture("Final/Background_1.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds)

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.backgrounds_1)

        arcade.draw_text("Вы выйграли", 300, SCREEN_HEIGHT // 2, (255, 255, 255), font_size=50)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        window.show_view(menu_view)
        menu_view.manager.enable()

class Story(arcade.View):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.text = None
        self.count = 0
        self.nummer = 0
        self.screen_text = ""
        self.start_text = 0


        self.num_str = 0

        self.spisok = []
        self.spisok_screen = []

    def setup(self):

        with open("Сюжет.txt", encoding="UTF-8") as text:
            self.text = text.read()
            len_text = len(self.text)
            self.start_text = 0
            for i in range(0, len_text + 1, 100):
                self.spisok.append(self.text[self.start_text:i])
                self.spisok_screen.append("")
                self.start_text = i
            self.spisok.append(self.text[self.start_text:])
            self.spisok_screen.append("")

    def on_draw(self):
        self.clear()
        y_text = (SCREEN_HEIGHT - 50)
        for i in self.spisok_screen:
            text = arcade.Text(i, 50, y_text, (0,255, 255))
            text.draw()
            y_text -= 50



    def update(self, delta_time: float):
        if self.num_str <= (self.start_text // 100) + 1:
            print(self.start_text)
            self.count += 1
            if self.count >= 1:
                self.count = 0
                self.spisok_screen[self.num_str] = self.spisok[self.num_str][:self.nummer]
                self.nummer += 1

                if self.nummer > 100:
                    self.nummer = 0
                    self.num_str += 1



window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
menu_view = Menu_View()
game_view = Game()
rip_view = Rip()
win_view = Win()
story_view = Story(menu_view)
level_view = Levels()
game_view.setup()



window.show_view(menu_view)
arcade.run()