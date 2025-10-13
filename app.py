import customtkinter as ctk
from PIL import Image
import os
import sys
import platform
import time
import shutil
import re
from datetime import datetime
import tempfile
import webbrowser 

# Importar ctypes para la función de wallpaper en Windows
try:
    import ctypes
    WIN_OS = platform.system() == "Windows"
except ImportError:
    ctypes = None
    WIN_OS = False

# --- CONFIGURACIÓN GLOBAL ---
DEVELOPER_KEY = "Yuuruii-TS-D3v_K3y-2025"
APP_NAME = "Yuuruii Technical Support"
LOGO_FILENAME = "demon.png"
WALLPAPER_FILENAME = "wallpaper.png"
CHANGELOG_DIR_NAME = "YTS"
CHANGELOG_FILENAME = "changelog.md"
# TAMAÑOS AJUSTADOS PARA MEJOR COMPATIBILIDAD CON LAPTOPS (480x500)
MAIN_WINDOW_SIZE = (480, 500)
SPLASH_WINDOW_SIZE = (480, 500) 
SPLASH_DURATION = 3.0 
FEEDBACK_URL = "https://tu-url-personalizada-de-feedback.com" 

# --- ESTRUCTURA DE DATOS (ICONOS OMITIDOS, SÓLO COLORES Y PALABRAS CLAVE) ---
# Los datos de OS se mantienen en el diccionario, pero los iconos ya no se cargan ni se usan.
OS_DATA = {
    "win": {"name": "Windows"},
    "mac": {"name": "macOS"},
    "lin": {"name": "Linux"}
}
# -----------------------------------------------------------

# Colores del tema "Dracula"
DRACULA_COLORS = {
    "background": "#282a36",
    "foreground": "#f8f8f2",
    "selection": "#44475a",
    "red": "#ff5555",       
    "green": "#50fa7b",     
    "cyan": "#8be9fd",      
    "orange": "#ffb86c",    
    "purple": "#DA9CFF",    
    "splash_bg": "#333333", 
    "accent_yellow": "#f1fa8c", 
}

# Palabras clave y sus colores
KEYWORD_COLORS = {
    r"\b(Optimizacion|Actualizacion)\b": DRACULA_COLORS["green"],
    r"\b(Remplazo|Formateo)\b": DRACULA_COLORS["red"],
    r"\b(Reparacion)\b": DRACULA_COLORS["orange"],
    r"\b(OS|S\.O|Sistema Operativo|Operative System|Windows|Linux|MacOS)\b": DRACULA_COLORS["cyan"],
}

# --- FUNCIONES DE UTILIDAD Y CORE ---

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def set_windows_wallpaper(image_path):
    if not WIN_OS or not ctypes:
        return False, "Función solo disponible para Windows o ctypes no cargado."
    
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDCHANGE = 2
    
    try:
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 
            0, 
            image_path, 
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        return result != 0, "Wallpaper establecido correctamente."
    except Exception as e:
        return False, f"Error de la API de Windows: {e}"

def get_documents_folder():
    return os.path.join(os.path.expanduser("~"), "Documents")

def get_changelog_path():
    docs_folder = get_documents_folder()
    yts_folder = os.path.join(docs_folder, CHANGELOG_DIR_NAME)
    
    if not os.path.exists(yts_folder):
        os.makedirs(yts_folder)
        
    return os.path.join(yts_folder, CHANGELOG_FILENAME)

def read_changelog():
    changelog_path = get_changelog_path()
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        default_content = f"Changelog [{datetime.now().strftime('%d-%m-%y')}]\n\n-> Reparacion de errores del sistema operativo Windows y Linux.\n\nBy Yuuruii's Tech Support"
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        content = default_content
        
    return content

def highlight_changelog(text_widget):
    """Resalta las palabras clave (sin iconos)."""
    text = text_widget.get("1.0", "end-1c")
    
    # 1. Limpiar tags anteriores
    for tag in text_widget.tag_names():
        if tag not in ('sel', 'start', 'end'):
            text_widget.tag_delete(tag) 
    
    # 2. Resaltado de texto y palabras clave
    for pattern, color in KEYWORD_COLORS.items():
        tag_name = f"color_{color.replace('#','')}"
        text_widget.tag_config(tag_name, foreground=color)
        
        for match in re.finditer(pattern, text, re.IGNORECASE): 
            start = match.start()
            end = match.end()
            start_pos_text = f"1.0 + {start} chars"
            end_pos_text = f"1.0 + {end} chars"
            
            # Aplicamos el color directamente al texto
            text_widget.tag_add(tag_name, start_pos_text, end_pos_text)
            
    # 3. Resaltado de flechas
    arrow_color = DRACULA_COLORS["purple"]
    arrow_tag_name = f"color_{arrow_color.replace('#','')}"
    text_widget.tag_config(arrow_tag_name, foreground=arrow_color)
    for match in re.finditer(r"->", text):
        start = match.start()
        end = match.end()
        start_pos = f"1.0 + {start} chars"
        end_pos = f"1.0 + {end} chars"
        text_widget.tag_add(arrow_tag_name, start_pos, end_pos)

    # 4. Resaltado de título
    title_match = re.search(r"Changelog\s*\[\s*\d{2}-\d{2}-\d{2}\s*\]", text, re.IGNORECASE)
    if title_match:
        text_widget.tag_config("title_tag", foreground=DRACULA_COLORS["foreground"])
        text_widget.tag_add("title_tag", f"1.0 + {title_match.start()} chars", f"1.0 + {title_match.end()} chars")


