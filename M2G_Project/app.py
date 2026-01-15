import flet as ft
import os
import sys
import subprocess
import shutil
import webbrowser

# --- 0. AUTO-INSTALLAZIONE PYGAME ---
try:
    import pygame
except ImportError:
    # Se siamo nell'exe, pygame è già impacchettato, quindi ignoriamo l'errore di pip
    if not getattr(sys, 'frozen', False):
        print("Installazione pygame...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

# --- 1. CONFIGURAZIONE PERCORSI INTELLIGENTE (PER EXE) ---

# A. PERCORSO ASSETS (Icone, MP3) -> Sola lettura
# Se è EXE, usa la cartella temporanea interna (_MEIPASS). Se è Script, usa la cartella corrente.
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# B. PERCORSO DATI (Salvataggi) -> Scrittura persistente
# Se è EXE, usa APPDATA (così i dati non si cancellano alla chiusura).
if getattr(sys, 'frozen', False):
    app_data_path = os.getenv('APPDATA')
    DATA_DIR = os.path.join(app_data_path, "M2G_App")
    # Crea la cartella in AppData se è la prima volta che apri l'app
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except:
            DATA_DIR = os.getcwd() # Fallback disperato
else:
    # Se stiamo sviluppando, salva qui vicino al file py
    DATA_DIR = BASE_DIR

# File di salvataggio puntati sulla cartella SICURA (DATA_DIR)
DATA_FILE = os.path.join(DATA_DIR, "user_data.txt")       
NOTES_FILE = os.path.join(DATA_DIR, "user_notes.txt")     
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.txt")    
PROFILE_PIC_FILE = os.path.join(DATA_DIR, "saved_profile.jpg") 

def get_path(filename):
    # Recupera risorse grafiche/audio
    return os.path.join(ASSETS_DIR, filename)

# --- FUNZIONI UTILITY ---
def load_file(filepath, default=""):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except: pass
    return default

def save_file(filepath, content):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(content))
    except: pass

