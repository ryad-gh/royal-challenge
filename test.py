import flet as ft
import random
import asyncio

# =============================================================
#  ✅ CLIENT CONFIG — ONLY EDIT THIS SECTION PER ORDER
# =============================================================

RECIPIENT_NAME = "her name"          # The person who will play
SENDER_NAME    = "your name"           # The person who made this

QUESTIONS = [
    "Do you remember the first time we met? 💭",
    "Do you think what we have is something rare? 💎",
    "Would you choose me all over again? 💛",
]

YES_MESSAGES = [
    "Of course you do... it was unforgettable 🌟",
    "Exactly. Don't ever forget that 👑",
    "I knew it. You always make the right choice 😏",
]

NO_MESSAGES = [
    "Wrong answer, {name}... the Titan is coming 😤",
    "Are you serious right now?! He's here 😤",
    "That's it. You asked for this 👿",
]

GIFT_TITLE    = "Your surprise is ready 🎁"
GIFT_MESSAGE  = "You completed the challenge! This was made with love just for you. ✨"

GALLERY_TITLE = "Our Moments ✨"
GALLERY_CAPTIONS = [
    "This one makes me smile every time 🥰",
    "Us, always 💛",
]

# Assets — place all files inside an /assets folder next to this script
ASSETS = {
    "titan":    "titan.png",       # punishment image
    "surprise": "image.png",       # gift reveal image
    "photo1":   "photo1.png",      # gallery photo 1
    "photo2":   "photo2.png",      # gallery photo 2
    "extra1":   "nounours.png",    # small decoration image
    "extra2":   "fleur.png",
    "extra3":   "stitch.png",
}

SOUNDS = {
    "tick":  "clock_tick.mp3",
    "titan": "titan_sound.mp3",
    "timer": "timer_sound.mp3",
    "happy": "happy.mp3",
    "yay":   "yay.mp3",
}

# Color theme — change to customize per order
THEME = {
    "bg":          "#001F3F",
    "card":        "#002B5B",
    "accent":      "#FFD700",
    "text":        "white",
    "danger":      "#FF4444",
    "btn_text":    "#001F3F",
}

# =============================================================
#  ✅ APP ENGINE — NO NEED TO EDIT BELOW
# =============================================================

