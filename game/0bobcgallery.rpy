# BobCGallery コード by Bob Conway 2023
# バージョン 1.1 - 2023年10月30日 - サムネイルのフェードをmatrixcolorに更新
# バージョン 1.0 - 2023年6月15日 - 初回リリース
# Ren'Pyエンジンでの使用を想定

# Creative Commons 0 (CC0) ライセンスで利用可能
# クレジット表記は歓迎します。bobcgames.comへのリンクをお願いします

# ソフトウェアは「現状のまま」提供され、いかなる種類の保証もありません

############################################
#             使用方法                     #
############################################

# 1) このファイル (0bobcgallery.rpy) をRen'Pyプロジェクトのgame/フォルダに配置してください。

# 2) このフレームワークは、images/bobcgalleryディレクトリ以下のすべての画像ファイル
#    (jpg, png, webp) を自動的に取り込むことができます。この機能を使用しない場合は、
#    この値をTrueからFalseに変更してください。
#    この機能を使用するには、game/imagesフォルダの下に "bobcgallery" という名前の
#    ディレクトリを作成し、そこに画像を追加してください。例：
#    game/images/bobcgallery/cg0.png
#    game/images/bobcgallery/cgs/cg1.png
#    このように追加された画像は、拡張子なしのファイル名が「名前」になります。
#    例えば、cg0.pngは「cg0」という名前になります。
define BOBCGALLERY_AUTOIMPORT = True

# 3) ギャラリーに追加の画像を追加するには、以下に (名前, 画像) のタプルとして
#    定義できます。これはlayeredimageや手動で定義された画像値を含むすべての
#    displayablesで動作します。例えば、"eileencg happy" というlayeredimageを
#    "eileencg" という名前で追加するには、次の行を追加します：
#    ("eileencg", "eileencg happy"),
#    すべてのCGが上記のように自動インポートされる場合、このリストを変更する必要はありません。
#    画像は画面サイズ（例：1920x1080）である必要はありません。
define BOBCGALLERY_MANUAL_CGS = (
    (None, None),
    # 単一画像の例：
    #("eileen asleep", "images/cg/eileen_asleep.png"),
    # "image eileen beach = Composite((1920, 1080), (0,0), "eileen beach body", (0,0), "beach background")" として定義された画像の例
    #("eileen beach", "eileen beach"),
    # "layeredimage eileen coffeetime" として定義された画像の例
    #("eileen coffee", "eileen coffeetime"),
    )
    
# 4) デフォルトでは、フレームワークは上記のギャラリー画像リストに追加された
#    画像を検証します。この検証は*かなり*包括的であるはずですが、
#    問題が多すぎる場合は、ここで無効にできます。
define BOBCGALLERY_VALIDATE_MANUAL_CGS = True

# 5) このギャラリーは画面サイズではない画像（例：1920x1080）をサポートしていますが、
#    すべてが画面サイズである場合は、パフォーマンス向上のためにこれをFalseに設定してください。
define BOBCGALLERY_USE_NON_SCREEN_IMGS = True
    
# 6) デフォルトでは、自動インポートされたCGは手動で定義されたものの後に
#    ギャラリービューに含まれます。この動作を変更して最初に含めるには、
#    この値をTrueからFalseに変更してください。
define BOBCGALLERY_MANUALFIRST = True

# 7) この画面は基本的なギャラリービュー画面です。必要に応じてカスタマイズできます。
#    1ページあたりのCG数やサムネイルのサイズを決定する定数を変更することもできます。
# ページごとの画像数を9に設定
define BOBCGALLERY_PER_PAGE = 9

# サムネイルの最大幅を384ピクセルに設定
define BOBCGALLERY_THUMB_XMAXIMUM = 384

# サムネイルの最大高さを216ピクセルに設定
define BOBCGALLERY_THUMB_YMAXIMUM = 216

# サムネイル間の間隔を20ピクセルに設定
define BOBCGALLERY_THUMB_SPACING = 20

# ギャラリー画像切り替え時のトランジションを0.5秒のディゾルブに設定
define BOBCGALLERY_TRANSITION = Dissolve(0.5)

# ロックされた画像用のプレースホルダーを灰色の矩形として定義
image bobcgallery_locked_cg = Transform("#aaa", xysize=(BOBCGALLERY_THUMB_XMAXIMUM, BOBCGALLERY_THUMB_YMAXIMUM))

# サムネイル用のトランスフォーム：通常時は暗く、ホバー時に明るくなる
transform bobcgallery_thumb:
    matrixcolor TintMatrix("#666666")  # 通常時は暗い灰色
    on hover:
        linear 0.5 matrixcolor TintMatrix("#ffffff")  # ホバー時に白に変化（0.5秒）
    on idle:
        linear 0.5 matrixcolor TintMatrix("#666666")  # アイドル状態に戻る時も0.5秒かけて変化

