# Pyxelゲーム `main.py` コード解説

## **はじめに**

本ドキュメントは、`pyxel`ライブラリを用いて制作されたシューティングゲーム`main.py`のソースコードを解説するものである。プログラムは複数のクラスによってオブジェクト指向的に構成されており、それぞれがゲーム内の特定の役割を担っている。

## **1. ライブラリのインポート**

```python
import pyxel
import random
import math
```

-   `import pyxel`: ゲームエンジンライブラリ`pyxel`をインポートする。画面描画、入力処理、サウンド再生など、ゲームの根幹をなす機能を提供する。
-   `import random`: 乱数を扱う`random`ライブラリをインポートする。主に敵の出現位置や種類の決定に利用される。
-   `import math`: 数学関数を提供する`math`ライブラリをインポートする。敵のサインカーブ移動など、複雑な動きの計算に用いる。

---

## **2. `Player` クラス**

プレイヤーが操作する自機を定義するクラスである。

```python
class Player:
    def __init__(self):
```

-   `class Player:`: `Player`クラスの定義を開始する。
-   `def __init__(self):`: コンストラクタ。`Player`オブジェクトが生成される際に一度だけ呼び出され、プロパティを初期化する。

```python
        self.x = pyxel.width / 2
        self.y = pyxel.height - 40
```

-   `self.x`: プレイヤーのX座標。画面の水平中央に初期化される。
-   `self.y`: プレイヤーのY座標。画面下部から40ピクセルの位置に初期化される。

```python
        self.speed = 2.5
        self.shots = []
        self.bombs = []
        self.lives = 3
        self.score = 0
```

-   `self.speed`: プレイヤーの移動速度。
-   `self.shots`: 発射された弾(`Shot`オブジェクト)を格納するリスト。
-   `self.bombs`: 投下された爆弾(`Bomb`オブジェクト)を格納するリスト。
-   `self.lives`: 残機。初期値は3である。
-   `self.score`: スコア。初期値は0である。

```python
        self.target_x = self.x + 8
        self.target_y = self.y - 32
```

-   `self.target_x`, `self.target_y`: 地上攻撃用の照準の座標。自機の位置を基準に設定される。

```python
        self.invincible_time = 0
        self.shot_cooldown = 0
        self.bomb_cooldown = 0
        self.engine_anim = 0
```

-   `self.invincible_time`: 被弾後の無敵時間を管理するタイマー。
-   `self.shot_cooldown`: ショットの連射間隔を制御するタイマー。
-   `self.bomb_cooldown`: ボムの投下間隔を制御するタイマー。
-   `self.engine_anim`: エンジンの噴射炎のアニメーション用カウンター。

### `update` メソッド

フレームごとにプレイヤーの状態を更新する。

```python
    def update(self):
        if self.invincible_time > 0:
            self.invincible_time -= 1
        # (shot_cooldown, bomb_cooldownも同様)
```

-   各種タイマーが0より大きい場合、フレームごとに1ずつデクリメントする。

```python
        # Movement with smoother controls
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(8, self.x - self.speed)
            self.target_x = self.x + 8
```

-   `pyxel.btn()`: キーが**押され続けている**間、`True`を返す。
-   `max(8, ...)`: プレイヤーが画面左端（X座標8）から外に出ないように制限する。
-   `RIGHT`, `UP`, `DOWN`キーも同様のロジックで移動処理と画面端の制限を行う。

```python
        # Rapid fire for shots
        if pyxel.btn(pyxel.KEY_Z) and self.shot_cooldown == 0:
            self.shots.append(Shot(self.x + 6, self.y - 2))
            self.shots.append(Shot(self.x + 10, self.y - 2))
            pyxel.play(0, 0)
            self.shot_cooldown = 8
```

-   Zキーが押されており、かつ`shot_cooldown`が0の場合にショットを発射する。
-   `self.shots.append()`: 新たな`Shot`オブジェクトを2つ生成し、リストに追加する。
-   `pyxel.play(0, 0)`: チャンネル0でサウンドID 0の音（ショット音）を再生する。
-   `self.shot_cooldown = 8`: クールダウンを設定し、連射速度を制限する。

