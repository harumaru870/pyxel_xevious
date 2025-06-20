import pyxel
import random
import math

class Player:
    def __init__(self):
        self.x = pyxel.width / 2
        self.y = pyxel.height - 40
        self.speed = 2.5
        self.shots = []
        self.bombs = []
        self.lives = 3
        self.score = 0
        self.target_x = self.x + 8
        self.target_y = self.y - 32
        self.invincible_time = 0
        self.shot_cooldown = 0
        self.bomb_cooldown = 0
        self.engine_anim = 0

    def update(self):
        if self.invincible_time > 0:
            self.invincible_time -= 1
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
            
        self.engine_anim += 1
        
        # Movement with smoother controls
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(8, self.x - self.speed)
            self.target_x = self.x + 8
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(pyxel.width - 24, self.x + self.speed)
            self.target_x = self.x + 8
        if pyxel.btn(pyxel.KEY_UP):
            self.y = max(16, self.y - self.speed)
            self.target_y = self.y - 32
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(pyxel.height - 24, self.y + self.speed)
            self.target_y = self.y - 32
            
        # Rapid fire for shots
        if pyxel.btn(pyxel.KEY_Z) and self.shot_cooldown == 0:
            self.shots.append(Shot(self.x + 6, self.y - 2))
            self.shots.append(Shot(self.x + 10, self.y - 2))
            pyxel.play(0, 0)
            self.shot_cooldown = 8
            
        # Bomb with cooldown
        if pyxel.btnp(pyxel.KEY_X) and self.bomb_cooldown == 0:
            self.bombs.append(Bomb(self.target_x, self.target_y))
            pyxel.play(1, 1)
            self.bomb_cooldown = 30
            
        # Update projectiles
        for shot in self.shots[:]:
            shot.update()
            if shot.y < -8:
                self.shots.remove(shot)
        for bomb in self.bombs[:]:
            bomb.update()
            if bomb.y > pyxel.height + 16:
                self.bombs.remove(bomb)

    def take_damage(self):
        if self.invincible_time == 0:
            self.lives -= 1
            self.invincible_time = 120
            pyxel.play(3, 4)
            return True
        return False

    def draw(self):
        # Draw player with blinking when invincible
        if self.invincible_time == 0 or self.invincible_time % 8 < 4:
            # Main body
            pyxel.rect(self.x + 4, self.y, 8, 16, 11)
            # Wings
            pyxel.rect(self.x, self.y + 6, 4, 8, 10)
            pyxel.rect(self.x + 12, self.y + 6, 4, 8, 10)
            # Engine flames
            if self.engine_anim % 8 < 4:
                pyxel.pset(self.x + 6, self.y + 16, 9)
                pyxel.pset(self.x + 9, self.y + 16, 9)
            else:
                pyxel.pset(self.x + 6, self.y + 16, 8)
                pyxel.pset(self.x + 9, self.y + 16, 8)
        
        # Draw target sight
        pyxel.rectb(self.target_x - 6, self.target_y - 6, 12, 12, 10)
        pyxel.line(self.target_x - 6, self.target_y, self.target_x + 6, self.target_y, 10)
        pyxel.line(self.target_x, self.target_y - 6, self.target_x, self.target_y + 6, 10)
        pyxel.circ(self.target_x, self.target_y, 1, 10)
        
        # Draw projectiles
        for shot in self.shots:
            shot.draw()
        for bomb in self.bombs:
            bomb.draw()

class Enemy:
    def __init__(self, enemy_type="toroid"):
        self.x = random.randint(16, pyxel.width - 32)
        self.y = -16
        self.type = enemy_type
        self.health = 1
        self.points = 100
        self.angle = 0
        self.formation_offset = random.random() * math.pi * 2
        
        if enemy_type == "toroid":
            self.speed = random.uniform(1.5, 2.5)
            self.pattern = random.choice(['straight', 'wave'])
            self.color = 8
        elif enemy_type == "garu":
            self.speed = random.uniform(2, 3)
            self.pattern = 'dive'
            self.color = 9
            self.points = 200
        elif enemy_type == "zakato":
            self.speed = random.uniform(1, 2)
            self.pattern = 'formation'
            self.color = 12
            self.points = 150

    def update(self):
        if self.pattern == 'straight':
            self.y += self.speed
        elif self.pattern == 'wave':
            self.y += self.speed
            self.x += math.sin(self.y / 15 + self.formation_offset) * 1.5
        elif self.pattern == 'dive':
            self.angle += 0.15
            self.y += self.speed + math.sin(self.angle) * 0.5
            if self.y > 60:
                self.x += math.cos(self.angle) * 2
        elif self.pattern == 'formation':
            self.y += self.speed
            self.x += math.sin(self.y / 20 + self.formation_offset) * 0.8
            
        # Keep enemies in bounds
        self.x = max(0, min(pyxel.width - 16, self.x))

    def draw(self):
        if self.type == "toroid":
            pyxel.circ(self.x + 8, self.y + 8, 6, self.color)
            pyxel.circ(self.x + 8, self.y + 8, 3, 0)
        elif self.type == "garu":
            pyxel.rect(self.x + 2, self.y, 12, 16, self.color)
            pyxel.rect(self.x, self.y + 4, 16, 8, self.color)
        else:  # zakato
            pyxel.rect(self.x + 4, self.y, 8, 16, self.color)
            pyxel.tri(self.x, self.y + 8, self.x + 4, self.y + 4, self.x + 4, self.y + 12, self.color)
            pyxel.tri(self.x + 12, self.y + 4, self.x + 16, self.y + 8, self.x + 12, self.y + 12, self.color)

