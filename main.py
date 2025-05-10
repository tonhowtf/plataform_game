import pgzrun
import random
from pgzero.builtins import * # type: ignore
from pgzero.rect import Rect
import math

WIDTH = 1280
HEIGHT = 720
COLOR_BG = (20, 20, 30)
TILE_SIZE = 64
n_stage = 0

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class State:
    IDLE = 1
    WALK = 2
    JUMP = 3
    DASH = 4
    DASH_LEFT = 5
    WALK_LEFT = 6
    JUMP_LEFT = 7
    IDLE_LEFT = 8

class AnimatedSprite:
    def __init__(self, path, n_frame, speed_animation=5):
        self.path = path
        self.n_frame = n_frame
        self.speed_animation = speed_animation
        self.time = 0
        self.frame = 0
    
    def animation(self):
        self.time += 1
        if self.time > self.speed_animation:
            self.time = 0
            self.frame = (self.frame + 1) % self.n_frame
        return f'{self.path}{self.frame}'

class GameObject(Actor): # type: ignore
    def __init__(self, image, position, *groups):
        super().__init__(image, position)
        self.topleft = position 
        self.name = None
        self.groups = groups
        for group_item in self.groups: 
            if group_item is not None:
                group_item.append(self)
        self.time = 0
        self.frame = 0

    def update(self):
        pass

class Obj(GameObject):
    def __init__(self, image, position, *groups):
        super().__init__(image, position, *groups)
    
    def animation(self, path, total_frames, speed=5):
        self.time += 1
        if self.time > speed:
            self.time = 0
            self.frame = (self.frame + 1) % total_frames
        return f"{path}{self.frame}"
    
    def update(self):
        pass

class BgAnimated(GameObject): 
    def __init__(self, image, y_position):
        super().__init__(image, (0, y_position))
        self.y = y_position 

    def update(self, speed, limit, start_position):
        self.y += speed
        if self.y >= limit:
            self.y = start_position

    def draw(self):
        screen.blit(self.image, (0, self.y)) # type: ignore

class Bee(GameObject): 
    def __init__(self, image_dummy_arg, position, *groups): 
        self.walk_frames = ['obstacles/bee_a', 'obstacles/bee_b'] 
        self.rest_frame = 'obstacles/bee_rest'      
        super().__init__(self.rest_frame, position, *groups) 
        self.limit = 200.0
        self.patrol_start_x = float(self.x)
        self.patrol_end_x = float(self.x) + self.limit
        self.current_target_x = self.patrol_end_x 
        self.speed = 1.0
        self.STATE_MOVING = "moving"
        self.STATE_RESTING = "resting"
        self.state = self.STATE_MOVING 
        self.animation_timer = 0
        self.walk_animation_speed = 15 
        self.rest_duration = 60    
        self.rest_timer = 0
        self.current_walk_frame_index = 0
        
    def update(self):
        if self.state == self.STATE_MOVING:
            if self.x < self.current_target_x:
                self.x += self.speed
                if self.x >= self.current_target_x:
                    self.x = self.current_target_x
                    self.state = self.STATE_RESTING
                    self.image = self.rest_frame
                    self.rest_timer = 0
            elif self.x > self.current_target_x:
                self.x -= self.speed
                if self.x <= self.current_target_x:
                    self.x = self.current_target_x
                    self.state = self.STATE_RESTING
                    self.image = self.rest_frame
                    self.rest_timer = 0
            
            if self.state == self.STATE_MOVING:
                self.animation_timer += 1
                if self.animation_timer >= self.walk_animation_speed:
                    self.animation_timer = 0
                    self.current_walk_frame_index = (self.current_walk_frame_index + 1) % len(self.walk_frames)
                    self.image = self.walk_frames[self.current_walk_frame_index]
        
        elif self.state == self.STATE_RESTING:
            self.rest_timer += 1
            if self.rest_timer >= self.rest_duration:
                self.state = self.STATE_MOVING
                if self.current_target_x == self.patrol_end_x:
                    self.current_target_x = self.patrol_start_x
                else:
                    self.current_target_x = self.patrol_end_x
                self.image = self.walk_frames[self.current_walk_frame_index]

