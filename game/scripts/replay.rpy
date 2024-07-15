## リプレイギャラリースクリーン ######################################
## このファイルを変更する際は注意してください #################

# リプレイ終了用のボタンスクリーン
screen Replayexit():
    zorder 100
    # リプレイ終了ボタン。exit_hover.pngとexit_idle.pngの2つの画像が自動的に作成される
    imagebutton auto "images/replay/exit_%s.png" action EndReplay() yalign .99 xalign .99
            # exit_hover.pngとexit_idle.pngという2つの画像を自動で作成する
# リプレイ中に終了ボタンを表示したい場合は以下の2行を追加する（オプション）
# これはリプレイ用のラベルの後に追加する必要がある
#if _in_replay:
#        show screen Replayexit

# リプレイギャラリースクリーンの定義
# 変数の定義（スクリプトの適切な場所に配置してください）
define REPLAY_PER_PAGE = 9
define REPLAY_THUMB_XMAXIMUM = 384
define REPLAY_THUMB_YMAXIMUM = 216
define REPLAY_THUMB_SPACING = 20
define REPLAY_TRANSITION = Dissolve(0.5)

screen replay_gallery():
    tag menu
    default pagenum = 0  # 初期ページ番号を0に設定

    use game_menu(_("リプレイギャラリー"), scroll="viewport"):  # ゲームメニューを使用
        style_prefix "about"  # スタイルプレフィックスを"about"に設定

        hbox:
            box_wrap True spacing REPLAY_THUMB_SPACING box_wrap_spacing REPLAY_THUMB_SPACING  # サムネイルを配置するhbox
            for i in range(pagenum * REPLAY_PER_PAGE, min((pagenum + 1) * REPLAY_PER_PAGE, len(Replay_items))):
                if renpy.seen_label(Replay_items[i].replay):  # リプレイがアンロックされている場合
                    vbox:
                        imagebutton:
                            idle Replay_items[i].thumbs
                            action Replay(Replay_items[i].replay)
                            at replay_thumb  # ホバーエフェクトを適用
                        text Replay_items[i].name  # リプレイ項目の名前を表示
                else:
                    vbox:
                        add "replay_locked_cg"  # ロックされた画像を表示
                        text _("???")  # ロックされた項目の名前を隠す

    if len(Replay_items) > REPLAY_PER_PAGE:  # 複数のページがある場合
        hbox:
            xcenter 0.5 yalign 1.0 spacing 20  # ページナビゲーションを画面下部中央に配置
            textbutton _("<") action SetScreenVariable("pagenum", pagenum-1) sensitive pagenum > 0  # 前のページへのボタン
            for i in range((len(Replay_items) - 1) // REPLAY_PER_PAGE + 1):  # 各ページ番号のボタンを作成
                textbutton str(i + 1) action SetScreenVariable("pagenum", i) selected pagenum == i
            textbutton _(">") action SetScreenVariable("pagenum", pagenum+1) sensitive (pagenum + 1) * REPLAY_PER_PAGE < len(Replay_items)  # 次のページへのボタン

# リプレイボタンのスタイル定義は変更なし
style replay_button:
    hover_background "images/gallery/thumbs/hover.png"  # ホバー時の背景画像を設定

# ロックされた画像用のプレースホルダーを定義
image replay_locked_cg = Transform("#aaa", xysize=(REPLAY_THUMB_XMAXIMUM, REPLAY_THUMB_YMAXIMUM))

# サムネイル用のトランスフォーム
transform replay_thumb:
    matrixcolor TintMatrix("#666666")  # 通常時は暗い灰色
    on hover:
        linear 0.5 matrixcolor TintMatrix("#ffffff")  # ホバー時に白に変化（0.5秒）
    on idle:
        linear 0.5 matrixcolor TintMatrix("#666666")  # アイドル状態に戻る時も0.5秒かけて変化