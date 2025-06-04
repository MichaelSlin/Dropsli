import os
import json
import pandas as pd
import sys
import ctypes
from itertools import cycle, chain
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import filedialog, messagebox, PhotoImage

from tabs.tab_new_project import TabNewProject
from tabs.tab_exp_param import TabExpParam
from tabs.tab_data import TabData
from tabs.tab_diagrams import TabDiagrams
from help_window import HelpWindow
from processing import module_excel_gui as xl
from i18n.i18n import t, set_language

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class DropsliApp:

    def __init__(self):
        self.THEMES_DICT = {"menu.theme_light": ("lumen", "journal"),
                            "menu.theme_dark": ("darkly", "superhero")}
        self.THEME_NAMES = tuple(chain.from_iterable(self.THEMES_DICT.values()))
        self.CYCLED_THEME_NAMES = cycle(self.THEME_NAMES)
        self.CURRENT_THEME_NAME = next(self.CYCLED_THEME_NAMES)

        self.main_window = ttk.Window(themename=self.CURRENT_THEME_NAME)
        self.style = self.main_window.style

        self.main_window.title('Dropsli')
        self.main_window.geometry('1000x700')
        self.main_window.state('zoomed')
        self.project_path = None

        default_font = ("Segoe UI", 16)
        self.main_window.option_add("*Font", default_font)
        self.style.configure('TButton', font=("Segoe UI", 14))

        self.dropsli_icon = None
        self.main_window.after(0, self.set_icon)

        self.tab_list = []
        self.help_window = None

        self.set_tabs()
        self.create_menu_bar()
        self.bind_shortcuts()
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_icon(self):
        try:
            # Путь внутри .exe
            if hasattr(sys, "_MEIPASS"):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")

            icon_path = os.path.join(base_path, "assets", "droplet.png")
            self.dropsli_icon = PhotoImage(file=icon_path)
            self.main_window.iconphoto(True, self.dropsli_icon)

        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")

    def get_main_window(self):
        return self.main_window

    def create_menu_bar(self):
        self.menubar = ttk.Menu(self.main_window)
        self.main_window.config(menu=self.menubar)

        self.file_menu = ttk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t('menu.file'), menu=self.file_menu)
        self.file_menu.add_command(label=t('menu.new_project'), command=self.create_new_project, accelerator="Ctrl+N")
        self.file_menu.add_command(label=t('menu.open_project'), command=self.open_project, accelerator="Ctrl+O")
        self.file_menu.add_command(label=t('menu.save_project'), command=self.save_project, accelerator="Ctrl+S")
        self.file_menu.add_separator()

        self.settings_menu = ttk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label=t('menu.settings'), menu=self.settings_menu)
        self.file_menu.add_command(label=t('menu.help'), command=self.show_help, accelerator="Ctrl+H")

        self.colortheme_menu = ttk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=f"{t('menu.color_theme')}{(15 - len(t('menu.color_theme'))) * ' '} Ctrl+T",
                                       menu=self.colortheme_menu)
        for contrast, themes in self.THEMES_DICT.items():
            for theme in themes:
                self.colortheme_menu.add_command(label=f"{t(contrast)} {theme.capitalize()}", command=lambda th=theme: self.change_theme(th))

        self.language_menu = ttk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=f"{t('menu.language')}{(15 - len(t('menu.language'))) * ' '} Ctrl+L",
                                       menu=self.language_menu)
        self.language_menu.add_command(label='English', command=lambda: self.change_language('en'))
        self.language_menu.add_command(label='Русский', command=lambda: self.change_language('ru'))

    def bind_shortcuts(self):
        self.main_window.bind_all('<Control-n>', lambda e: self.create_new_project())
        self.main_window.bind_all('<Control-o>', lambda e: self.open_project())
        self.main_window.bind_all('<Control-s>', lambda e: self.save_project())
        self.main_window.bind_all('<Control-h>', lambda e: self.show_help())
        self.main_window.bind_all('<Control-t>', lambda e: self.switch_theme())
        self.main_window.bind_all('<Control-l>', lambda e: self.toggle_language())

    def change_theme(self, theme_name):
        try:
            self.style.theme_use(theme_name)
            self.CURRENT_THEME_NAME = theme_name

            default_font = ("Segoe UI", 16)
            self.main_window.option_add("*Font", default_font)
            self.style.configure('TButton', font=("Segoe UI", 14))

            for tab in self.tab_list:
                if hasattr(tab, 'update_theme'):
                    tab.update_theme()

            if self.help_window and self.help_window.winfo_exists():
                self.help_window.apply_theme()
        except Exception as e:
            messagebox.showerror(t('error.title'), f"{t('error.theme')}\n{e}")

    def switch_theme(self):
        self.CURRENT_THEME_NAME = next(self.CYCLED_THEME_NAMES)
        self.change_theme(self.CURRENT_THEME_NAME)

    def set_tabs(self):
        self.notebook = ttk.Notebook(self.main_window)
        self.notebook.pack(expand=True, fill='both')

        self.tab_new_project = TabNewProject(self.notebook, self)
        self.tab_exp_param = TabExpParam(self.notebook, self)
        self.tab_data = TabData(self.notebook, self)
        self.tab_diagrams = TabDiagrams(self.notebook, self)

        self.notebook.add(self.tab_new_project, text=t('tab.new_project'))
        self.notebook.add(self.tab_exp_param, text=t('tab.experiment_parameters'))
        self.notebook.add(self.tab_data, text=t('tab.data'))
        self.notebook.add(self.tab_diagrams, text=t('tab.data_visualization'))

        self.tab_list = [self.tab_new_project, self.tab_exp_param, self.tab_data, self.tab_diagrams]

    def is_project_modified(self):
        path = self.tab_new_project.project_json_path
        if not path or not os.path.exists(path):
            return False
        try:
            with open(path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
        except Exception:
            return True

        new_data = self.tab_new_project.get_project_data()
        new_data.update(self.tab_exp_param.get_experiment_parameters())
        table_data = self.tab_data.get_table_data()
        if table_data:
            new_data['results_file'] = 'results.xlsx'

        return old_data != new_data

    def save_project(self):
        path = self.tab_new_project.project_json_path
        if not path:
            messagebox.showwarning(t('warning.title'), t('msg.project_not_created'))
            return

        data = self.tab_new_project.get_project_data()
        data.update(self.tab_exp_param.get_experiment_parameters())

        table_data = self.tab_data.get_table_data()
        if table_data:
            df = pd.DataFrame(table_data)
            results_path = os.path.join(os.path.dirname(path), "results.xlsx")
            df.to_excel(results_path, index=False)
            data['results_file'] = 'results.xlsx'

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        messagebox.showinfo(t('info.title'), f"{t('msg.project_saved')}\n{path}")

    def create_new_project(self):
        if self.tab_new_project.project_json_path and self.is_project_modified():
            answer = messagebox.askyesnocancel(t('dialog.title'), t('msg.save_prompt'))
            if answer is True:
                self.save_project()
            elif answer is None:
                return

        self.project_path = None
        self.tab_new_project.reset()
        self.tab_exp_param.reset()
        self.tab_data.reset()
        self.tab_diagrams.reset()
        self.notebook.select(0)
        messagebox.showinfo(t('info.title'), t('msg.new_project_ready'))

    def open_project(self):
        if self.tab_new_project.project_json_path and self.is_project_modified():
            answer = messagebox.askyesnocancel(t('dialog.title'), t('msg.save_prompt'))
            if answer is True:
                self.save_project()
            elif answer is None:
                return

        json_path = filedialog.askopenfilename(
            title=t('dialog.open_project'),
            filetypes=[("JSON files", "*.json")]
        )
        if not json_path:
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.tab_new_project.load_project_data(config)
        self.tab_new_project.project_json_path = json_path
        self.tab_exp_param.load_experiment_parameters(config)

        results_file = config.get('results_file')
        if results_file:
            excel_path = os.path.join(os.path.dirname(json_path), results_file)
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                self.tab_data.load_table_data(df)

        messagebox.showinfo(t('info.title'), f"{t('msg.project_loaded')}\n{json_path}")

    def export_to_xl(self):
        data = self.tab_data.sheet.get_sheet_data()
        headers = self.tab_data.sheet.headers()

        if not data or not headers:
            messagebox.showwarning(t('warning.title'), t('msg.no_data_export'))
            return

        project_path = self.tab_new_project.project_folder or os.getcwd()
        project_name = os.path.basename(project_path).lower()

        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialdir=project_path,
            initialfile=f"{project_name}.xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title=t('dialog.save_excel')
        )
        if not path:
            return

        try:
            sheet, workbook = xl.create_excel_worksheet()
            xl.create_headers(sheet)

            for row in data:
                xl.append_table_data(sheet, row)

            xl.apply_alignment(sheet)
            xl.set_up_format(sheet)
            xl.save_excel_file(workbook, path)

            messagebox.showinfo(t('info.title'), f"{t('msg.excel_saved')}\n{path}")

        except Exception as e:
            messagebox.showerror(t('error.title'), f"{t('msg.excel_error')}\n{e}")

    def change_language(self, lang_code):
        self._lang = lang_code  # запоминаем текущий язык в памяти
        set_language(lang_code)

        # Обновить меню
        self.create_menu_bar()

        # Обновить названия вкладок
        keys = [
            'tab.new_project',
            'tab.experiment_parameters',
            'tab.data',
            'tab.data_visualization'
        ]
        for idx, key in enumerate(keys):
            self.notebook.tab(idx, text=t(key))

        # Обновить содержимое вкладок
        for tab in self.tab_list:
            if hasattr(tab, 'update_language'):
                tab.update_language()

        # Обновить справку
        if self.help_window and self.help_window.winfo_exists():
            self.help_window.update_language()
            self.help_window.apply_theme()



    def toggle_language(self):
        current = self.get_current_language()
        new_lang = 'ru' if current == 'en' else 'en'
        self.change_language(new_lang)

    def get_current_language(self):
        return getattr(self, "_lang", "en")  # всегда начинаем с английского

    def show_help(self):
        if self.help_window and self.help_window.winfo_exists():
            self.help_window.lift()
        else:
            self.help_window = HelpWindow(self)

    def on_close(self):
        if self.tab_new_project.project_json_path and self.is_project_modified():
            answer = messagebox.askyesnocancel(t('dialog.title'), t('msg.save_prompt'))
            if answer is True:
                self.save_project()
            elif answer is None:
                return
        self.main_window.destroy()
