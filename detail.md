# ゼビウス風シューティングゲーム 詳細設計書

## 1. 添付書類
- [proposal.md](./proposal.md)
- [overview.md](./overview.md)

## 2. 使用する変数とその役割

### Player クラス
| 変数名 | 型 | 役割 |
|--------|----|------|
| x | float | プレイヤーのX座標 |
| y | float | プレイヤーのY座標 |
| speed | float | 移動速度 |
| shots | list | 発射した弾のリスト |
| bombs | list | 投下したボムのリスト |
| lives | int | 残機数 |
| score | int | スコア |
| target_x | float | 照準のX座標 |
| target_y | float | 照準のY座標 |
| invincible_time | int | 無敵時間 |
| shot_cooldown | int | ショットのクールダウン |
| bomb_cooldown | int | ボムのクールダウン |
| engine_anim | int | エンジンエフェクトのアニメーション |

### Enemy クラス
| 変数名 | 型 | 役割 |
|--------|----|------|
| x | float | 敵のX座標 |
| y | float | 敵のY座標 |
| type | str | 敵の種類 |
| health | int | 体力 |
| points | int | 倒した時のスコア |
| speed | float | 移動速度 |
| pattern | str | 移動パターン |
| color | int | 表示色 |
| angle | float | 移動角度 |
| formation_offset | float | 編隊のオフセット |

### GroundEnemy クラス
| 変数名 | 型 | 役割 |
|--------|----|------|
| x | float | 敵のX座標 |
| y | float | 敵のY座標 |
| type | str | 敵の種類 |
| health | int | 体力 |
| points | int | 倒した時のスコア |
| speed | float | 移動速度 |
| color | int | 表示色 |
| size | int | 表示サイズ |
| animation | int | アニメーションカウンター |

### Shot クラス
| 変数名 | 型 | 役割 |
|--------|----|------|
| x | float | 弾のX座標 |
| y | float | 弾のY座標 |
| speed | float | 移動速度 |

### Bomb クラス
| 変数名 | 型 | 役割 |
|--------|----|------|
| x | float | ボムのX座標 |
| y | float | ボムのY座標 |
| speed | float | 落下速度 |
| radius | float | 爆発半径 |
| exploded | bool | 爆発状態 |
| explosion_time | int | 爆発時間 |
| shockwave_radius | float | 衝撃波の半径 |

### Game クラス
| 変数名 | 型 | 役割 |
|--------|----|------|
| state | str | ゲームの状態 |
| player | Player | プレイヤーオブジェクト |
| enemies | list | 敵のリスト |
| ground_enemies | list | 地上の敵のリスト |
| wave | int | 現在のウェーブ |
| enemies_spawned | int | 出現した敵の数 |
| background | ScrollingBackground | 背景オブジェクト |

## 3. プログラムの全体の流れ

### 初期化処理
1. Pyxelの初期化
   - 画面サイズ：256x192
   - FPS：60
   - タイトル設定

2. リソースの読み込み
   - サウンドエフェクトの設定
   - 画像リソースの読み込み

3. ゲーム状態の初期化
   - プレイヤーの生成
   - 敵リストの初期化
   - 背景の初期化
   - ウェーブ数の設定

### メインループ
1. 入力処理
   - キーボード入力の検知
   - プレイヤーの移動
   - ショット/ボムの発射

2. 更新処理
   - プレイヤーの状態更新
   - 敵の生成と更新
   - 弾とボムの更新
   - 衝突判定
   - スコアの更新
   - ウェーブの進行

3. 描画処理
   - 背景の描画
   - プレイヤーの描画
   - 敵の描画
   - 弾とボムの描画
   - UI（スコア、ライフ）の描画

### ゲーム状態管理
1. タイトル画面
   - タイトル表示
   - スペースキーでゲーム開始

2. プレイ中
   - 通常のゲームプレイ
   - Pキーでポーズ

3. ポーズ中
   - ゲーム一時停止
   - Pキーで再開

4. ゲームオーバー
   - ゲームオーバー表示
   - スペースキーでリトライ

### 敵の生成と管理
1. 空中の敵
   - 定期的な生成
   - 種類に応じた移動パターン
   - 体力とスコアの管理

2. 地上の敵
   - 定期的な生成
   - 種類に応じた行動パターン
   - 体力とスコアの管理

### 衝突判定
1. プレイヤーと敵
   - 接触時のライフ減少
   - 無敵時間の管理

2. 弾と敵
   - 命中時の敵の体力減少
   - スコアの加算

3. ボムと地上の敵
   - 爆発範囲内の敵にダメージ
   - スコアの加算 