## リプレイギャラリースクリーン ######################################
##
## ゲームから特定のシーンをリプレイするボタンを表示するシンプルなスクリーンです。
init python:

    # サムネイルの最大幅と高さを計算
    maxthumbx = config.screen_width / (3 + 1)
    maxthumby = config.screen_height / (3 + 1)

    # 現在のリプレイページ
    replay_page = 0

    # リプレイアイテムクラス
    class ReplayItem:
        def __init__(self, thumbs, replay, name):
            self.thumbs = thumbs  # サムネイル画像
            self.replay = replay  # リプレイするラベル
            self.name = name  # アイテム名

        def num_replay(self):
            # リプレイ可能なサムネイルの数を返す
            return len(self.thumbs)

    # リプレイアイテムをここに追加、以下のフォーマットを使用
    # Replay_items.append(ReplayItem(["サムネイル"], "コードからのラベル", "簡単な説明"))
    Replay_items = []
    Replay_items.append(ReplayItem(["Rthumb1"], "syou1", "{color=#000}一章{/color}"))
    #Replay_items.append(ReplayItem(["Rthumb1"], "main_gallery_images", "{color=#000}ギャラリー画像{/color}"))
    #Replay_items.append(ReplayItem(["Rthumb1"], "gallery_usage", "{color=#000}ギャラリー画像の表示方法{/color}"))
    #Replay_items.append(ReplayItem(["Rthumb1"], "replay_button", "{color=#000}リプレイボタンの設定{/color}"))
    #Replay_items.append(ReplayItem(["Rthumb1"], "replay_thumb_image", "{color=#000}リプレイサムネイルの設定{/color}"))
    #Replay_items.append(ReplayItem(["Rthumb1"], "replay_list_setup", "{color=#000}リプレイリストの設定{/color}"))
    #Replay_items.append(ReplayItem(["Rthumb1"], "finished", "{color=#000}最後に必要なこと{/color}"))

# 選択用の黒背景スクリーン
image black = "#000"

# リプレイギャラリー用のロック画像、ギャラリーを使用している場合は同じ画像を使用できます（希望する場合）
image replay_locked = "images/replay/replay_lock.jpg"

# 384x216 (16x9) 1280x720p、600x338 (16x9) 1920x1080でロックとサムネイルを設定
# リプレイサムネイル画像の設定はここで定義
image Rthumb1 = ("images/replay/replay_unlock.jpg")