class Button(GameObject):
    def __init__(self, image, position, *groups):
        super().__init__(image, position, *groups)

class Fade:
    def __init__(self, group):
        self.alpha = 255
        self.speed = 10
        self.on = True
        self.call_fade = False
        self.group = group
        self.group.append(self)

    def fadein(self):
        self.on = True
        self.call_fade = True

    def update(self):
        if self.call_fade:
            if self.on:
                if self.alpha > 0:
                    self.alpha -= self.speed
                    if self.alpha < 0: self.alpha = 0 
                else:
                    self.call_fade = False
            else: 
                if self.alpha < 255:
                    self.alpha += self.speed
                    if self.alpha > 255: self.alpha = 255
                else:
                    self.call_fade = False

    def draw(self):
        if self.alpha > 0:
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (COLOR_BG[0], COLOR_BG[1], COLOR_BG[2], self.alpha)) # type: ignore

class Coin(Obj):
    def __init__(self, img, pos, *group):
        super().__init__(img, pos, *group)
    
    def update(self):
        self.image = self.animation('coin/', 5, 5)
        return super().update()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(3, 6)
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(0, 255))
        self.life = random.randint(40, 60)
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life -= 1

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.size, self.color) # type: ignore

class Player(Obj):
    def __init__(self, img, pos, collisions, group):
        super().__init__(img, pos, group)
        self.life = 3
        self.start_position = (0, 0)
        self.speed = 5
        self.jump_speed = -18
        self.gravity = 1
        self.direction = Vector2(0, 0)
        self.collisions = collisions
        self.image = 'player/base/base'
        self.collision_area = Rect(self.x, self.y, 40, 40)
        self.on_ground = False
        self.can_dash = False
        self.dash_speed = 4
        self.dash_timer = 1
        self.dash_duration = 1
        self.n_dash = 3
        self.time_dash = 0
        self.flip = False
        self.animations = {
            State.IDLE: AnimatedSprite('player/idle/', 7),
            State.IDLE_LEFT: AnimatedSprite('player/idlef/', 7),
            State.WALK: AnimatedSprite('player/walk/', 7),
            State.WALK_LEFT: AnimatedSprite('player/walkf/', 7),
            State.JUMP: AnimatedSprite('player/jump/', 1),
            State.JUMP_LEFT: AnimatedSprite('player/jumpf/', 1),
            State.DASH: AnimatedSprite('player/dash/', 1),
            State.DASH_LEFT: AnimatedSprite('player/dashf/', 1)
        }
        self.control_animation = self.animations[State.IDLE]
        self.current_animation = State.IDLE
            
    def return_to_start(self):
        self.x, self.y = self.start_position
        sounds.death.play() # type: ignore

    def drop_platform(self):
        if self.y > HEIGHT + 200:
            self.return_to_start()

    def y_collision_check(self):
        for sprite in self.collisions:
            if sprite.name == "platform":
                if sprite.colliderect(self):
                    if self.direction.y > 0:
                        self.direction.y = 0
                        self.bottom = sprite.top
                        self.on_ground = True
                    if self.direction.y < 0:
                        self.direction.y = 0
                        self.top = sprite.bottom
    
    def x_collision_check(self):
        for sprite in self.collisions:
            if sprite.name == "platform":
                if sprite.colliderect(self):
                    if self.direction.x > 0:
                        self.right = sprite.left
                    if self.direction.x < 0:
                        self.left = sprite.right
    
    def gravity_force(self):
        if not self.can_dash:
            if self.direction.y < 10:
                self.direction.y += self.gravity
            self.y += self.direction.y
    
    def move(self):
        if not self.can_dash:
            self.x += self.direction.x * self.speed
        else:
            if not self.flip:
                self.x += self.dash_speed * 5
            else:
                self.x -= self.dash_speed * 5

    def reset_dash(self, dash_move_speed=10):
        if self.can_dash:
            self.time_dash += 1
            if self.time_dash >= dash_move_speed:
                self.can_dash = False
                self.time_dash = 0
                self.direction.x = 0
            
    def limit_to_screen(self):
        self.x = max(64, min(self.x, 1216)) 
                
    def events(self):
        if not self.can_dash:
            if keyboard.left: # type: ignore
                self.direction.x = -1
                self.flip = True
            elif keyboard.right: # type: ignore
                self.direction.x = 1
                self.flip = False
            else:
                self.direction.x = 0
            if keyboard.z and self.on_ground: # type: ignore
                self.on_ground = False
                self.direction.y = self.jump_speed
                sounds.jump.play() # type: ignore
            if keyboard.x and not self.on_ground and self.n_dash > 0: # type: ignore
                self.can_dash = True
                self.n_dash -=1
                sounds.dash.play() # type: ignore
                if self.flip: self.direction.x = -self.dash_speed 
                else: self.direction.x = self.dash_speed
                self.direction.y = 0 
            
    def animation_stage(self):
        if self.can_dash and not self.on_ground:
            self.current_animation = State.DASH_LEFT if self.flip else State.DASH
        else:
            if self.on_ground and self.direction.x != 0:
                self.current_animation = State.WALK_LEFT if self.flip else State.WALK
            elif self.on_ground and self.direction.x == 0:
                self.current_animation = State.IDLE_LEFT if self.flip else State.IDLE
            elif not self.on_ground:
                self.current_animation = State.JUMP_LEFT if self.flip else State.JUMP
        if self.control_animation != self.animations[self.current_animation]:
            self.control_animation = self.animations[self.current_animation]

    def draw(self):
        overlay_image = self.control_animation.animation()
        screen.blit('player/base/base', (self.x - 20, self.y - 20)) # type: ignore
        screen.blit(overlay_image, (self.x - 30, self.y - 20)) # type: ignore

    def update(self):
        self.events()
        self.move()
        self.x_collision_check()
        self.gravity_force()
        self.y_collision_check()
        self.animation_stage()
        self.reset_dash()
        self.drop_platform()
        self.limit_to_screen()