# --- CLASE PRINCIPAL: SPLASH SCREEN (El nuevo Root) ---
class SplashScreen(ctk.CTk):
    ICON_TEMP_PATH = None
    
    def __init__(self):
        super().__init__()
        
        self.title("Cargando...")
        
        self.app_logo_image = self.load_single_image(LOGO_FILENAME, size=(40, 40))
        # Reducimos el tamaño del logo en splash para ahorrar espacio vertical
        self.app_logo_image_full = self.load_single_image(LOGO_FILENAME, size=(100, 100)) 
        
        self.set_main_icon() 
        
        root_w = self.winfo_screenwidth()
        root_h = self.winfo_screenheight()
        x = (root_w - SPLASH_WINDOW_SIZE[0]) // 2
        y = (root_h - SPLASH_WINDOW_SIZE[1]) // 2
        
        self.geometry(f"{SPLASH_WINDOW_SIZE[0]}x{SPLASH_WINDOW_SIZE[1]}+{x}+{y}")
        self.resizable(False, False)
        
        self.attributes('-topmost', True) 
        self.overrideredirect(True) 
        self.configure(fg_color=DRACULA_COLORS["splash_bg"])

        # Interfaz de Splash Screen
        main_frame = ctk.CTkFrame(self, fg_color=DRACULA_COLORS["splash_bg"])
        main_frame.pack(expand=True, fill="both")
        main_frame.grid_columnconfigure(0, weight=1)
        # Ajustamos las filas para que haya más espacio arriba y abajo del contenido
        main_frame.grid_rowconfigure((0, 2), weight=1) 
        
        header_frame = ctk.CTkFrame(main_frame, fg_color=DRACULA_COLORS["splash_bg"])
        header_frame.grid(row=1, column=0, pady=0)
        
        if self.app_logo_image_full:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.app_logo_image_full)
            logo_label.pack(side="top", pady=(0, 10))
        
        # Reducimos la fuente aquí también
        text_label = ctk.CTkLabel(header_frame, 
                                  text=f"{APP_NAME}\nCargando...", 
                                  font=("Courier New", 14, "bold"),
                                  text_color="white")
        text_label.pack(side="top")
        
        self.progress_bar = ctk.CTkProgressBar(main_frame, 
                                              orientation="horizontal", 
                                              mode="determinate",
                                              height=4,
                                              width=SPLASH_WINDOW_SIZE[0] - 80,
                                              progress_color="white",
                                              fg_color="#444444")
        self.progress_bar.grid(row=2, column=0, sticky="s", padx=40, pady=40)
        self.progress_bar.set(0)

        self.after(50, self.start_loading)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.ICON_TEMP_PATH and os.path.exists(self.ICON_TEMP_PATH):
            try:
                os.remove(self.ICON_TEMP_PATH)
            except Exception:
                pass 
        self.destroy()

    def set_main_icon(self):
        try:
            icon_path = resource_path(LOGO_FILENAME)
            if WIN_OS:
                self.ICON_TEMP_PATH = os.path.join(tempfile.gettempdir(), "main_icon_yts.ico")
                # Aseguramos que se cargue el archivo si existe para el icono de la barra de tareas
                Image.open(icon_path).save(self.ICON_TEMP_PATH, format='ICO')
                self.iconbitmap(self.ICON_TEMP_PATH)
                self.deiconify() 
            else:
                self.iconphoto(False, ctk.PhotoImage(file=icon_path))
        except Exception as e:
            pass

    def load_single_image(self, filename, size=(40, 40)):
        try:
            path = resource_path(filename)
            pil_image = Image.open(path)
            pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(pil_image, size=size)
        except Exception:
            return None
            
    def start_loading(self):
        start_time = time.time()
        duration = SPLASH_DURATION
        
        def update_progress():
            elapsed = time.time() - start_time
            progress = min(elapsed / duration, 1.0)
            self.progress_bar.set(progress)
            
            if progress < 1.0:
                self.update_idletasks() 
                self.after(50, update_progress)
            else:
                self.update_idletasks()
                self.attributes('-topmost', False) 
                self.launch_main_app() 
                self.withdraw() 

        update_progress()
        
    def launch_main_app(self):
        self.main_app = App(self)
        self.main_app.protocol("WM_DELETE_WINDOW", self.main_app.on_closing_main)
        
        if WIN_OS and self.ICON_TEMP_PATH:
            self.main_app.set_toplevel_icon(self.ICON_TEMP_PATH) 
        
        self.main_app.deiconify() 
        self.main_app.lift()
        self.main_app.attributes('-topmost', True) 
        self.main_app.attributes('-topmost', False) 

    def center_toplevel_window(self, toplevel_window, width, height):
        root_w = self.winfo_screenwidth()
        root_h = self.winfo_screenheight()
        
        x = (root_w - width) // 2
        y = (root_h - height) // 2
        
        toplevel_window.geometry(f'{width}x{height}+{x}+{y}')


