import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import Toplevel
from i18n.i18n import t


class HelpWindow(Toplevel):
    def __init__(self, parent_app):
        super().__init__(parent_app.get_main_window())
        self.parent_app = parent_app
        self.title(t('help.title'))
        self.geometry('800x600')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        try:
            if hasattr(parent_app, 'dropsli_icon'):
                self.iconphoto(True, parent_app.dropsli_icon)
        except Exception:
            pass

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tabs
        self.about_tab = ttk.Frame(self.notebook)
        self.howto_tab = ttk.Frame(self.notebook)
        self.faq_tab = ttk.Frame(self.notebook)
        self.info_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.about_tab, text=t('help.tabs.about'))
        self.notebook.add(self.howto_tab, text=t('help.tabs.how_to_use'))
        self.notebook.add(self.faq_tab, text=t('help.tabs.faq'))
        self.notebook.add(self.info_tab, text=t('help.tabs.info'))

        # Content
        self.about_label = self._create_label(self.about_tab, t('help.about_text'))
        self.howto_label = self._create_label(self.howto_tab, t('help.how_to_use_text'))
        self.faq_label = self._create_label(self.faq_tab, t('help.faq_text'))
        self.info_label = self._create_label(self.info_tab, t('help.info_text'))

        self.apply_theme()

    def _create_label(self, parent, text):
        frame = ScrolledFrame(parent)
        frame.pack(fill='both', expand=True)
        label = ttk.Label(frame, text=text, wraplength=700, justify='left')
        label.pack(padx=15, pady=15, anchor='nw')
        return label

    def apply_theme(self):
        style = self.parent_app.style
        theme = style.colors

        # Используем корректные атрибуты для текста и фона
        fg = theme.fg
        bg = theme.bg

        self.configure(bg=bg)
        for tab in (self.about_tab, self.howto_tab, self.faq_tab, self.info_tab):
            tab.configure(style='TFrame')

        for label in (self.about_label, self.howto_label, self.faq_label, self.info_label):
            label.configure(foreground=fg)

    def update_language(self):
        self.title(t('help.title'))
        self.notebook.tab(0, text=t('help.tabs.about'))
        self.notebook.tab(1, text=t('help.tabs.how_to_use'))
        self.notebook.tab(2, text=t('help.tabs.faq'))
        self.notebook.tab(3, text=t('help.tabs.info'))

        self.about_label.configure(text=t('help.about_text'))
        self.howto_label.configure(text=t('help.how_to_use_text'))
        self.faq_label.configure(text=t('help.faq_text'))
        self.info_label.configure(text=t('help.info_text'))

    def on_close(self):
        self.parent_app.help_window = None
        self.destroy()