BG_MAP = [  
    "S",  
    "C",  
    "C",  
    "S",  
    "S"   
]

MAP0 = [ 
    '                    ', 
    '                    ', 
    '                    ', 
    '                    ', 
    '                    ', 
    '                   ', 
    '                    ',  
    ' PAAAAAAAA O       C ', 
    'XXXXXXXXXXX   XXXXXX', 
    'XXXXXXXXXXX   XXXXXX', 
    'XXXXXXXXXXXSSSXXXXXX', 
    'XXXXXXXXXXXXXXXXXXXX', 
]

MAP1 = [
    '                    ', 
    '                    ', 
    '                    ', 
    '        A           ', 
    '      LGR           ', 
    '   A         A      ', 
    ' LGR    O    LGR    ', 
    '     LGR            ', 
    'P                  C', 
    'XXXXXXXXXXXXXXXXXXXX', 
    'XXXXXXXXXXXXXXXXXXXX', 
    'XXXXXXXXXXXXXXXXXXXX', 
]

MAP2 = [
    '                    ', 
    '            A       ', 
    '          LGR       ', 
    '      S S S         ', 
    '    LGGGGGGGR       ', 
    '  A               C ', 
    'LGR       O    LGR  ', 
    '    LGR             ', 
    'P     O             ', 
    'LGGGGGGGGGGGGGGGGGGR', 
    'XXXXXXXXXXXXXXXXXXXX', 
    'XXXXXXXXXXXXXXXXXXXX', 
]

MAP3 = [
    '    C               ', 
    '   LGR A            ', 
    '                    ', 
    'LGR     O    LGR    ', 
    'XXXXXX      XXXXXX    ', 
    '      AX            ', 
    'P                   ', 
    'LGR   LGR   LGR     ', 
    '                    ', 
    'SSSSSSSSSSSSSSSSSSSS', 
    'XXXXXXXXXXXXXXXXXXXX', 
    'XXXXXXXXXXXXXXXXXXXX', 
]

MAP4 = [
'XXXXXXXXXXXXXXXXXXXX',
'X                   ',
'X                   ',
'X           O     0 ',
'X                 XX',
'X                X  ',
'X      O      O X   ',
'X         X X  X    ',
'        X     X     ',
'  P   X     X       ',
'XXXXXSSSSSSSSSSSSSXX']