```python
        # Bomb with cooldown
        if pyxel.btnp(pyxel.KEY_X) and self.bomb_cooldown == 0:
            self.bombs.append(Bomb(self.target_x, self.target_y))
            # ...
```

-   `pyxel.btnp()`: キーが**押された瞬間**にのみ`True`を返す。ボム投下のような単発のアクションに使用する。
-   `self.bombs.append()`: `Bomb`オブジェクトを照準の位置に生成する。

```python
        # Update projectiles
        for shot in self.shots[:]:
            shot.update()
            if shot.y < -8:
                self.shots.remove(shot)
```

-   `self.shots[:]`: リストの**コピー（スライス）**に対してループを実行する。これにより、ループ中に元のリストから安全に要素を削除できる。
-   `shot.update()`: 各弾丸オブジェクトの座標を更新する。
-   `self.shots.remove(shot)`: 画面外に出た弾丸をリストから削除し、メモリ負荷を軽減する。

### `take_damage` メソッド

被弾処理を行う。

```python
    def take_damage(self):
        if self.invincible_time == 0:
            self.lives -= 1
            self.invincible_time = 120
            # ...
            return True
        return False
```

-   `self.invincible_time == 0`の場合（無敵時間中でない場合）のみ、ライフを減らし、120フレーム（2秒）の無敵時間を設定する。
-   ダメージ処理が実行された場合は`True`、無敵で無視した場合は`False`を返す。

### `draw` メソッド

プレイヤー関連の描画を行う。

```python
    def draw(self):
        if self.invincible_time == 0 or self.invincible_time % 8 < 4:
            # ... (自機の描画処理)
```

-   この条件式により、無敵時間中は8フレーム周期で描画と非描画を繰り返し、点滅エフェクトを実現する。
-   `pyxel.rect()`, `pyxel.pset()`などの描画コマンドを使い、自機の形状やエンジンの炎を描画する。
-   `self.shots`と`self.bombs`リストをループし、各オブジェクトの`draw`メソッドを呼び出して弾丸と爆弾を描画する。

---

## **3. `Enemy` クラス (空中敵)**

空中の敵キャラクターを定義するクラスである。

```python
class Enemy:
    def __init__(self, enemy_type="toroid"):
        self.x = random.randint(16, pyxel.width - 32)
        # ...
        if enemy_type == "toroid":
            # ...
```

-   コンストラクタの引数`enemy_type`によって、生成する敵の性能（速度、移動パターン、得点など）を動的に変更する。

### `update` メソッド

```python
    def update(self):
        if self.pattern == 'straight':
            self.y += self.speed
        elif self.pattern == 'wave':
            self.y += self.speed
            self.x += math.sin(self.y / 15 + self.formation_offset) * 1.5
```

-   `self.pattern`プロパティの値に基づき、移動ロジックを分岐させる。
-   `'wave'`パターンでは`math.sin()`を使用し、Y座標の進行に応じてX座標を周期的に変化させ、波状の軌道を描く。

### `draw` メソッド

-   `self.type`プロパティの値に基づき、`pyxel.circ()`, `pyxel.rect()`, `pyxel.tri()`などを組み合わせて敵の形状を描画する。

---

## **4. `GroundEnemy` クラス (地上敵)**

地上の敵キャラクターを定義するクラスである。基本的な構造は`Enemy`クラスに準ずる。

```python
class GroundEnemy:
    # ...
    def update(self):
        if self.type == "domogram":
            # ... 左右往復移動
        elif self.type == "barra":
            pass # 静止
```

-   地上敵の種類に応じた移動パターンを`update`メソッドで実装する。`pass`は何もしない命令であり、静止している敵を表現する。

---

## **5. `Shot`, `Bomb` クラス (発射物)**