class GroundEnemy:
    def __init__(self, enemy_type="domogram"):
        self.x = random.randint(16, pyxel.width - 32)
        self.y = pyxel.height - 16
        self.type = enemy_type
        self.health = 1
        self.points = 200
        self.animation = 0
        
        if enemy_type == "domogram":
            self.speed = random.uniform(0.5, 1.5)
            self.color = 4
            self.size = 16
        elif enemy_type == "barra":
            self.speed = random.uniform(1, 2)
            self.color = 6
            self.size = 24
            self.points = 500
            self.health = 2
        elif enemy_type == "logram":
            self.speed = random.uniform(0.3, 1)
            self.color = 5
            self.size = 20
            self.points = 300

    def update(self):
        self.animation += 1
        if self.type == "domogram":
            self.x += self.speed
            if self.x <= 0 or self.x >= pyxel.width - self.size:
                self.speed *= -1
        elif self.type == "barra":
            # Stationary tank
            pass
        else:  # logram
            self.x += self.speed * math.sin(self.animation / 30)

    def draw(self):
        if self.type == "domogram":
            # Simple tank design
            pyxel.rect(self.x, self.y + 8, self.size, 8, self.color)
            pyxel.rect(self.x + 4, self.y + 4, self.size - 8, 4, self.color)
            pyxel.rect(self.x + 6, self.y, 4, 4, self.color)
        elif self.type == "barra":
            # Large fortress
            pyxel.rect(self.x, self.y, self.size, 16, self.color)
            pyxel.rect(self.x + 4, self.y - 4, 16, 4, self.color)
            if self.animation % 60 < 30:
                pyxel.rect(self.x + 8, self.y - 8, 8, 4, 8)  # Blinking radar
        else:  # logram
            # Mobile unit
            pyxel.rect(self.x + 2, self.y + 4, self.size - 4, 12, self.color)
            pyxel.circ(self.x + 4, self.y + 10, 3, 1)
            pyxel.circ(self.x + self.size - 4, self.y + 10, 3, 1)

class Shot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 6

    def update(self):
        self.y -= self.speed

    def draw(self):
        pyxel.rect(self.x - 1, self.y, 2, 6, 7)

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.radius = 2
        self.exploded = False
        self.explosion_time = 0
        self.shockwave_radius = 0

    def update(self):
        if not self.exploded:
            self.y += self.speed
        else:
            self.explosion_time += 1
            self.radius += 0.5
            self.shockwave_radius += 1

    def explode(self):
        if not self.exploded:
            self.exploded = True
            pyxel.play(2, 3)

    def draw(self):
        if not self.exploded:
            # ボムの本体
            pyxel.circ(self.x, self.y, 3, 10)
            # ボムの尾
            for i in range(3):
                pyxel.pset(self.x - 1 + i, self.y - 2 - i, 7)
        else:
            # 爆発エフェクト
            colors = [10, 9, 8, 4]
            for i, color in enumerate(colors):
                if self.explosion_time > i * 3:
                    pyxel.circ(self.x, self.y, self.radius - i, color)
            
            # 衝撃波
            if self.shockwave_radius < 20:
                pyxel.circb(self.x, self.y, self.shockwave_radius, 7)
                pyxel.circb(self.x, self.y, self.shockwave_radius - 2, 8)

