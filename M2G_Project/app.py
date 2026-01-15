import flet as ft

# --- CONFIGURAZIONE ---
# NOTA: Ho RIMOSSO lo slash "/" iniziale. 
# Con assets_dir="assets", Flet cerca direttamente dentro quella cartella.
BOOKS_DATA = {
    "Lodi Mattutine": ["lodi1.jpg", "lodi2.jpg", "lodi3.jpg", "lodi4.jpg", "lodi5.jpg"],
    "Libretto": ["lib1.jpg", "lib2.jpg", "lib3.jpg", "lib4.jpg", "lib5.jpg"],
    "Foto ricordo": [] 
}

FEATHER_MAP = {
    "sunrise": "sunrise.svg", "book-open": "book-open.svg", "music": "music.svg", 
    "camera": "camera.svg", "chevron-right": "chevron-right.svg", "home": "home.svg", 
    "user": "user.svg", "arrow-left": "arrow-left.svg", "save": "save.svg", 
    "edit": "edit.svg", "play": "play-circle.svg", "pause": "pause-circle.svg", 
    "stop": "stop-circle.svg"
}

LYRICS_TEXT = """
Lo sai che ti amo
Ma a volte è difficile sai?
Io mi perdo, mi strappo
E arriviamo sempre allo stesso punto

Sono le nove e fuori piove
Il cielo è pieno di te
I tuoi capelli scintillano sotto la Luna
E la tua bianca pelle mi ricorda la radura

Il mio amore per te
È lapalissiano
Io so chi siamo
Solo quando sto con te
Ti respiro cosi forte
Da rimanerne asfissiato
E solo se ti metti di lato
Posso mostrarti con le mani
Quanto ti amo perché

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non dormirò
Li distruggo tutti e poi ripartirò (oooh)
(Dammi il tuo cuore baby)

"Hey pronto amore mio perché non vieni qui a casa mia?
Sono da sola... c'è la mia coperta calda che ti piace tanto, 
i pop corn... e poi guardiamo un film... dai che ho il ciclo 
e non mi sento tanto bene... allora ciao, a dopo amore..."

Sono le nove e fuori piove
Anche stasera un segone
Te l'ho detto
Se hai le mestruazioni non mi cercare
Se poi arrivo
E non possiamo più nemmeno scopare
Eppure sai che c'è
Sperimentiamo
Analizziamo
Di orifizi tu ne hai tre
Quando sto con te mi diventa duro
Mi devi dare il culo
Non lo diciamo a nessuno
Sborro come Nettuno

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non me la dai
Ti distruggo il culo mentre dormirai

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non me la dai
Ti distruggo il culo mentre dormirai

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non me la dai
Ti distruggo il culo mentre dormirai
E non importa
"""

COLORS = {
    "light": {
        "bg": "#f3f0e9", "primary": "#6a8a73", "text": "#1a1a1a", "text_sub": "#888888", 
        "card": "white", "icon_bg": "#dbe4de", "nav_bg": "white", "input_bg": "white",
        "paper_bg": "#fcfbf9", "paper_line": "#e0e6e3"
    },
    "dark": {
        "bg": "#1e1e1e", "primary": "#6a8a73", "text": "#ffffff", "text_sub": "#aaaaaa", 
        "card": "#2c2c2c", "icon_bg": "#3a3a3a", "nav_bg": "#2c2c2c", "input_bg": "#333333",
        "paper_bg": "#252525", "paper_line": "#3a3a3a"
    }
}