TEXT_INTRO = """Num despertar envolto em névoas prateadas, o guerreiro abriu os olhos sob um dossel vivo de folhas entrelaçadas que sussurravam histórias.
Seu coração bateu com estranha curiosidade,
pois ali não havia muralhas nem clarins, apenas o murmúrio antigo do vento e o aroma terroso de musgo molhado.

Você certamente acaba achando alguma coisa
se olhar mas nem sempre é a alguma coisa
que você estava procurando. """
GAMEOVER_TEXT = """GAME OVER! Suas forças falharam e as sombras venceram.
O véu das eras se fecha em torno de você.
FIM DE JOGO."""

class Scene:
    def __init__(self):
        self.new = self
        self.all_sprites = []
        self.collisions = []
        self.particles = []
        self.world_map = [MAP0, MAP1, MAP2, MAP3, MAP4] 

    def start_music(self, lib, music_name):
        try:
            if lib and hasattr(lib, 'play'):
                lib.play(music_name)
        except NameError:
            pass

    def create_particles(self, x, y):
        for _ in range(10):
            self.particles.append(Particle(x, y))
    
    def draw(self, screen_surface):
        pass

    def generate_bg(self, all_sprites_list):
        background_tile_image_paths = {
            'S': 'tiles/background_solid_sky.png',
            'C': 'tiles/background_clouds.png',
        }

        if not BG_MAP or len(BG_MAP) == 0:
            return
            
        num_cols_tiles = math.ceil(WIDTH / TILE_SIZE) 
        num_horizontal_bands = len(BG_MAP)
        current_band_start_y_pixel = 0 

        for band_index, band_tile_type_str in enumerate(BG_MAP):
            band_tile_char_key = None
            for char_candidate in band_tile_type_str:
                if char_candidate != ' ':
                    band_tile_char_key = char_candidate
                    break
            
            if band_index == num_horizontal_bands - 1:
                band_end_y_pixel = HEIGHT
            else:
                band_end_y_pixel = round((band_index + 1) * HEIGHT / num_horizontal_bands)

            if not band_tile_char_key or band_tile_char_key not in background_tile_image_paths:
                current_band_start_y_pixel = band_end_y_pixel 
                continue

            tile_image_to_use = background_tile_image_paths[band_tile_char_key]

            y_pixel_for_tile_row = current_band_start_y_pixel
            while y_pixel_for_tile_row < band_end_y_pixel:
                if y_pixel_for_tile_row >= HEIGHT:
                    break
                for col_tile_index in range(num_cols_tiles):
                    x_pixel_for_tile = col_tile_index * TILE_SIZE
                    if x_pixel_for_tile >= WIDTH:
                        break
                    Obj(tile_image_to_use, (x_pixel_for_tile, y_pixel_for_tile_row), all_sprites_list)
                y_pixel_for_tile_row += TILE_SIZE 
            current_band_start_y_pixel = band_end_y_pixel 

    def generate_map(self, all_sprites_list, collision_list, player_actor):
        global n_stage
        current_map_data = self.world_map[n_stage]
        default_platform_for_x = 'tiles/terrain_grass_block_center' 
        o2_sprite_width = 64 
        o2_sprite_height = 32 

        for row_idx, row_str in enumerate(current_map_data):
            for col_idx, tile_char in enumerate(row_str):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                image_to_load, is_platform, obj_name, object_instance = None, False, None, None
                terrain_path = 'tiles/' 
                if tile_char == 'G': image_to_load, is_platform = terrain_path + 'terrain_grass_block_top', True
                elif tile_char == 'L': image_to_load, is_platform = terrain_path + 'terrain_grass_block_top_left', True
                elif tile_char == 'R': image_to_load, is_platform = terrain_path + 'terrain_grass_block_top_right', True
                elif tile_char == 'F': image_to_load, is_platform = terrain_path + 'terrain_grass_block_center', True
                elif tile_char == 'E': image_to_load, is_platform = terrain_path + 'terrain_grass_block_left', True 
                elif tile_char == 'D': image_to_load, is_platform = terrain_path + 'terrain_grass_block_right', True 
                elif tile_char == "X": image_to_load, is_platform = default_platform_for_x, True 
                elif tile_char == "C": image_to_load, obj_name = 'tiles/4', "next" 
                elif tile_char == "O": 
                    object_instance = Bee('dummy_image_for_bee', (x, y), all_sprites_list, collision_list)
                    if object_instance: object_instance.name = "obstacle"
                elif tile_char == "S": 
                    image_to_load, obj_name = 'obstacles/o2', "obstacle" 
                elif tile_char == "A": 
                    coin_width, coin_height = 32, 32 
                    object_instance = Coin('coin/0', (x + (TILE_SIZE - coin_width)//2, y + (TILE_SIZE - coin_height)//2), all_sprites_list, collision_list) 
                    if object_instance: object_instance.name = "coin"
                elif tile_char == "0": image_to_load, obj_name = 'tiles/4', "theend" 
                elif tile_char == "P": 
                    player_actor.x, player_actor.y = x, y
                    player_actor.start_position = (x, y)

                if object_instance: pass 
                elif image_to_load:
                    current_pos = (x,y)
                    if tile_char == "S": 
                        current_pos_x = x + (TILE_SIZE - o2_sprite_width) // 2
                        current_pos_y = y + (TILE_SIZE - o2_sprite_height) 
                        current_pos = (current_pos_x, current_pos_y)
                    new_obj = Obj(image_to_load, current_pos, all_sprites_list, collision_list)
                    if is_platform: new_obj.name = "platform"
                    elif obj_name: new_obj.name = obj_name
            
    def on_mouse_down(self, pos): pass
    def on_key_down(self, key): pass
    def update(self): pass
    def change_scene(self, new_scene): self.new = new_scene
    
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.all_sprites = [] 
        self.menu_itens = {
            'bg1': BgAnimated('menu/bg', 360), 
            'bg2': BgAnimated('menu/bg', -360), 
            'title': Obj('menu/title', (WIDTH / 2 - 230, HEIGHT / 2 - 300), self.all_sprites),
            'button_play': Button('menu/text_start', (WIDTH / 2 - 57, HEIGHT / 2 + 50), self.all_sprites),
            'button_exit': Button('menu/text_exit', (WIDTH / 2 - 57, HEIGHT / 2 + 150), self.all_sprites)
        }
        self.fade = Fade(self.all_sprites)
        self.fade.fadein()
        self.start_music(music, 'menu') # type: ignore

    def draw(self, screen_surface): 
        self.menu_itens['bg1'].draw()
        self.menu_itens['bg2'].draw()
        for sprite in self.all_sprites:
            sprite.draw()
            
    def on_key_down(self, key):
        if key == keys.ESCAPE: quit() # type: ignore
        if key == keys.RETURN: self.change_scene(Intro()) # type: ignore

    def on_mouse_down(self, pos):
        if self.menu_itens['button_play'].collidepoint(pos):
            self.change_scene(Intro())
        elif self.menu_itens['button_exit'].collidepoint(pos):
            quit()

    def update(self):
        self.menu_itens['bg1'].update(speed=1, limit=1080, start_position=360)
        self.menu_itens['bg2'].update(1, 360, -360)
        for sprite in self.all_sprites:
            sprite.update()

class Intro(Scene):
    def __init__(self):
        super().__init__()
        self.all_sprites = []
        self.comands = Obj('menu/comands', (45, 550), self.all_sprites)
        self.button = Button('menu/text_play', (WIDTH - 120, HEIGHT - 100), self.all_sprites)
        self.fade = Fade(self.all_sprites)
        self.fade.fadein()

    def on_key_down(self, key):
        if key == keys.ESCAPE: quit() # type: ignore
        if key == keys.RETURN: # type: ignore
            self.start_music(music, 'game') # type: ignore
            self.change_scene(GameScene())

    def on_mouse_down(self, pos):
        if self.button.collidepoint(pos):
            self.start_music(music, 'game') # type: ignore
            self.change_scene(GameScene())

    def draw(self, screen_surface):
        screen_surface.fill(COLOR_BG)
        screen_surface.draw.text(TEXT_INTRO, (100, 100), color="white", fontsize=24) 
        for sprite in self.all_sprites:
            sprite.draw()
    
    def update(self):
        for sprite in self.all_sprites: sprite.update()
            
class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.all_sprites = [] 
        self.all_collisions = [] 
        self.generate_bg(self.all_sprites) 
        self.player = Player('player/idle/0', (100, 0), self.all_collisions, self.all_sprites) 
        self.generate_map(self.all_sprites, self.all_collisions, self.player)
        self.fade = Fade(self.all_sprites)
        self.fade.fadein()

    def draw(self, screen_surface):
        screen_surface.fill(COLOR_BG) 
        for sprite in self.all_sprites: 
            sprite.draw()
        for particle in self.particles:
            particle.draw()
        screen_surface.draw.text(f"Life: {self.player.life}", (50, 50), color="white", fontsize=30)
        screen_surface.draw.text(f"Dash: {self.player.n_dash}", (50, 90), color="white", fontsize=30)

    def check_collision(self):
        global n_stage
        player_collided_with_obstacle_this_frame = False

        for sprite in list(self.all_collisions): 
            if self.player.colliderect(sprite): 
                if sprite.name == "next":
                    n_stage += 1
                    if n_stage >= len(self.world_map):
                        self.change_scene(GameOver(won=True))
                    else:
                        self.change_scene(GameScene())
                    return 
                elif sprite.name == "obstacle" and not player_collided_with_obstacle_this_frame:
                    player_collided_with_obstacle_this_frame = True 
                    if self.player.life > 1:
                        self.player.life -= 1
                        sounds.death.play() # type: ignore
                        self.create_particles(self.player.x, self.player.y)
                        self.player.return_to_start()
                    else: 
                        self.player.life = 0 
                        self.change_scene(GameOver(won=False))
                    return 
                elif sprite.name == "theend":
                    self.change_scene(GameOver(won=True))
                    return 
                elif sprite.name == "coin":
                    if sprite in self.all_collisions: self.all_collisions.remove(sprite)
                    if sprite in self.all_sprites: self.all_sprites.remove(sprite)
                    sounds.coin.play() # type: ignore

    def update(self):
        for sprite in self.all_sprites: sprite.update() 
        for particle in list(self.particles): 
            particle.update()
            if particle.life <= 0: self.particles.remove(particle)
        self.check_collision()
        
class GameOver(Scene):
    def __init__(self, won=False): 
        super().__init__()
        self.all_sprites = [] 
        self.won = won
        self.button = Button('menu/text_play', (WIDTH /2 - 57, HEIGHT - 200), self.all_sprites) 
        self.fade = Fade(self.all_sprites)
        self.fade.fadein()
        if self.won:
            self.start_music(music, 'win') # type: ignore
            self.game_over_message = "As névoas se dissipam. O guerreiro triunfou, e a floresta agora sussurra seu nome entre as folhas. VITÓRIA!"
        else:
            self.start_music(music, 'gameover') # type: ignore
            self.game_over_message = GAMEOVER_TEXT
        global n_stage
        n_stage = 0 
            
    def on_key_down(self, key):
        if key == keys.ESCAPE: quit() # type: ignore
        if key == keys.RETURN: self.change_scene(MenuScene()) # type: ignore

    def on_mouse_down(self, pos):
        if self.button.collidepoint(pos): self.change_scene(MenuScene())

    def draw(self, screen_surface):
        screen_surface.fill(COLOR_BG)
        screen_surface.draw.text(self.game_over_message, 
                                 (WIDTH/2, 150), 
                                 centerx=WIDTH/2, 
                                 fontsize=30, 
                                 color="white", 
                                 width=WIDTH-200, 
                                 align="center", 
                                 lineheight=1.2)
        for sprite in self.all_sprites: sprite.draw()

    def update(self):
        for sprite in self.all_sprites: sprite.update()

current_scene = MenuScene()

def draw(): 
    current_scene.draw(screen) # type: ignore

def update():
    global current_scene
    current_scene.update()
    if current_scene.new != current_scene: 
        current_scene = current_scene.new

def on_mouse_down(pos): 
    current_scene.on_mouse_down(pos) 

def on_key_down(key): 
    current_scene.on_key_down(key)      

pgzrun.go()