# --- CLASE SECUNDARIA: APP (Toplevel) ---
class App(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title(APP_NAME)
        self.transient(master) 
        self.master.center_toplevel_window(self, MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])
        self.resizable(False, False)
        
        self.changelog_content = read_changelog()
        self.start_gui_components()
        
    def on_closing_main(self):
        self.master.on_closing() 

    def set_toplevel_icon(self, icon_path):
        try:
            self.iconbitmap(icon_path)
        except Exception:
            if self.master.app_logo_image:
                 self.iconphoto(False, self.master.app_logo_image._dark_image) 

    def open_feedback_url(self):
        webbrowser.open_new_tab(FEEDBACK_URL)
        
    def start_gui_components(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=DRACULA_COLORS["background"])
        self.main_frame.pack(expand=True, fill="both")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=0)
        self.main_frame.grid_rowconfigure(3, weight=1) # El changelog es la fila que se expande
        self.main_frame.grid_rowconfigure(4, weight=0)

        # Header 
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=DRACULA_COLORS["background"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        if self.master.app_logo_image:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.master.app_logo_image)
            logo_label.grid(row=0, column=0, padx=(0, 10))
        text_label = ctk.CTkLabel(header_frame, text=APP_NAME, font=("Arial", 18, "bold"), text_color=DRACULA_COLORS["foreground"])
        text_label.grid(row=0, column=1, sticky="w")
        
        # Botón de Feedback (Row 2)
        #feedback_button = ctk.CTkButton(self.main_frame,
        #                                text="🌟 Calificar y Dar Feedback",
        #                                command=self.open_feedback_url,
        #                                font=("Arial", 14, "bold"),
        #                                fg_color=DRACULA_COLORS["accent_yellow"],
        #                                text_color=DRACULA_COLORS["background"],
        #                                hover_color=DRACULA_COLORS["orange"],
        #                                corner_radius=8)
        #feedback_button.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 10))


        # Changelog (Row 3, se expande)
        changelog_frame = ctk.CTkFrame(self.main_frame, fg_color=DRACULA_COLORS["selection"], border_color=DRACULA_COLORS["red"], border_width=2)
        changelog_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 10))
        changelog_frame.grid_columnconfigure(0, weight=1)
        changelog_frame.grid_rowconfigure(0, weight=1)
        # Fuente más pequeña para ahorrar espacio vertical
        self.changelog_textbox = ctk.CTkTextbox(changelog_frame, 
                                                font=("Consolas", 11), 
                                                text_color=DRACULA_COLORS["foreground"], 
                                                fg_color=DRACULA_COLORS["selection"], 
                                                wrap="word", 
                                                activate_scrollbars=True, 
                                                padx=10, 
                                                pady=10)
        self.changelog_textbox.grid(row=0, column=0, sticky="nsew")
        self.changelog_textbox.insert("1.0", self.changelog_content)
        self.changelog_textbox.configure(state="disabled")
        highlight_changelog(self.changelog_textbox)

        # YRZ OPTIONS (Row 4) 
        hidden_color = "#353745"
        options_label = ctk.CTkLabel(self.main_frame, text="YRZ OPTIONS", text_color=hidden_color, font=("Arial", 9, "bold"), cursor="hand2")
        options_label.grid(row=4, column=0, pady=(5, 10))
        options_label.bind("<Button-1>", self.open_dev_prompt)


    def open_dev_prompt(self, event):
        if hasattr(self, 'dev_prompt') and self.dev_prompt.winfo_exists():
            self.dev_prompt.lift()
            return
            
        self.dev_prompt = ctk.CTkToplevel(self)
        self.dev_prompt.title("Developer Key")
        self.dev_prompt.resizable(False, False)
        self.dev_prompt.transient(self) 
        
        self.dev_prompt.update_idletasks()
        self.master.center_toplevel_window(self.dev_prompt, 300, 150)
        
        label = ctk.CTkLabel(self.dev_prompt, text="Ingrese Clave de Desarrollo:", font=("Arial", 12))
        label.pack(pady=10)
        
        self.key_entry = ctk.CTkEntry(self.dev_prompt, show="*", width=200)
        self.key_entry.pack(pady=5)
        
        button = ctk.CTkButton(self.dev_prompt, text="Verificar", command=self.check_dev_key)
        button.pack(pady=10)
        
        self.dev_prompt.focus_set()

    def check_dev_key(self):
        entered_key = self.key_entry.get()
        self.dev_prompt.destroy()
        
        if entered_key != DEVELOPER_KEY:
            error_window = ctk.CTkToplevel(self)
            error_window.title("Error")
            error_window.resizable(False, False)
            self.master.center_toplevel_window(error_window, 250, 100)
            ctk.CTkLabel(error_window, text="Clave Incorrecta", text_color="red").pack(pady=30)
            error_window.transient(self)
        else:
            self.open_ts_tools()

    def open_ts_tools(self):
        TS_Tools(self)