class ScrollingBackground:
    def __init__(self):
        self.offset = 0
        self.terrain = []
        self.generate_terrain()

    def generate_terrain(self):
        for i in range(0, pyxel.height + 40, 4):
            self.terrain.append({
                'y': i,
                'features': random.choice(['plain', 'forest', 'city', 'river'])
            })

    def update(self):
        self.offset += 1
        if self.offset >= 4:
            self.offset = 0
            # Add new terrain at top
            self.terrain.insert(0, {
                'y': -4,
                'features': random.choice(['plain', 'forest', 'city', 'river'])
            })
            # Remove terrain that's gone off screen
            if len(self.terrain) > 50:
                self.terrain.pop()
        
        # Update terrain positions
        for terrain in self.terrain:
            terrain['y'] += 1

    def draw(self):
        for terrain in self.terrain:
            y = terrain['y']
            if -8 <= y <= pyxel.height:
                if terrain['features'] == 'forest':
                    for x in range(0, pyxel.width, 16):
                        if random.random() < 0.3:
                            pyxel.circ(x + random.randint(0, 12), y, 2, 3)
                elif terrain['features'] == 'city':
                    for x in range(0, pyxel.width, 20):
                        if random.random() < 0.4:
                            h = random.randint(2, 6)
                            pyxel.rect(x + random.randint(0, 8), y - h, 8, h, 13)
                elif terrain['features'] == 'river':
                    pyxel.line(0, y, pyxel.width, y + 2, 12)
                    pyxel.line(0, y + 1, pyxel.width, y + 3, 5)