def load_settings():
    settings = {"font_size": "16", "dark_mode": "False"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        settings[k] = v.strip()
        except: pass
    return settings

def save_settings_to_disk(font_size, dark_mode):
    try:
        with open(SETTINGS_FILE, "w") as f:
            f.write(f"font_size={font_size}\n")
            f.write(f"dark_mode={dark_mode}\n")
    except: pass

def get_current_profile_pic():
    if os.path.exists(PROFILE_PIC_FILE):
        return PROFILE_PIC_FILE
    return get_path("user.svg")

def main(page: ft.Page):
    try: pygame.mixer.init()
    except: pass

    # --- 2. STATO INIZIALE ---
    user_name_value = load_file(DATA_FILE, "Utente")
    user_notes_value = load_file(NOTES_FILE, "")
    current_settings = load_settings()
    
    current_font_size = float(current_settings["font_size"])
    is_dark_mode = (current_settings["dark_mode"] == "True")
    current_profile_src = get_current_profile_pic()
    audio_state = 0 

    # --- 3. COLORI DINAMICI ---
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

    def get_c(key):
        return COLORS["dark" if is_dark_mode else "light"][key]

    page.title = "M2G App"
    page.bgcolor = "#333333" 
    page.window_width = 400
    page.window_height = 850
    page.scroll = "adaptive"

    # --- 4. MAPPA ICONE ---
    feather_map = {
        "sunrise": "sunrise.svg", "book-open": "book-open.svg", "music": "music.svg", 
        "camera": "camera.svg", "chevron-right": "chevron-right.svg", "home": "home.svg", 
        "user": "user.svg", "arrow-left": "arrow-left.svg", "save": "save.svg", 
        "edit": "edit.svg", "play": "play-circle.svg", "pause": "pause-circle.svg", 
        "stop": "stop-circle.svg"
    }

    BOOKS_DATA = {
        "Lodi Mattutine": ["lodi1.jpg", "lodi2.jpg", "lodi3.jpg", "lodi4.jpg", "lodi5.jpg"],
        "Libretto": ["lib1.jpg", "lib2.jpg", "lib3.jpg", "lib4.jpg", "lib5.jpg"],
        "Foto ricordo": [] 
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

    # --- 5. COMPONENTI UI BASE ---
    
    # Header
    txt_welcome_name = ft.Text(f"Bentornato, {user_name_value}", size=24, color=get_c("text"), weight="w400")
    header_container = ft.Container(
        width=float("inf"), padding=ft.padding.only(top=20, bottom=20),
        content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, controls=[
            ft.Container(width=65, height=65, bgcolor=get_c("primary"), border_radius=18, alignment=ft.Alignment(0, 0), content=ft.Text("M2G", color="white", size=22, weight="w300")),
            txt_welcome_name
        ])
    )

    # --- 6. DEFINIZIONE CONTENITORI (PRIMA DELL'USO) ---
    
    # -- 6A. NOTES CONTAINER --
    lines_background = ft.Column(spacing=0, controls=[])
    def build_paper_lines(line_color):
        lines_background.controls.clear()
        for _ in range(30): 
            lines_background.controls.append(ft.Container(height=32, border=ft.border.only(bottom=ft.border.BorderSide(1, line_color)), width=float("inf")))
    build_paper_lines(get_c("paper_line"))

    notes_input_full = ft.TextField(
        value=user_notes_value, multiline=True, min_lines=30, max_length=10000,
        border=ft.InputBorder.NONE, text_size=current_font_size, color=get_c("text"), bgcolor="transparent", content_padding=ft.padding.only(top=5, left=5)
    )
    
    icon_save_notes = ft.Image(src=get_path(feather_map["save"]), width=24, height=24, color=get_c("primary"))
    
    def save_notes_action(e):
        save_file(NOTES_FILE, notes_input_full.value)
        icon_save_notes.color = "green" 
        icon_save_notes.update()

    def close_notes(e):
        notes_container.offset = ft.Offset(1, 0)
        notes_container.opacity = 0
        notes_container.update()
        nonlocal user_notes_value
        user_notes_value = notes_input_full.value
        save_file(NOTES_FILE, user_notes_value)

    notes_header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Container(padding=10, on_click=close_notes, content=ft.Image(src=get_path(feather_map["arrow-left"]), width=24, height=24, color=get_c("text"))),
            ft.Text("Le tue Note", size=20, weight="bold", color=get_c("text")),
            ft.Container(padding=10, on_click=save_notes_action, content=icon_save_notes)
        ]
    )

    paper_stack = ft.Stack(controls=[lines_background, notes_input_full])

    # DEFINIZIONE NOTES CONTAINER
    notes_container = ft.Container(
        width=375, height=812, bgcolor=get_c("bg"), padding=20,
        offset=ft.Offset(1, 0), animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        opacity=0, animate_opacity=300,
        content=ft.Column(controls=[
            notes_header,
            ft.Divider(color="transparent", height=10),
            ft.Container(
                expand=True,
                bgcolor=get_c("paper_bg"),
                border_radius=5,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                shadow=ft.BoxShadow(blur_radius=5, color="#22000000", offset=ft.Offset(2,2)),
                content=ft.Column(scroll="auto", controls=[paper_stack])
            )
        ])
    )

    def open_notes_page(e):
        notes_container.bgcolor = get_c("bg")
        notes_container.content.controls[2].bgcolor = get_c("paper_bg")
        build_paper_lines(get_c("paper_line"))
        notes_input_full.color = get_c("text")
        icon_save_notes.color = get_c("primary")
        notes_container.offset = ft.Offset(0, 0)
        notes_container.opacity = 1
        notes_container.update()

    # -- 6B. READER CONTAINER --
    reader_title = ft.Text("Titolo", size=20, weight="bold", color=get_c("text"))
    pages_column = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    scroll_container = ft.Column(scroll="auto", expand=True, controls=[pages_column], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def close_reader(e):
        try: pygame.mixer.music.stop()
        except: pass
        nonlocal audio_state
        audio_state = 0
        reader_container.offset = ft.Offset(1, 0)
        reader_container.opacity = 0
        reader_container.update()

    # DEFINIZIONE READER CONTAINER
    reader_container = ft.Container(
        width=375, height=812, bgcolor=get_c("bg"), padding=0,
        offset=ft.Offset(1, 0), animate_offset=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        opacity=0, animate_opacity=300,
        content=ft.Column(controls=[
            ft.Container(padding=20, content=ft.Row(controls=[
                ft.Container(padding=10, on_click=close_reader, content=ft.Image(src=get_path(feather_map["arrow-left"]), width=24, height=24, color=get_c("text"))),
                ft.Container(width=10), reader_title
            ])),
            ft.Divider(height=1, color="#e0e0e0"),
            ft.Container(expand=True, content=scroll_container)
        ])
    )

    def open_reader(e, title):
        nonlocal audio_state
        reader_title.value = title
        reader_title.color = get_c("text")
        pages_column.controls.clear()
        reader_container.bgcolor = get_c("bg")
        reader_container.offset = ft.Offset(0, 0)
        reader_container.opacity = 1
        reader_container.update()
        
        if title == "Inno":
            text_element = ft.Container(padding=20, content=ft.Text(LYRICS_TEXT, size=current_font_size, color=get_c("text"), text_align="center"))
            audio_path = get_path("inno.mp3")
            if os.path.exists(audio_path):
                try:
                    pygame.mixer.music.load(audio_path)
                    if not pygame.mixer.music.get_busy(): audio_state = 0
                except: pass
                
                icon_play = ft.Image(src=get_path(feather_map["play"]), width=30, height=30, color="white")
                label_play = ft.Text("RIPRODUCI", color="white", weight="bold")
                btn_play = ft.Container(bgcolor=get_c("primary"), border_radius=15, padding=15, width=250, content=ft.Row([icon_play, label_play], alignment=ft.MainAxisAlignment.CENTER), on_click=lambda e: toggle_audio(e))
                btn_stop = ft.Container(padding=10, content=ft.Column([ft.Image(src=get_path(feather_map["stop"]), width=24, height=24, color="red"), ft.Text("STOP", size=10, color="red")], spacing=2, alignment=ft.MainAxisAlignment.CENTER), on_click=lambda e: stop_audio(e))

                def toggle_audio(e):
                    nonlocal audio_state
                    if audio_state == 0:
                        pygame.mixer.music.play()
                        audio_state = 1
                        icon_play.src = get_path(feather_map["pause"])
                        label_play.value = "PAUSA"
                        btn_play.bgcolor = "#d9534f"
                    elif audio_state == 1:
                        pygame.mixer.music.pause()
                        audio_state = 2
                        icon_play.src = get_path(feather_map["play"])
                        label_play.value = "RIPRENDI"
                        btn_play.bgcolor = get_c("primary")
                    elif audio_state == 2:
                        pygame.mixer.music.unpause()
                        audio_state = 1
                        icon_play.src = get_path(feather_map["pause"])
                        label_play.value = "PAUSA"
                        btn_play.bgcolor = "#d9534f"
                    btn_play.update()

                def stop_audio(e):
                    nonlocal audio_state
                    pygame.mixer.music.stop()
                    audio_state = 0
                    icon_play.src = get_path(feather_map["play"])
                    label_play.value = "RIPRODUCI"
                    btn_play.bgcolor = get_c("primary")
                    btn_play.update()

                pages_column.controls.extend([ft.Container(height=20), ft.Row([btn_play, btn_stop], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)])
            pages_column.controls.append(ft.Container(height=10))
            pages_column.controls.append(text_element)
            pages_column.controls.append(ft.Container(height=50))
        else:
            images_names = BOOKS_DATA.get(title, [])
            if not images_names:
                pages_column.controls.append(ft.Container(padding=20, content=ft.Text("Nessuna pagina qui.", color=get_c("text_sub"))))
            else:
                for img_name in images_names:
                    full_path = get_path(img_name)
                    if os.path.exists(full_path):
                        pages_column.controls.append(ft.Image(src=full_path, width=350, border_radius=5))
                        pages_column.controls.append(ft.Container(height=10))
        pages_column.update()

    # --- 7. HOME & USER UI ---
    
    # DEFINIZIONE dynamic_content
    cards_column = ft.Column(scroll="auto", spacing=20)
    dynamic_content = ft.Container(content=cards_column, expand=True, padding=ft.padding.symmetric(horizontal=25))

    def create_card(icon_filename, title):
        action = (lambda e: webbrowser.open("https://biografieonline.it/img/bio/gallery/r/Robert_Oppenheimer_1.jpg")) if title == "Foto ricordo" else (lambda e: open_reader(e, title))
        return ft.Container(
            bgcolor=get_c("card"), border_radius=22, padding=15, height=80, on_click=action,
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#0D000000", offset=ft.Offset(0, 5)),
            content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Row(controls=[
                    ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=14, alignment=ft.Alignment(0, 0), content=ft.Image(src=get_path(icon_filename), width=24, height=24, color=get_c("primary"))),
                    ft.Container(width=10),
                    ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=0, controls=[ft.Text(title, size=16, weight="bold", color=get_c("text"))])
                ]),
                ft.Image(src=get_path(feather_map["chevron-right"]), width=24, color="#dddddd")
            ])
        )

    def build_home_cards():
        cards_column.controls.clear()
        cards_column.controls.extend([
            create_card(feather_map["sunrise"], "Lodi Mattutine"),
            create_card(feather_map["book-open"], "Libretto"),
            create_card(feather_map["music"], "Inno"),
            create_card(feather_map["camera"], "Foto ricordo"),
            ft.Container(height=50) 
        ])
    build_home_cards()

    # USER PROFILE LOGIC
    is_custom_pic = (current_profile_src == PROFILE_PIC_FILE)
    img_profile_view = ft.Image(src=current_profile_src, width=150, height=150, border_radius=75, fit="cover", color=None if is_custom_pic else get_c("primary"))
    
    txt_name_input = ft.TextField(value=user_name_value, label="Il tuo nome", max_length=14, border_color=get_c("primary"))
    txt_path_input = ft.TextField(label="Incolla percorso foto JPG", text_size=12, border_color=get_c("primary"))
    
    lbl_font_size = ft.Text(f"Grandezza Testo: {int(current_font_size)}", color=get_c("text"))
    slider_font = ft.Slider(min=12, max=30, divisions=18, value=current_font_size, active_color=get_c("primary"))
    lbl_dark = ft.Text("Modalità Notte", color=get_c("text"))
    switch_theme = ft.Switch(value=is_dark_mode, active_color=get_c("primary"))

    def on_name_change(e):
        txt_welcome_name.value = f"Bentornato, {e.control.value}"
        txt_welcome_name.update()
        save_file(DATA_FILE, e.control.value)
    txt_name_input.on_change = on_name_change

    def on_font_change(e):
        nonlocal current_font_size
        current_font_size = e.control.value
        lbl_font_size.value = f"Grandezza Testo: {int(current_font_size)}"
        lbl_font_size.update()
        notes_input_full.text_size = current_font_size
        notes_input_full.update()
        save_settings_to_disk(current_font_size, is_dark_mode)
    slider_font.on_change = on_font_change

    txt_status_upload = ft.Text("", size=12)
    def upload_photo_manual(e):
        path_org = txt_path_input.value.strip().replace('"', '')
        if os.path.exists(path_org) and os.path.isfile(path_org):
            try:
                shutil.copy(path_org, PROFILE_PIC_FILE)
                nonlocal current_profile_src
                current_profile_src = PROFILE_PIC_FILE
                img_profile_view.src = current_profile_src
                img_profile_view.color = None
                img_profile_view.update()
                nav_user_img.src = current_profile_src
                nav_user_img.color = None
                nav_user_img.border_radius = 50
                nav_user_img.update()
                txt_status_upload.value = "✅ Foto caricata!"
                txt_status_upload.color = "green"
            except:
                txt_status_upload.value = "❌ Errore file."
                txt_status_upload.color = "red"
        else:
            txt_status_upload.value = "⚠️ File non trovato."
            txt_status_upload.color = "red"
        txt_status_upload.update()
    btn_manual_upload = ft.ElevatedButton("CARICA FOTO", bgcolor=get_c("primary"), color="white", on_click=upload_photo_manual)

    btn_open_notes = ft.Container(
        bgcolor=get_c("primary"), border_radius=10, padding=15, width=300,
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Image(src=get_path(feather_map["edit"]), width=20, height=20, color="white"),
            ft.Text("APRI LE TUE NOTE", color="white", weight="bold")
        ]),
        on_click=open_notes_page
    )

    user_view_content = ft.Column(
        scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15,
        controls=[
            ft.Container(height=10),
            ft.Text("Il tuo Profilo", size=20, weight="bold", color=get_c("text")),
            ft.Container(content=img_profile_view, border=ft.border.all(3, get_c("primary")), border_radius=100, padding=5),
            ft.Container(width=280, content=txt_name_input),
            ft.Divider(),
            btn_open_notes, 
            ft.Divider(),
            ft.Text("Cambia Foto (Incolla percorso)", size=12, color="grey"),
            ft.Container(width=300, content=txt_path_input),
            btn_manual_upload,
            txt_status_upload,
            ft.Divider(),
            ft.Text("Impostazioni", size=18, weight="bold", color=get_c("text")),
            ft.Container(padding=10, content=ft.Column(controls=[
                ft.Row([lbl_dark, switch_theme], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                lbl_font_size,
                slider_font
            ])),
            ft.Container(height=120) 
        ]
    )

    # NAVBAR
    nav_home_img = ft.Image(src=get_path(feather_map["home"]), width=20, height=20, color="white")
    nav_user_img = ft.Image(src=current_profile_src, width=20, height=20, fit="cover", border_radius=50 if is_custom_pic else 0, color=None if is_custom_pic else get_c("text"))
    btn_home_container = ft.Container(bgcolor=get_c("primary"), border_radius=10, padding=10, width=140, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[nav_home_img, ft.Text("HOME", color="white", weight="bold")]))
    btn_user_container = ft.Container(bgcolor=get_c("nav_bg"), border_radius=10, padding=10, width=140, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[nav_user_img, ft.Text("PROFILO", color=get_c("text"), weight="bold")]))
    custom_navbar = ft.Container(bgcolor=get_c("nav_bg"), padding=15, border_radius=ft.border_radius.only(top_left=20, top_right=20), shadow=ft.BoxShadow(blur_radius=10, color="#11000000"), content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[btn_home_container, btn_user_container]))

    def go_home(e):
        dynamic_content.content = cards_column
        dynamic_content.update()
        btn_home_container.bgcolor = get_c("primary")
        nav_home_img.color = "white"
        btn_home_container.content.controls[1].color = "white"
        btn_user_container.bgcolor = get_c("nav_bg")
        if not (current_profile_src == PROFILE_PIC_FILE): nav_user_img.color = get_c("text")
        btn_user_container.content.controls[1].color = get_c("text")
        btn_home_container.update()
        btn_user_container.update()

    def go_user(e):
        dynamic_content.content = user_view_content
        dynamic_content.update()
        btn_home_container.bgcolor = get_c("nav_bg")
        nav_home_img.color = get_c("text")
        btn_home_container.content.controls[1].color = get_c("text")
        btn_user_container.bgcolor = get_c("primary")
        if not (current_profile_src == PROFILE_PIC_FILE): nav_user_img.color = "white"
        btn_user_container.content.controls[1].color = "white"
        btn_home_container.update()
        btn_user_container.update()

    btn_home_container.on_click = go_home
    btn_user_container.on_click = go_user

    # --- 8. LOGICA THEME FINALE ---
    def update_interface_colors():
        mobile_screen.bgcolor = get_c("bg")
        header_container.content.controls[0].bgcolor = get_c("primary")
        txt_welcome_name.color = get_c("text")
        reader_container.bgcolor = get_c("bg")
        reader_title.color = get_c("text")
        notes_container.bgcolor = get_c("bg")
        custom_navbar.bgcolor = get_c("nav_bg")
        build_home_cards()
        
        img_profile_view.color = None if (current_profile_src == PROFILE_PIC_FILE) else get_c("primary")
        txt_name_input.border_color = get_c("primary")
        txt_path_input.border_color = get_c("primary")
        lbl_font_size.color = get_c("text")
        slider_font.active_color = get_c("primary")
        lbl_dark.color = get_c("text")
        switch_theme.active_color = get_c("primary")
        if dynamic_content.content == cards_column: go_home(None)
        else: go_user(None)
        
        notes_header.controls[0].content.color = get_c("text")
        icon_save_notes.color = get_c("primary")
        btn_open_notes.bgcolor = get_c("primary")
        btn_open_notes.content.controls[1].color = "white"

        for ctrl in user_view_content.controls:
             if isinstance(ctrl, ft.Text) and ctrl.weight == "bold": ctrl.color = get_c("text")
        page.update()

    def on_theme_change(e):
        nonlocal is_dark_mode
        is_dark_mode = e.control.value
        save_settings_to_disk(current_font_size, is_dark_mode)
        update_interface_colors()
    switch_theme.on_change = on_theme_change

    # --- 9. ASSEMBLAGGIO ---
    mobile_screen = ft.Container(
        width=375, height=812, bgcolor=get_c("bg"), border_radius=35,
        clip_behavior=ft.ClipBehavior.HARD_EDGE, shadow=ft.BoxShadow(blur_radius=50, color="#33000000"),
        content=ft.Stack(controls=[
            ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[header_container, dynamic_content, custom_navbar]),
            reader_container,
            notes_container
        ])
    ) 

    page.add(mobile_screen)
    if is_dark_mode: update_interface_colors()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)