# ギャラリー画面の定義
screen gallery():
    tag menu  # メニュータグを設定
    default pagenum = 0  # 初期ページ番号を0に設定
    use game_menu(_("ギャラリー"), scroll="viewport"):  # ゲームメニューを使用
        style_prefix "about"  # スタイルプレフィックスを"about"に設定
        hbox:
            box_wrap True spacing BOBCGALLERY_THUMB_SPACING box_wrap_spacing BOBCGALLERY_THUMB_SPACING  # サムネイルを配置するhbox
            for name, thm, img in BOBCGALLERY_IMAGE_SETS[pagenum]:  # 現在のページの画像セットをループ
                if name in persistent.bobcgallery_unlocked:  # 画像がアンロックされている場合
                    imagebutton idle thm at bobcgallery_thumb action Show("bobcgallery_showcg", img=img, transition=BOBCGALLERY_TRANSITION)  # アンロックされた画像を表示
                else:
                    add "bobcgallery_locked_cg"  # ロックされた画像を表示
    if BOBCGALLERY_NUM_SETS > 1:  # 複数のページがある場合
        hbox:
            xcenter 0.5 yalign 1.0 spacing 20  # ページナビゲーションを画面下部中央に配置
            textbutton _("<") action SetScreenVariable("pagenum", pagenum-1) sensitive pagenum > 0  # 前のページへのボタン
            for i in range(BOBCGALLERY_NUM_SETS):  # 各ページ番号のボタンを作成
                textbutton str(i + 1) action SetScreenVariable("pagenum", i) selected pagenum == i
            textbutton _(">") action SetScreenVariable("pagenum", pagenum+1) sensitive pagenum < (BOBCGALLERY_NUM_SETS-1)  # 次のページへのボタン
            

# 8) Ren'Pyプロジェクトのscreens.rpyを開き、"screen navigation():" を検索してください
#    （引用符なし）。そのスクリーンのPreferencesボタンの下に以下の行を追加してください
#    （先頭の#を除く）：
#        textbutton _("ギャラリー") action ShowMenu("bobcgallery")

#    コードは以下のようになるはずです（先頭の#を除く）：
#        textbutton _("設定") action ShowMenu("preferences")
#        textbutton _("ギャラリー") action ShowMenu("bobcgallery")
#    （新しいギャラリーボタンのインデントが合っていることを確認してください。）

# 9) CGをユーザーに表示する方法をカスタマイズしたい場合は、
#    この画面をカスタマイズできますが、必須ではありません。
define BOBCGALLERY_CGBG = "#000a"
screen bobcgallery_showcg(img):
    modal True
    zorder 99
    add BOBCGALLERY_CGBG
    add img fit "scale-down" xcenter 0.5 ycenter 0.5
    imagebutton idle "#fff0" action Hide("bobcgallery_showcg", transition=BOBCGALLERY_TRANSITION)
    
# 10) 画像を表示せずにギャラリーで画像をアンロックするには、
#     スクリプトで "galleryunlock <画像名>" と入力してください。
#     例えば、サンプルCG eileen asleepをアンロックするには、
#     galleryunlock eileen asleep と入力します。
#     画像をアンロック *かつ* ユーザーに表示するには、代わりに "gallery" を使用します。
#     gallery eileenasleep

#     例えば、eileen asleepをアンロックし、eileen beachを表示（およびアンロック）するには：
#     label my_test_label:
#         "アイリーンは眠っていましたが、あなたが起こしました。"
#         galleryunlock eileen asleep
#         "今、一緒にビーチに行きます！"
#         gallery eileen beach
#         "プレイヤーがCGを非表示にするためにクリックし、ゲームが続きます。"
    
#############################################
# ここから下は変更しないでください         #
#############################################

# （以下、コードの実装部分は変更せず、そのまま保持します）
default persistent.bobcgallery_unlocked = Set()

python early:
    def parse_bobcgallery(lexer):
        return lexer.rest()
    def bobcgallery_unlockonly(imgname):
        if imgname not in BOBCGALLERY_VALID_IMAGES:
            return
        persistent.bobcgallery_unlocked.add(imgname)
    def bobcgallery_unlockshow(imgname):
        if imgname not in BOBCGALLERY_VALID_IMAGES:
            return
        persistent.bobcgallery_unlocked.add(imgname)
        renpy.transition(BOBCGALLERY_TRANSITION)
        renpy.show_screen("bobcgallery_showcg", img=BOBCGALLERY_VALID_IMAGES[imgname])
    def lint_bobcgallery(imgname):
        if imgname not in BOBCGALLERY_VALID_IMAGES:
            renpy.error("Gallery image '" + imgname + "' was not recognized. Please ensure an image with that name was imported or manually added.")
    renpy.register_statement("galleryunlock", parse=parse_bobcgallery, execute=bobcgallery_unlockonly, lint=lint_bobcgallery)
    renpy.register_statement("gallery", parse=parse_bobcgallery, execute=bobcgallery_unlockshow, lint=lint_bobcgallery)