class Game:
    def __init__(self):
        pyxel.init(256, 192, title="XEVIOUS", fps=60)
        try:
            pyxel.load("assets.pyxres")
        except:
            self.create_sounds()
        self.state = "TITLE"
        self.background = ScrollingBackground()
        self.wave = 1
        self.enemies_spawned = 0
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def create_sounds(self):
        # ショット音（軽快な音）
        pyxel.sound(0).set(
            "c3e3g3c4",  # 音階
            "t",         # 音色
            "7",         # 音量
            "f",         # エフェクト
            10           # スピード
        )
        
        # ボム音（重厚な音）
        pyxel.sound(1).set(
            "f2c3f3c4",  # 音階
            "n",         # 音色
            "6",         # 音量
            "f",         # エフェクト
            20           # スピード
        )
        
        # 敵の撃破音
        pyxel.sound(2).set(
            "a3e4a4",    # 音階
            "n",         # 音色
            "5",         # 音量
            "f",         # エフェクト
            15           # スピード
        )
        
        # 爆発音
        pyxel.sound(3).set(
            "c2g2c3g3",  # 音階
            "n",         # 音色
            "4",         # 音量
            "f",         # エフェクト
            30           # スピード
        )
        
        # プレイヤーの被弾音
        pyxel.sound(4).set(
            "f1c2f2",    # 音階
            "n",         # 音色
            "3",         # 音量
            "f",         # エフェクト
            40           # スピード
        )

    def reset_game(self):
        self.player = Player()
        self.enemies = []
        self.ground_enemies = []
        self.explosions = []
        self.state = "TITLE"
        self.wave = 1
        self.enemies_spawned = 0
        self.background = ScrollingBackground()

    def spawn_enemies(self):
        # Spawn air enemies
        if pyxel.frame_count % max(40 - self.wave * 2, 15) == 0:
            enemy_types = ["toroid", "garu", "zakato"]
            weights = [0.6, 0.3, 0.1]
            enemy_type = random.choices(enemy_types, weights=weights)[0]
            self.enemies.append(Enemy(enemy_type))
            self.enemies_spawned += 1

        # Spawn ground enemies
        if pyxel.frame_count % max(120 - self.wave * 5, 60) == 0:
            ground_types = ["domogram", "barra", "logram"]
            weights = [0.7, 0.1, 0.2]
            ground_type = random.choices(ground_types, weights=weights)[0]
            self.ground_enemies.append(GroundEnemy(ground_type))

        # Wave progression
        if self.enemies_spawned >= 20 + self.wave * 5:
            self.wave += 1
            self.enemies_spawned = 0

    def update(self):
        if self.state == "TITLE":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "PLAY"
            return
        elif self.state == "PAUSE":
            if pyxel.btnp(pyxel.KEY_P):
                self.state = "PLAY"
            return
        elif self.state == "GAMEOVER":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
            return

        # PLAY state
        if pyxel.btnp(pyxel.KEY_P):
            self.state = "PAUSE"
            return

        self.background.update()
        self.player.update()
        self.spawn_enemies()

        # Update air enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y > pyxel.height + 16:
                self.enemies.remove(enemy)
                continue

            # Collision with player
            if (abs(enemy.x + 8 - self.player.x - 8) < 12 and 
                abs(enemy.y + 8 - self.player.y - 8) < 12):
                if self.player.take_damage():
                    self.enemies.remove(enemy)
                    if self.player.lives <= 0:
                        self.state = "GAMEOVER"
                continue

            # Collision with shots
            for shot in self.player.shots[:]:
                if (abs(enemy.x + 8 - shot.x) < 8 and 
                    abs(enemy.y + 8 - shot.y) < 8):
                    self.player.score += enemy.points
                    self.enemies.remove(enemy)
                    self.player.shots.remove(shot)
                    pyxel.play(2, 2)
                    break

        # Update ground enemies
        for ground_enemy in self.ground_enemies[:]:
            ground_enemy.update()

            # Collision with player
            if (abs(ground_enemy.x + ground_enemy.size//2 - self.player.x - 8) < ground_enemy.size//2 + 8 and
                abs(ground_enemy.y + 8 - self.player.y - 8) < 12):
                if self.player.take_damage():
                    if self.player.lives <= 0:
                        self.state = "GAMEOVER"
                continue

            # Collision with bombs
            for bomb in self.player.bombs[:]:
                distance = math.sqrt((ground_enemy.x + ground_enemy.size//2 - bomb.x)**2 + 
                                   (ground_enemy.y + 8 - bomb.y)**2)
                if distance < bomb.radius + ground_enemy.size//2:
                    ground_enemy.health -= 1
                    if ground_enemy.health <= 0:
                        self.player.score += ground_enemy.points
                        self.ground_enemies.remove(ground_enemy)
                    bomb.explode()
                    break

        # Update bombs
        for bomb in self.player.bombs[:]:
            bomb.update()
            if bomb.exploded and bomb.explosion_time > 20:
                self.player.bombs.remove(bomb)

    def draw(self):
        pyxel.cls(1)
        
        if self.state == "TITLE":
            self.draw_title()
        elif self.state == "PAUSE":
            self.draw_play()
            self.draw_pause()
        elif self.state == "GAMEOVER":
            self.draw_play()
            self.draw_gameover()
        else:
            self.draw_play()

    def draw_title(self):
        pyxel.cls(1)
        
        # Title screen with Xevious-style graphics
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 1)
        
        # Title
        pyxel.text(pyxel.width//2 - 32, 40, "X E V I O U S", 7)
        pyxel.text(pyxel.width//2 - 48, 60, "FARDRAUT SAGA", 10)
        
        # Instructions
        pyxel.text(pyxel.width//2 - 60, 100, "PRESS SPACE TO START", 8)
        pyxel.text(pyxel.width//2 - 80, 120, "ARROW KEYS: MOVE", 6)
        pyxel.text(pyxel.width//2 - 80, 130, "Z: SHOOT    X: BOMB", 6)
        pyxel.text(pyxel.width//2 - 80, 140, "P: PAUSE", 6)
        
        # Animated elements
        if pyxel.frame_count % 60 < 30:
            pyxel.text(pyxel.width//2 - 60, 160, "1984 NAMCO LTD.", 9)

    def draw_pause(self):
        pyxel.rect(60, 70, 136, 50, 0)
        pyxel.rectb(60, 70, 136, 50, 7)
        pyxel.text(pyxel.width//2 - 20, 85, "PAUSED", 8)
        pyxel.text(pyxel.width//2 - 48, 100, "PRESS P TO RESUME", 7)

    def draw_gameover(self):
        pyxel.rect(60, 70, 136, 50, 0)
        pyxel.rectb(60, 70, 136, 50, 7)
        pyxel.text(pyxel.width//2 - 32, 85, "GAME OVER", 8)
        pyxel.text(pyxel.width//2 - 60, 100, "PRESS SPACE TO RESTART", 7)

    def draw_play(self):
        # Draw scrolling background
        self.background.draw()
        
        # Draw game entities
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        for ground_enemy in self.ground_enemies:
            ground_enemy.draw()

        # Draw HUD
        pyxel.rect(0, 0, pyxel.width, 16, 0)
        pyxel.text(4, 4, f"SCORE: {self.player.score:06d}", 7)
        pyxel.text(120, 4, f"WAVE: {self.wave}", 7)
        pyxel.text(180, 4, f"LIVES: {self.player.lives}", 7)
        
        # Draw lives indicator
        for i in range(self.player.lives):
            pyxel.rect(220 + i * 12, 6, 8, 4, 11)

if __name__ == "__main__":
    Game()