def main(page: ft.Page):
    # Configurazione iniziale minima
    page.title = "M2G App"
    page.bgcolor = "white"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    
    # --- AUDIO (Safe Load) ---
    audio_player = None
    try:
        # Percorso senza slash iniziale
        audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
        page.overlay.append(audio_player)
    except: pass

    # --- DATI ---
    def get_stored_data():
        try:
            saved_pic = page.client_storage.get("profile_pic") or "user.svg"
            # Pulizia percorsi Windows
            if "C:" in saved_pic or "\\" in saved_pic or saved_pic.startswith("/"): 
                saved_pic = "user.svg"
            
            return {
                "name": page.client_storage.get("user_name") or "Utente",
                "notes": page.client_storage.get("user_notes") or "",
                "font": float(page.client_storage.get("font_size") or 16.0),
                "dark": page.client_storage.get("dark_mode") or False,
                "pic": saved_pic
            }
        except:
             return {"name": "Utente", "notes": "", "font": 16.0, "dark": False, "pic": "user.svg"}
    
    data = get_stored_data()
    
    state = {
        "font_size": data["font"],
        "is_dark": data["dark"],
        "audio_playing": False
    }

    def get_c(key):
        return COLORS["dark" if state["is_dark"] else "light"][key]

    # --- FILE PICKER ---
    def on_file_picked(e):
        if e.files:
            path = e.files[0].path
            page.client_storage.set("profile_pic", path)
            img_profile_view.src = path
            img_profile_view.color = None
            nav_user_img.src = path
            nav_user_img.color = None
            nav_user_img.border_radius = 50
            page.update()
            
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # --- UI COMPONENTS ---
    
    # Header
    txt_welcome_name = ft.Text(f"Bentornato, {data['name']}", size=24, weight="w400")
    header_logo = ft.Container(width=65, height=65, border_radius=18, alignment=ft.Alignment(0, 0), content=ft.Text("M2G", color="white", size=22, weight="w300"))
    header_container = ft.Container(padding=ft.padding.only(top=20, bottom=20, left=20, right=20), content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, controls=[header_logo, txt_welcome_name]))

    # User Page
    is_svg_start = "user.svg" in data["pic"]
    img_profile_view = ft.Image(src=data["pic"], width=150, height=150, border_radius=75, fit="cover", color=get_c("primary") if is_svg_start else None)
    container_profile_border = ft.Container(content=img_profile_view, border_radius=100, padding=5, border=ft.border.all(3, "transparent"))
    
    txt_name_input = ft.TextField(value=data["name"], label="Il tuo nome", max_length=14)
    btn_upload_photo = ft.ElevatedButton("CARICA DALLA GALLERIA", color="white", on_click=lambda _: file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE))
    
    btn_open_notes_user = ft.Container(border_radius=10, padding=15, width=300) 
    lbl_font_size = ft.Text(f"Grandezza Testo: {int(state['font_size'])}")
    slider_font = ft.Slider(min=12, max=30, divisions=18, value=state["font_size"])
    switch_theme = ft.Switch(value=state["is_dark"])

    user_view_content = ft.Column(
        scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15,
        controls=[
            ft.Container(height=10),
            ft.Text("Il tuo Profilo", size=20, weight="bold"),
            container_profile_border,
            ft.Container(width=280, content=txt_name_input),
            ft.Divider(),
            btn_open_notes_user,
            ft.Divider(),
            btn_upload_photo,
            ft.Divider(),
            ft.Text("Impostazioni", size=18, weight="bold"),
            ft.Container(padding=10, content=ft.Column(controls=[
                ft.Row([ft.Text("Modalità Notte"), switch_theme], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                lbl_font_size,
                slider_font
            ])),
            ft.Container(height=120) 
        ]
    )

    # Note Page
    notes_input_full = ft.TextField(
        value=data["notes"], multiline=True, min_lines=30, max_length=10000,
        border=ft.InputBorder.NONE, text_size=state["font_size"], bgcolor="transparent", content_padding=ft.padding.only(top=5, left=5)
    )
    lines_background = ft.Column(spacing=0)
    btn_close_notes = ft.Container(padding=10, content=ft.Image(src=FEATHER_MAP["arrow-left"], width=24, height=24))
    btn_save_notes = ft.Container(padding=10, content=ft.Image(src=FEATHER_MAP["save"], width=24, height=24))
    
    notes_container = ft.Container(
        expand=True, padding=20,
        offset=ft.Offset(1, 0), animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        opacity=0, animate_opacity=300,
        content=ft.Column(controls=[
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                btn_close_notes,
                ft.Text("Le tue Note", size=20, weight="bold"),
                btn_save_notes
            ]),
            ft.Divider(color="transparent", height=10),
            ft.Container(
                expand=True, border_radius=5, padding=ft.padding.symmetric(horizontal=15, vertical=10),
                shadow=ft.BoxShadow(blur_radius=5, color="#22000000", offset=ft.Offset(2,2)),
                content=ft.Column(scroll="auto", controls=[ft.Stack(controls=[lines_background, notes_input_full])])
            )
        ])
    )

    # Reader Page
    reader_title = ft.Text("Titolo", size=20, weight="bold")
    reader_col = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    reader_scroll = ft.Column(scroll="auto", expand=True, controls=[reader_col], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    btn_close_reader = ft.Container(padding=10, content=ft.Image(src=FEATHER_MAP["arrow-left"], width=24, height=24))
    
    reader_container = ft.Container(
        expand=True, padding=0,
        offset=ft.Offset(1, 0), animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        opacity=0, animate_opacity=300,
        content=ft.Column(controls=[
            ft.Container(padding=20, content=ft.Row(controls=[btn_close_reader, ft.Container(width=10), reader_title])),
            ft.Divider(height=1, color="#e0e0e0"),
            ft.Container(expand=True, content=reader_scroll)
        ])
    )

    # Home & Nav
    cards_column = ft.Column(scroll="auto", spacing=20)
    dynamic_content = ft.Container(content=cards_column, expand=True, padding=ft.padding.symmetric(horizontal=25))
    btn_home_container = ft.Container(border_radius=10, padding=10, width=140)
    btn_user_container = ft.Container(border_radius=10, padding=10, width=140)
    
    nav_home_img = ft.Image(src=FEATHER_MAP["home"], width=20, height=20)
    nav_user_img = ft.Image(src=data["pic"], width=20, height=20, fit="cover", border_radius=50 if not is_svg_start else 0)

    custom_navbar = ft.Container(
        padding=15, border_radius=ft.border_radius.only(top_left=20, top_right=20),
        shadow=ft.BoxShadow(blur_radius=10, color="#11000000"),
        content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[btn_home_container, btn_user_container])
    )

    # --- LOGICA ---
    def update_interface_colors():
        c = get_c
        bg, fg, primary = c("bg"), c("text"), c("primary")
        page.bgcolor = bg
        header_logo.bgcolor = primary
        txt_welcome_name.color = fg
        
        # User colors
        txt_name_input.color = fg
        txt_name_input.border_color = primary
        btn_upload_photo.bgcolor = primary
        container_profile_border.border = ft.border.all(3, primary)
        
        is_svg = "user.svg" in img_profile_view.src
        img_profile_view.color = primary if is_svg else None
        
        btn_open_notes_user.bgcolor = primary
        btn_open_notes_user.content = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Image(src=FEATHER_MAP["edit"], width=20, height=20, color="white"),
            ft.Text("APRI LE TUE NOTE", color="white", weight="bold")
        ])
        
        user_view_content.controls[1].color = fg
        user_view_content.controls[9].color = fg
        user_view_content.controls[10].content.controls[0].controls[0].color = fg
        lbl_font_size.color = fg
        slider_font.active_color = primary
        switch_theme.active_color = primary

        # Note colors
        notes_container.bgcolor = bg
        notes_container.content.controls[0].controls[1].color = fg
        btn_close_notes.content.color = fg
        btn_save_notes.content.color = primary
        notes_container.content.controls[2].bgcolor = c("paper_bg")
        notes_input_full.color = fg
        lines_background.controls.clear()
        for _ in range(30): lines_background.controls.append(ft.Container(height=32, border=ft.border.only(bottom=ft.border.BorderSide(1, c("paper_line"))), width=float("inf")))

        # Reader colors
        reader_container.bgcolor = bg
        reader_title.color = fg
        btn_close_reader.content.color = fg

        # Navbar
        custom_navbar.bgcolor = c("nav_bg")
        is_home = dynamic_content.content == cards_column
        btn_home_container.bgcolor = primary if is_home else c("nav_bg")
        btn_home_container.content = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Image(src=FEATHER_MAP["home"], width=20, height=20, color="white" if is_home else fg), ft.Text("HOME", color="white" if is_home else fg, weight="bold")])
        
        is_svg_nav = "user.svg" in img_profile_view.src
        btn_user_container.bgcolor = primary if not is_home else c("nav_bg")
        user_icon_color = "white" if not is_home else fg
        if not is_svg_nav: user_icon_color = None
        btn_user_container.content = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Image(src=img_profile_view.src, width=20, height=20, fit="cover", border_radius=50 if not is_svg_nav else 0, color=user_icon_color), ft.Text("PROFILO", color="white" if not is_home else fg, weight="bold")])

        # Cards
        cards_column.controls.clear()
        for item in [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]:
            title, icon = item
            action = (lambda e, t=title: page.launch_url("https://biografieonline.it/img/bio/gallery/r/Robert_Oppenheimer_1.jpg")) if title == "Foto ricordo" else (lambda e, t=title: open_reader(t))
            cards_column.controls.append(ft.Container(
                bgcolor=c("card"), border_radius=22, padding=15, height=80, on_click=action,
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#0D000000", offset=ft.Offset(0, 5)),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row(controls=[
                        ft.Container(width=50, height=50, bgcolor=c("icon_bg"), border_radius=14, alignment=ft.Alignment(0, 0), content=ft.Image(src=FEATHER_MAP[icon], width=24, height=24, color=primary)),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=fg)
                    ]),
                    ft.Image(src=FEATHER_MAP["chevron-right"], width=24, color="#dddddd")
                ])
            ))
        cards_column.controls.append(ft.Container(height=50))
        page.update()

    def navigate(index):
        if index == 0: dynamic_content.content = cards_column
        else: dynamic_content.content = user_view_content
        update_interface_colors()

    def open_reader(title):
        reader_title.value = title
        reader_col.controls.clear()
        c = get_c
        reader_container.bgcolor = c("bg")
        reader_title.color = c("text")
        btn_close_reader.content.color = c("text")
        if title == "Inno":
            text_el = ft.Container(padding=20, content=ft.Text(LYRICS_TEXT, size=state["font_size"], color=c("text"), text_align="center"))
            
            icon_play = ft.Image(src=FEATHER_MAP["play"], width=30, height=30, color="white")
            label_play = ft.Text("RIPRODUCI", color="white", weight="bold")
            btn_play = ft.Container(bgcolor=c("primary"), border_radius=15, padding=15, width=250, content=ft.Row([icon_play, label_play], alignment=ft.MainAxisAlignment.CENTER))
            btn_stop = ft.Container(padding=10, content=ft.Column([ft.Image(src=FEATHER_MAP["stop"], width=24, height=24, color="red"), ft.Text("STOP", size=10, color="red")], spacing=2, alignment=ft.MainAxisAlignment.CENTER))
            
            def toggle_audio(e):
                if state["audio_playing"]:
                    if audio_player: audio_player.pause()
                    state["audio_playing"] = False
                    icon_play.src = FEATHER_MAP["play"]
                    label_play.value = "RIPRENDI"
                    btn_play.bgcolor = c("primary")
                else:
                    if audio_player: audio_player.play()
                    state["audio_playing"] = True
                    icon_play.src = FEATHER_MAP["pause"]
                    label_play.value = "PAUSA"
                    btn_play.bgcolor = "#d9534f"
                btn_play.update()
            
            def stop_audio(e):
                if audio_player:
                    audio_player.pause()
                    audio_player.seek(0)
                state["audio_playing"] = False
                icon_play.src = FEATHER_MAP["play"]
                label_play.value = "RIPRODUCI"
                btn_play.bgcolor = c("primary")
                btn_play.update()
            
            btn_play.on_click = toggle_audio
            btn_stop.on_click = stop_audio
            reader_col.controls.extend([ft.Container(height=20), ft.Row([btn_play, btn_stop], alignment=ft.MainAxisAlignment.CENTER), ft.Container(height=10), text_el, ft.Container(height=50)])
        else:
            if not BOOKS_DATA[title]: reader_col.controls.append(ft.Container(padding=20, content=ft.Text("Nessuna pagina qui.", color=c("text_sub"))))
            else:
                for img in BOOKS_DATA[title]: reader_col.controls.append(ft.Image(src=img, width=350, border_radius=5)); reader_col.controls.append(ft.Container(height=10))
        reader_container.offset = ft.Offset(0, 0)
        reader_container.opacity = 1
        reader_container.update()

    def close_reader(e):
        if state["audio_playing"]: 
            if audio_player: audio_player.pause()
            state["audio_playing"] = False
        reader_container.offset = ft.Offset(1, 0)
        reader_container.opacity = 0
        reader_container.update()

    def open_notes(e):
        notes_container.bgcolor = get_c("bg")
        lines_background.controls.clear()
        for _ in range(30): lines_background.controls.append(ft.Container(height=32, border=ft.border.only(bottom=ft.border.BorderSide(1, get_c("paper_line"))), width=float("inf")))
        notes_container.content.controls[2].bgcolor = get_c("paper_bg")
        notes_input_full.color = get_c("text")
        notes_container.offset = ft.Offset(0, 0)
        notes_container.opacity = 1
        notes_container.update()

    def close_notes(e):
        notes_container.offset = ft.Offset(1, 0)
        notes_container.opacity = 0
        notes_container.update()
        page.client_storage.set("user_notes", notes_input_full.value)

    def save_notes(e):
        page.client_storage.set("user_notes", notes_input_full.value)
        btn_save_notes.content.color = "green"
        btn_save_notes.update()

    def on_name_change(e):
        txt_welcome_name.value = f"Bentornato, {e.control.value}"
        page.client_storage.set("user_name", e.control.value)
        txt_welcome_name.update()

    def on_font_change(e):
        new_size = e.control.value
        state["font_size"] = new_size
        notes_input_full.text_size = new_size
        lbl_font_size.value = f"Grandezza Testo: {int(new_size)}"
        page.client_storage.set("font_size", new_size)
        lbl_font_size.update()
        notes_input_full.update()

    def on_theme_change(e):
        state["is_dark"] = e.control.value
        page.client_storage.set("dark_mode", state["is_dark"])
        update_interface_colors()

    # Bindings
    txt_name_input.on_change = on_name_change
    slider_font.on_change = on_font_change
    switch_theme.on_change = on_theme_change
    btn_open_notes_user.on_click = open_notes
    btn_close_notes.on_click = close_notes
    btn_save_notes.on_click = save_notes
    btn_close_reader.on_click = close_reader
    btn_home_container.on_click = lambda e: navigate(0)
    btn_user_container.on_click = lambda e: navigate(1)

    # Start
    mobile_screen = ft.Container(
        expand=True, 
        bgcolor="white", 
        content=ft.Stack(controls=[
            ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[header_container, dynamic_content, custom_navbar]),
            reader_container,
            notes_container
        ])
    )
    
    page.add(mobile_screen)
    update_interface_colors()

# IMPORTANTE: assets_dir="assets" (senza slash)
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