プレイヤーが発射する弾と爆弾のクラスである。

### `Shot` クラス

-   シンプルなオブジェクト。`update`メソッドでY座標を減算し、上方へ直進する。

### `Bomb` クラス

```python
class Bomb:
    # ...
    def update(self):
        if not self.exploded:
            self.y += self.speed
        else:
            self.explosion_time += 1
            # ...
```

-   `self.exploded`フラグによって、落下中と爆発後で`update`の処理を切り替える。爆発後は、エフェクト描画のためのタイマーや半径を更新する。

```python
    def explode(self):
        if not self.exploded:
            self.exploded = True
            pyxel.play(2, 3)
```

-   `self.exploded`を`True`に設定し、状態を「爆発後」に遷移させる。一度しか実行されないようにフラグで制御する。

---

## **6. `ScrollingBackground` クラス**

無限にスクロールする背景を管理するクラスである。

```python
class ScrollingBackground:
    # ...
    def update(self):
        # ...
        self.terrain.insert(0, { ... })
        if len(self.terrain) > 50:
            self.terrain.pop()
```

-   `self.terrain`リストの先頭(`insert(0, ...)`）に新しい地形データを追加し、末尾(`pop()`)から古いデータを削除することで、無限スクロールを実現している。

---

## **7. `Game` クラス (ゲーム本体)**

ゲーム全体の進行と状態を管理する中心的なクラスである。

```python
class Game:
    def __init__(self):
        pyxel.init(...)
        try:
            pyxel.load("assets.pyxres")
        except:
            self.create_sounds()
        self.state = "TITLE"
        # ...
        pyxel.run(self.update, self.draw)
```

-   `pyxel.init()`: Pyxelエンジンを初期化する。
-   `try...except`: `assets.pyxres`リソースファイルの読み込みを試行し、失敗した場合は`create_sounds()`でプログラム内定義の音源を使用するフォールバック処理。
-   `self.state`: `"TITLE"`, `"PLAY"`, `"GAMEOVER"` といったゲームの状態を保持する変数。この変数によって`update`と`draw`の挙動が変化する（State パターン）。
-   `pyxel.run(self.update, self.draw)`: ゲームのメインループを開始する。Pyxelが内部で`self.update`と`self.draw`を毎フレーム呼び出し続ける。

### `update` メソッド

-   `self.state`の値に応じて、タイトル画面の処理、プレイ中の処理、ゲームオーバー画面の処理へと分岐する。
-   プレイ中の処理では、全てのゲームオブジェクト（背景、プレイヤー、敵）の`update`メソッドを呼び出し、当たり判定を実行し、必要に応じて敵をスポーンさせる。

```python
        # Collision detection
        if (abs(enemy.x + 8 - self.player.x - 8) < 12 and 
            abs(enemy.y + 8 - self.player.y - 8) < 12):
            # ...
```

-   当たり判定は、2つのオブジェクトの中心点間のX距離とY距離が、それぞれの当たり判定サイズより小さいかどうかで判定する、単純な矩形衝突判定（AABB: Axis-Aligned Bounding Box）である。

### `draw` メソッド

-   `pyxel.cls(1)`: 毎フレームの描画開始時に、画面を指定色でクリアする。
-   `self.state`の値に応じて、`draw_title`, `draw_play`など、それぞれの場面に対応した描画メソッドを呼び出す。

```python
        # Draw HUD
        pyxel.text(4, 4, f"SCORE: {self.player.score:06d}", 7)
```

-   f-stringの書式指定 `{変数:06d}` を用いて、スコアを常に6桁のゼロ埋めで表示する。

---

## **8. ゲームの実行ブロック**

```python
if __name__ == "__main__":
    Game()
```

-   `__name__ == "__main__"`: このPythonスクリプトが直接実行された場合にのみ`True`となる定型構文。
-   `Game()`: `Game`クラスのインスタンスを生成する。これによりコンストラクタ(`__init__`)が実行され、ゲームが起動する。