init 999 python:
    def bobcgallery_get_thumb(img):
        if BOBCGALLERY_USE_NON_SCREEN_IMGS:
            timg = Composite((config.screen_width, config.screen_height),(0,0), BOBCGALLERY_CGBG, (0,0), Fixed(Transform(img, fit="scale-down", xcenter=0.5, ycenter=0.5), xysize=(config.screen_width, config.screen_height)))
        else:
            timg = img
        return Transform(timg, xsize=BOBCGALLERY_THUMB_XMAXIMUM, ysize=BOBCGALLERY_THUMB_YMAXIMUM)
    def bobcgallery_append_manuals(allimgs):
        if len(BOBCGALLERY_MANUAL_CGS) <= 0:
            return
        validimages = renpy.list_images()
        for itm in BOBCGALLERY_MANUAL_CGS:
            if not isinstance(itm, tuple):
                renpy.error("BOBCGALLERY_MANUAL_CGS list had a badly-formatted item: " + str(itm))
                return
            if len(itm) != 2:
                renpy.error("BOBCGALLERY_MANUAL_CGS list had an item that was not name and image: " + str(itm))
            if itm == (None, None):
                continue
            if not isinstance(itm[0], str):
                renpy.error("BOBCGALLERY_MANUAL_CGS image name " + str(itm[0]) + " must be a string")
            if not isinstance(itm[1], str):
                renpy.error("BOBCGALLERY_MANUAL_CGS image " + str(itm[1]) + " must be a string")
            if BOBCGALLERY_VALIDATE_MANUAL_CGS:
                if itm[1] not in validimages:
                    if " " in itm[1]:
                        itmsplit = itm[1].split(" ")
                        itmfirst = itmsplit[0]
                        attrs = itmsplit[1:]
                        if itmfirst in validimages:
                            validattrs = renpy.get_ordered_image_attributes(itmfirst)
                            if validattrs is None or len(validattrs) == 0:
                                renpy.error("BOBCGALLERY_MANUAL_CGS image " + itm[1] + " has invalid attributes")
                            else:
                                for a in attrs:
                                    if a not in validattrs:
                                        renpy.error("BOBCGALLERY_MANUAL_CGS image " + itm[1] + " has invalid attribute " + str(a))
                    else:
                        renpy.error("BOBCGALLERY_MANUAL_CGS image " + itm[1] + " was not a valid image")
            allimgs.append((itm[0], bobcgallery_get_thumb(itm[1]), itm[1]))
    def bobcgallery_handle_autoimport(allimgs):
        for path in renpy.list_files():
            if path.startswith("images/gallery/"):
                pathlist = path.split("/")
                imgname = pathlist[-1]
                ridx = imgname.rindex(".")
                if ridx < 0:
                    renpy.error("Gallery image " + path + " did not have a file extension and will be skipped from auto-import")
                    continue
                namepart = imgname[0:ridx]
                suffixpart = imgname[ridx+1:]
                if suffixpart.lower() in ("jpg", "png", "webp"):
                    allimgs.append((namepart, bobcgallery_get_thumb(path), path))
                else:
                    BOBCGALLERY_LINT_ERRORS.add("Gallery image " + path + " was not a recognized extension (jpg, png, webp) and will be skipped from auto-import")
                    continue
    def bobcgallery_lint_badimages():
        if len(BOBCGALLERY_LINT_ERRORS) > 0:
            for err in BOBCGALLERY_LINT_ERRORS:
                print("\n" + err)
    config.lint_hooks.append(bobcgallery_lint_badimages)
    BOBCGALLERY_VALID_IMAGES = {}
    BOBCGALLERY_IMAGE_SETS = []
    BOBCGALLERY_LINT_ERRORS = Set()
    bobcgallery_all_images = []
    if BOBCGALLERY_MANUALFIRST:
        bobcgallery_append_manuals(bobcgallery_all_images)
    if BOBCGALLERY_AUTOIMPORT:
        bobcgallery_handle_autoimport(bobcgallery_all_images)
    if not BOBCGALLERY_MANUALFIRST:
        bobcgallery_append_manuals(bobcgallery_all_images)
    if len(bobcgallery_all_images) <= 0:
        renpy.error("You don't have any gallery images defined. Please add at least one image, via auto-import or in the manual list.")
    for nm, thmb, img in bobcgallery_all_images:
        BOBCGALLERY_VALID_IMAGES[nm] = img
    while len(bobcgallery_all_images) > BOBCGALLERY_PER_PAGE:
        BOBCGALLERY_IMAGE_SETS.append(tuple(bobcgallery_all_images[0:BOBCGALLERY_PER_PAGE]))
        bobcgallery_all_images = bobcgallery_all_images[BOBCGALLERY_PER_PAGE:]
    BOBCGALLERY_IMAGE_SETS.append(tuple(bobcgallery_all_images))
    del bobcgallery_all_images
    del BOBCGALLERY_MANUAL_CGS
    BOBCGALLERY_NUM_SETS = len(BOBCGALLERY_IMAGE_SETS)
