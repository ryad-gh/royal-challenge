import flet as ft
import random
import asyncio
import os

async def main(page: ft.Page):
    page.title = "✨ THE ROYAL CHALLENGE ✨"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#001F3F"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # --- Audio elements (all preload) ---
    audio_tick = ft.Audio(src="clock_tick.mp3", autoplay=False, volume=1)
    audio_titan = ft.Audio(src="titan_sound.mp3", autoplay=False, volume=1)
    audio_timer = ft.Audio(src="timer_sound.mp3", autoplay=False, volume=1)
    audio_happy = ft.Audio(src="happy.mp3", autoplay=False, volume=1)
    audio_yay = ft.Audio(src="yay.mp3", autoplay=False, volume=1)

    page.overlay.extend([audio_tick, audio_titan, audio_timer, audio_happy, audio_yay])

    # Helper to play a sound with error handling
    def play_sound(sound):
        try:
            sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    # Helper to pause a sound safely
    def pause_sound(sound):
        try:
            sound.pause()
        except Exception as e:
            print(f"Error pausing sound: {e}")

    state = {"current": 0, "no_clicks": 0}

    questions = [
        "est ce que ryad special 3and maissa w dawilah glbah ki tweli tbiba nchalah?",
        "est ce que ryad gentelman, moubdi3, moumti3 and you enjoy your time with him?",
        "est ce que ryad et maissa ytwalmoo w maissa tdhak w tel3ab bch3arha ki tkhemem fih?"
    ]

    yes_msgs = [
        "bayna hadi My Future Doctor ani mriservi men drwk😉😂",
        "thank y maiss maiss you have a good taste😉😉✨",
        "ani 3arf fe9tlk ya setouta 😂😂😂😍"
    ]

    no_msgs = [
        "wach ya batala😂 wbali khask tclicii 3la no rohi diri yes tchof gatlah ana machi special w madawinich أعوذ بالله",
        "dersset la39el banetlek m3aya😂😂 w baghya diri no matehechmich😂😂",
        "wacha 3awelti 3la no 3labalk rahom yadbzo 3liya sema rah 3andk a limited edition"
    ]

    warnings = ["Are you sure? 🤔", "Last chance... ⚠️"]

    # --- GALERIE ---
    async def show_gallery_screen(e=None):
        page.clean()
        img1 = ft.Image(src="photo1.png", width=300, border_radius=10)
        img2 = ft.Image(src="photo2.png", width=300, border_radius=10)

        gallery_items = ft.Column.ft.Text("bon had le jour special hata li ya ana pcq fih jiti ntiya l had denya thank god for it w bsebtah 3reftek ana ya hbibti(wah hbibti w ma3ndek matgoli. had لقب ana meditholek (بما أنني احبكي فأنتي حبيبتي)(ntiya dicidi iyla ana hbibek ou no w nchalah rani hbibek)donc j'ai créé  cette chance pour te dir how much you are important to me and dahkatek w hadertek w afkarek w injazatek w majhoudatek w ntiya ka kol mouhima 3andi ghi ki nchof tswirtek nfrah w ki nchof dook 3aynin mama a mama 3la douk 3ynin ndoub fihom nghos fihom nkhrej m denya ga3. vous m'inspire bach nkhdem w nsiyii chaque jour bach nkon better version of my self and i'm serious about you pcq drwk rani nkteblek men gelbi (chkon hadi li ryad ydekhelha f hyatah w moukha w dirha un motivation et inspiration). rani ndir 3la jalek sawalah rebi 3alem bihom  manich ngolek bach nzoukh 3lik wela rani dayer fik plaisire 'non' rani ngolek haka bach nbiyenlek anou sah ana nbghik fi3la w 9awla w rani nchofek tstahli had te3b j'ai decouvrir un nouveu niveau d'amour jdid 3liya completement (yarebi tsde9li m3ak wela mchit f 60 dahya😂😂)ani 3arf wassm raki t3ichi chaque jour ghorba تخمام و صراعات و حروب نفسية يومية,و حزن والهمb w depretion w thessi rassk day3a w talfa w thessi rassk bahdek makanch li tkhewilah li may3tikch les solutions just ysma3lek tkherji wassm f glbk donc ana noglk anou rani hna ana dirlek ga3 had chi nchalah(soit tebghi wela ma tebghich) bon ga3 had hadra bach t3rfi beli 3andi tsway w raki une partie de ma vie li nemchilha ki mhawess nefrah nriyah w nhess b touma2nina.واختم ب: lahyferhak w yrz9ek ahdafek w 3icha li khasatek w ydwem 3lik feraha w dahk w familtek w yhafdek w t3ichi ferhana ga3 hyatek ✨ ") ", size=26, weight="bold", color="#FFD700", text_align="center"),
            img1,
            ft.Text("Ton premier jour à la clinique... 🩺", italic=True, size=16, text_align="center"),
            ft.Divider(height=20, color="transparent"),
            img2,
            ft.Text("Toujours avec le sourire ! 😊", italic=True, size=16, text_align="center"),
        ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO, spacing=20)

        page.add(
            ft.Container(
                content=ft.Column([
                    gallery_items,
                    ft.Container(height=20),
                    ft.ElevatedButton("RETOUR AU DÉBUT", on_click=lambda _: restart_game(), bgcolor="#FFD700", color="#001F3F", width=200)
                ], horizontal_alignment="center"),
                padding=20, expand=True
            )
        )
        page.update()

    def show_feedback_screen(text):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("✨", size=50),
                    ft.Text(text, size=28, color="#FFD700", weight="bold", text_align="center"),
                    ft.Text("💖", size=50),
                    ft.Container(height=20),
                    ft.ElevatedButton("CONTINUE →", bgcolor="#FFD700", color="#001F3F", on_click=lambda _: next_question())
                ], horizontal_alignment="center", spacing=10),
                expand=True
            )
        )

    def show_titan_with_msg(text):
        # Stop timer sound when Titan appears
        pause_sound(audio_timer)
        # Play titan sound
        play_sound(audio_titan)
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(text, size=22, color="#FFD700", weight="bold", text_align="center"),
                    ft.Image(src="titan.png", width=300, height=300, fit="contain"),
                    ft.Text("YOU SHOULD HAVE SAID YES!", color="red", size=20, weight="bold", text_align="center"),
                    ft.ElevatedButton("RETRY ↩️", bgcolor="#FFD700", color="#001F3F", on_click=lambda _: retry_after_titan())
                ], horizontal_alignment="center", spacing=15),
                expand=True
            )
        )

    def next_question():
        state["current"] += 1
        if state["current"] < len(questions):
            show_question()
        else:
            # Stop timer sound before showing gift screen
            pause_sound(audio_timer)
            play_sound(audio_yay)
            show_gift_screen()

    def retry_after_titan():
        # Stop titan sound when Retry is clicked
        pause_sound(audio_titan)
        state["no_clicks"] = 0
        show_question()

    def handle_yes(e):
        # Stop timer sound when Yes is clicked
        pause_sound(audio_timer)
        play_sound(audio_timer)   # optional second sound
        play_sound(audio_tick)    # optional second sound
        state["no_clicks"] = 0
        show_feedback_screen(yes_msgs[state["current"]])

    def show_question():
        # Stop any lingering sounds before starting new question
        pause_sound(audio_timer)
        pause_sound(audio_titan)
        # Play timer sound from the beginning
        audio_timer.seek(0)
        play_sound(audio_timer)

        question_text = ft.Text(questions[state["current"]], size=24, weight="bold", color="white", text_align="center")
        warning_text = ft.Text("", size=18, color="#FFD700", weight="w500", text_align="center")

        def on_no_click(e):
            state["no_clicks"] += 1
            if state["no_clicks"] == 1:
                warning_text.value = warnings[0]
            elif state["no_clicks"] == 2:
                warning_text.value = warnings[1]
            elif state["no_clicks"] >= 3:
                show_titan_with_msg(no_msgs[state["current"]])
            page.update()

        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Quest {state['current']+1}/3", color="#FFD700", weight="bold", text_align="center"),
                    question_text,
                    warning_text,
                    ft.Row([
                        ft.ElevatedButton("Yes", bgcolor="#FFD700", color="#001F3F", width=110, on_click=handle_yes),
                        ft.ElevatedButton("No", bgcolor="#FFD700", color="#001F3F", width=110, on_click=on_no_click),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], horizontal_alignment="center", spacing=20),
                padding=40, bgcolor="#002B5B", border_radius=25, border=ft.border.all(2, "#FFD700"),
                margin=20
            )
        )

    def show_gift_screen():
        # Ensure timer sound is stopped before displaying gift screen
        pause_sound(audio_timer)
        page.clean()
        page.add(
            ft.Column([
                ft.Text("🔱 MISSION COMPLETE 🔱", size=28, weight="bold", color="white", text_align="center"),
                ft.Text("🎁", size=120, text_align="center"),
                ft.ElevatedButton("OUVRIR LE CADEAU", width=200, height=50, bgcolor="#FFD700", color="#001F3F", on_click=open_chest),
            ], horizontal_alignment="center", spacing=30)
        )

    # --- SURPRISE ---
    async def open_chest(e):
        # Stop any lingering timer sound before playing happy sound
        pause_sound(audio_timer)
        play_sound(audio_happy)
        page.clean()

        # Static confetti row
        confetti_row = ft.Row(
            [
                ft.Container(
                    width=8, height=8,
                    bgcolor=random.choice(["#FFD700", "#FF69B4", "#00FF00", "#FF4500", "#00FFFF", "white"]),
                    border_radius=2,
                )
                for _ in range(40)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

        image_surprise = ft.Image(src="image.png", width=320, fit="contain", border_radius=25)
        mon_message = "Joyeux Anniversaire Maissa ! ❤️🩺"

        page.add(
            ft.Column(
                [
                    ft.Text("🎉 SURPRISE, MAISSA ! 🎉", size=32, weight="bold", color="#FFD700", text_align="center"),
                    ft.Container(
                        content=image_surprise,
                        border_radius=25,
                        border=ft.border.all(2, "#FFD700"),
                        padding=10,
                    ),
                    confetti_row,
                    ft.Container(
                        content=ft.Text(mon_message, size=16, italic=True, text_align="center"),
                        padding=20,
                        bgcolor="#003366",
                        border_radius=15,
                    ),
                    ft.Row(
                        [
                            ft.Image(src="nounours.png", width=80, height=80, fit="contain"),
                            ft.Image(src="fleur.png", width=80, height=80, fit="contain"),
                            ft.Image(src="stitch.png", width=80, height=80, fit="contain"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.ElevatedButton("SUIVANT →", on_click=show_gallery_screen, bgcolor="white", color="#001F3F", width=200),
                    ft.ElevatedButton("RESTART", on_click=lambda _: restart_game(), bgcolor="#FFD700", color="#001F3F", width=200),
                ],
                horizontal_alignment="center",
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
            )
        )
        page.update()

    def restart_game():
        # Stop all sounds before resetting
        pause_sound(audio_timer)
        pause_sound(audio_titan)
        pause_sound(audio_tick)
        pause_sound(audio_happy)
        pause_sound(audio_yay)
        state["current"] = 0
        state["no_clicks"] = 0
        show_start_screen()

    def show_start_screen():
        page.clean()
        page.add(
            ft.Column([
                ft.Text("🎮", size=100, text_align="center"),
                ft.Text("THE ROYAL CHALLENGE", size=30, weight="bold", text_align="center"),
                ft.Container(height=30),
                ft.ElevatedButton("BEGIN", width=200, height=50, on_click=lambda _: show_question(), bgcolor="#FFD700", color="#001F3F")
            ], horizontal_alignment="center", spacing=30)
        )

    show_start_screen()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=port,
        host="0.0.0.0",
        assets_dir="assets"
    )