# --- VENTANA DE HERRAMIENTAS (DEV MODE) ---
class TS_Tools(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("TS TOOLS")
        self.transient(master)
        
        self.master.master.center_toplevel_window(self, 600, 400) 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header 
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        if self.master.master.app_logo_image:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.master.master.app_logo_image)
            logo_label.grid(row=0, column=0, padx=(0, 10))
        text_label = ctk.CTkLabel(header_frame, text="TS TOOLS", font=("Arial", 18, "bold"), text_color=DRACULA_COLORS["foreground"])
        text_label.grid(row=0, column=1, sticky="w")
        
        edit_frame = ctk.CTkFrame(self)
        edit_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        edit_frame.grid_columnconfigure(0, weight=1)
        edit_frame.grid_rowconfigure(0, weight=1)
        self.edit_textbox = ctk.CTkTextbox(edit_frame, font=("Consolas", 11), text_color="white", fg_color="#333333", wrap="word", padx=10, pady=10)
        self.edit_textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        current_changelog = read_changelog()
        self.edit_textbox.insert("1.0", current_changelog)
        
        # Button frame 
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        button_frame.columnconfigure((0, 1), weight=1)
        
        # Eliminamos los parámetros 'image' y 'compound' ya que los iconos no existen
        save_button = ctk.CTkButton(button_frame, text="Guardar Changelog", command=self.save_changelog)
        save_button.grid(row=0, column=0, padx=10, pady=5)
        
        config_button = ctk.CTkButton(button_frame, text="SET CONFIG (Wallpaper)", command=self.set_wallpaper_config)
        config_button.grid(row=0, column=1, padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=3, column=0, pady=5)

    def save_changelog(self):
        new_content = self.edit_textbox.get("1.0", "end-1c")
        changelog_path = get_changelog_path()
        try:
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            if self.master.changelog_textbox: 
                self.master.changelog_textbox.configure(state="normal")
                self.master.changelog_textbox.delete("1.0", "end")
                self.master.changelog_textbox.insert("1.0", new_content)
                self.master.changelog_textbox.configure(state="disabled")
                highlight_changelog(self.master.changelog_textbox)
            self.show_config_message("Changelog Guardado y Actualizado!", "green")
        except Exception as e:
            self.show_config_message(f"Error al guardar: {e}", "red")

    def set_wallpaper_config(self):
        source_path = resource_path(WALLPAPER_FILENAME)
        new_filename = "yuuruiits_wallpaper.png"
        
        if WIN_OS:
            temp_dir = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), "Yuuruii_TS_Wallpaper")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            destination_path = os.path.join(temp_dir, new_filename)
            
            if source_path.lower().endswith('.png'):
                Image.open(source_path).save(destination_path, format='PNG')
            else:
                shutil.copy2(source_path, destination_path)
            
            success, message = set_windows_wallpaper(destination_path)
            
            if success:
                self.show_config_message(f"Wallpaper establecido automáticamente en Windows!\n{message}", "green")
            else:
                self.show_config_message(f"Wallpaper copiado a '{temp_dir}'.\nError en la configuración automática: {message}", "red")
            
        else: 
            dest_folder = os.path.join(os.path.expanduser("~"), "Pictures")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            destination_path = os.path.join(dest_folder, new_filename)
            shutil.copy2(source_path, destination_path)
            
            message = f"Wallpaper preparado en la carpeta de imágenes:\n{destination_path}\n(Configuración manual requerida en este S.O.)"
            self.show_config_message(message, "orange")

    def show_config_message(self, message, color):
        self.status_label.configure(text=message, text_color=color)
        self.after(5000, lambda: self.status_label.configure(text=""))


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark") 
    ctk.set_default_color_theme("blue") 
    
    app = SplashScreen()
    app.mainloop()