async def main(page: ft.Page):
    page.title  = f"✨ The Royal Challenge — For {RECIPIENT_NAME} ✨"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = THEME["bg"]
    page.vertical_alignment   = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width  = 390
    page.window_height = 844
    page.padding = 0

    # --- Audio setup ---
    audios = {k: ft.Audio(src=v, autoplay=False) for k, v in SOUNDS.items()}
    page.overlay.extend(audios.values())

    state = {"current": 0, "no_clicks": 0}
    warnings = ["Are you sure? 🤔", "Last chance... ⚠️"]

    # ---------- helpers ----------

    def stop_all_audio():
        for a in audios.values():
            try:
                a.pause()
            except Exception:
                pass

    def play(name):
        try:
            audios[name].play()
        except Exception:
            pass

    def gold_btn(label, on_click, width=160, bgcolor=None, color=None):
        return ft.ElevatedButton(
            label,
            bgcolor  = bgcolor or THEME["accent"],
            color    = color   or THEME["btn_text"],
            width    = width,
            height   = 48,
            style    = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14)),
            on_click = on_click,
        )

    def screen_wrapper(content, scroll=False):
        return ft.Container(
            content=ft.Column(
                [content],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO if scroll else None,
            ),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=24, vertical=30),
        )

    # ---------- screens ----------

    def show_start_screen():
        stop_all_audio()
        state["current"]   = 0
        state["no_clicks"] = 0
        page.clean()

        page.add(screen_wrapper(
            ft.Column([
                ft.Text("👑", size=90, text_align="center"),
                ft.Text("THE ROYAL", size=34, weight="bold",
                        color=THEME["accent"], text_align="center"),
                ft.Text("CHALLENGE", size=34, weight="bold",
                        color=THEME["text"], text_align="center"),
                ft.Container(height=8),
                ft.Text(f"Made for {RECIPIENT_NAME} 💛",
                        size=16, color="#AACCFF", text_align="center"),
                ft.Container(height=40),
                gold_btn("BEGIN THE CHALLENGE →", lambda _: show_question(), width=220),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6)
        ))
        page.update()

    def show_question():
        stop_all_audio()
        play("timer")

        idx = state["current"]
        progress = f"Question {idx + 1} / {len(QUESTIONS)}"

        question_text = ft.Text(
            QUESTIONS[idx], size=22, weight="bold",
            color=THEME["text"], text_align="center"
        )
        warning_text = ft.Text("", size=16, color=THEME["accent"], weight="w600")

        def on_no_click(e):
            state["no_clicks"] += 1
            if state["no_clicks"] == 1:
                warning_text.value = warnings[0]
            elif state["no_clicks"] == 2:
                warning_text.value = warnings[1]
            else:
                show_titan_screen()
            page.update()

        def on_yes_click(e):
            stop_all_audio()
            play("tick")
            state["no_clicks"] = 0
            show_feedback_screen(YES_MESSAGES[idx])

        # progress bar
        prog_value = (idx) / len(QUESTIONS)
        progress_bar = ft.ProgressBar(
            value=prog_value, bgcolor="#003366",
            color=THEME["accent"], height=6
        )

        page.clean()
        page.add(screen_wrapper(
            ft.Column([
                ft.Text(progress, color=THEME["accent"], size=13, weight="bold"),
                progress_bar,
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column([
                        ft.Text("💭", size=36, text_align="center"),
                        question_text,
                        ft.Container(height=10),
                        warning_text,
                        ft.Container(height=16),
                        ft.Row([
                            gold_btn("✅  YES", on_yes_click, width=120,
                                     bgcolor="#1A6B3A", color="white"),
                            gold_btn("❌  NO",  on_no_click,  width=120,
                                     bgcolor="#6B1A1A", color="white"),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=28,
                    bgcolor=THEME["card"],
                    border_radius=22,
                    border=ft.border.all(2, THEME["accent"]),
                    width=340,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16)
        ))
        page.update()

    def show_feedback_screen(msg):
        page.clean()
        page.add(screen_wrapper(
            ft.Column([
                ft.Text("✨", size=64, text_align="center"),
                ft.Container(
                    content=ft.Text(msg, size=22, color=THEME["accent"],
                                    weight="bold", text_align="center"),
                    padding=24, bgcolor=THEME["card"],
                    border_radius=20, border=ft.border.all(1, THEME["accent"]),
                    width=320,
                ),
                ft.Container(height=20),
                gold_btn("CONTINUE  →", lambda _: next_question(), width=180),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        ))
        page.update()

    def show_titan_screen():
        stop_all_audio()
        play("titan")
        no_msg = NO_MESSAGES[state["current"]].replace("{name}", RECIPIENT_NAME)
        page.clean()
        page.add(screen_wrapper(
            ft.Column([
                ft.Text(no_msg, size=20, color=THEME["accent"],
                        weight="bold", text_align="center"),
                ft.Container(height=10),
                ft.Image(src=ASSETS["titan"], width=260, height=260,
                         fit=ft.ImageFit.CONTAIN),
                ft.Container(
                    content=ft.Text("YOU SHOULD HAVE SAID YES!", color=THEME["danger"],
                                    size=18, weight="bold", text_align="center"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=12),
                    bgcolor="#200000", border_radius=14,
                ),
                ft.Container(height=16),
                gold_btn("↩️  TRY AGAIN", lambda _: retry_question(), width=180),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14)
        ))
        page.update()

    def retry_question():
        audios["titan"].pause()
        state["no_clicks"] = 0
        show_question()

    def next_question():
        state["current"] += 1
        if state["current"] < len(QUESTIONS):
            show_question()
        else:
            stop_all_audio()
            play("yay")
            show_gift_screen()

    def show_gift_screen():
        page.clean()
        page.add(screen_wrapper(
            ft.Column([
                ft.Text("🔱", size=60, text_align="center"),
                ft.Text("MISSION COMPLETE", size=28, weight="bold",
                        color=THEME["text"], text_align="center"),
                ft.Text(f"Well done, {RECIPIENT_NAME}!", size=16,
                        color=THEME["accent"], text_align="center"),
                ft.Container(height=20),
                ft.Text("🎁", size=100, text_align="center"),
                ft.Container(height=20),
                gold_btn("OPEN YOUR GIFT 🎀", open_chest, width=220),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        ))
        page.update()

    async def open_chest(e):
        stop_all_audio()
        play("happy")
        page.clean()

        # confetti
        confetti_colors = ["#FFD700", "#FF69B4", "#00FF00", "#FF4500", "#00FFFF", "white"]
        confettis = [
            ft.Container(
                width=random.randint(6, 12),
                height=random.randint(6, 12),
                bgcolor=random.choice(confetti_colors),
                border_radius=random.randint(0, 6),
                left=random.randint(0, 300),
                top=random.randint(-200, -10),
                animate_position=ft.animation.Animation(
                    random.randint(1800, 3500), ft.AnimationCurve.EASE_IN
                ),
            )
            for _ in range(50)
        ]

        image_surprise = ft.Image(
            src=ASSETS["surprise"], width=300,
            fit=ft.ImageFit.CONTAIN, border_radius=20
        )

        page.add(
            ft.Column([
                ft.Text(GIFT_TITLE, size=22, weight="bold",
                        color=THEME["accent"], text_align="center"),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Stack([image_surprise] + confettis, width=300, height=300),
                    border_radius=22,
                    border=ft.border.all(2, THEME["accent"]),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Container(
                    content=ft.Text(GIFT_MESSAGE, size=15, italic=True,
                                    text_align="center", color=THEME["text"]),
                    padding=20, bgcolor=THEME["card"],
                    border_radius=16, width=310,
                ),
                ft.Row([
                    ft.Image(src=ASSETS["extra1"], width=75, border_radius=10),
                    ft.Image(src=ASSETS["extra2"], width=75, border_radius=10),
                    ft.Image(src=ASSETS["extra3"], width=75, border_radius=10),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ft.Container(height=4),
                gold_btn("SEE OUR MOMENTS  →", show_gallery_screen, width=220),
                gold_btn("↺  RESTART", lambda _: show_start_screen(),
                         width=160, bgcolor="#334466", color="white"),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               spacing=14, scroll=ft.ScrollMode.AUTO)
        )
        page.update()
        await asyncio.sleep(0.15)
        for c in confettis:
            c.top = 420
        page.update()

    async def show_gallery_screen(e=None):
        stop_all_audio()
        page.clean()

        fade = ft.animation.Animation(900, ft.AnimationCurve.EASE_IN_OUT)
        img1 = ft.Image(src=ASSETS["photo1"], width=300, border_radius=14,
                        opacity=0, animate_opacity=fade)
        img2 = ft.Image(src=ASSETS["photo2"], width=300, border_radius=14,
                        opacity=0, animate_opacity=fade)

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(GALLERY_TITLE, size=26, weight="bold",
                            color=THEME["accent"], text_align="center"),
                    ft.Container(height=10),
                    img1,
                    ft.Text(GALLERY_CAPTIONS[0], italic=True, size=15,
                            color="#AACCFF", text_align="center"),
                    ft.Divider(height=20, color="#334466"),
                    img2,
                    ft.Text(GALLERY_CAPTIONS[1], italic=True, size=15,
                            color="#AACCFF", text_align="center"),
                    ft.Container(height=24),
                    ft.Text(f"From {SENDER_NAME}, with love 💛",
                            size=14, color=THEME["accent"], text_align="center"),
                    ft.Container(height=16),
                    gold_btn("↺  PLAY AGAIN", lambda _: show_start_screen(), width=180),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   spacing=16, scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.symmetric(horizontal=24, vertical=30),
                expand=True,
            )
        )
        page.update()
        await asyncio.sleep(0.12)
        img1.opacity = 1
        img2.opacity = 1
        page.update()

    # --- launch ---
    show_start_screen()


import os
if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=int(os.environ.get("PORT", 8080)),
        host="0.0.0.0"
    )