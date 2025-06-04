import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np
import os
import io
import ctypes
from scipy.interpolate import make_interp_spline
from i18n.i18n import t

def get_screen_dpi():
    try:
        dc = ctypes.windll.gdi32.GetDC(0)
        dpi_x = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)
        return dpi_x
    except Exception:
        return 100

class TabDiagrams(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.dpi = get_screen_dpi()
        self.graph_style = ttk.StringVar(value="Line")
        self.plot_image = None
        self.current_plot_data = None
        self.init_ui()

    def init_ui(self):
        font_small = ("Segoe UI", 12)
        self.style = ttk.Style()

        # Общие настройки шрифта
        self.option_add("*TLabel.font", font_small)
        self.option_add("*TButton.font", font_small)
        self.option_add("*TCombobox.font", font_small)
        self.option_add("*TCombobox*Listbox.font", font_small)
        self.option_add("*TCheckbutton.font", font_small)

        # Настройка шрифта для всех стилей кнопок (bootstyle)
        self.style.configure("TButton", font=font_small)
        self.style.configure("Primary.TButton", font=font_small)
        self.style.configure("Secondary.TButton", font=font_small)
        self.style.configure("Info.TButton", font=font_small)
        self.style.configure("Success.TButton", font=font_small)
        self.style.configure("Danger.TButton", font=font_small)
        self.style.configure("Warning.TButton", font=font_small)

        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(side="top", fill="x", padx=20, pady=(20, 5))

        self.label_x_axis = ttk.Label(self.control_frame, text=t("X axis:"))
        self.label_x_axis.pack(side="left", padx=(0, 5))

        self.x_choice_var = ttk.StringVar()
        self.x_choice = ttk.Combobox(
            self.control_frame,
            values=["Time [ms]", "Frame Number"],
            textvariable=self.x_choice_var,
            state="readonly",
            width=13
        )
        self.x_choice.current(0)
        self.x_choice.pack(side="left", padx=(0, 20))

        self.label_y_axis = ttk.Label(self.control_frame, text=t("Y axis:"))
        self.label_y_axis.pack(side="left")

        self.y_choice_var = ttk.StringVar()
        self.y_choice = ttk.Combobox(
            self.control_frame,
            values=self.get_y_options(),
            textvariable=self.y_choice_var,
            state="readonly",
            width=29
        )
        self.y_choice.current(0)
        self.y_choice.pack(side="left", padx=10)

        self.label_graph_style = ttk.Label(self.control_frame, text=t("Graph style:"))
        self.label_graph_style.pack(side="left", padx=(30, 5))

        self.style_choice = ttk.Combobox(
            self.control_frame,
            values=["Line", "Points", "Spline"],
            textvariable=self.graph_style,
            state="readonly",
            width=6
        )
        self.style_choice.pack(side="left", padx=5)

        self.btn_plot = ttk.Button(self.control_frame, text=t("Plot"), width=15, command=self.plot_data)
        self.btn_plot.pack(side="left", padx=10)

        self.btn_clear = ttk.Button(self.control_frame, text=t("Clear"), width=15, command=self.reset)
        self.btn_clear.pack(side="left", padx=10)

        self.btn_export = ttk.Button(self.control_frame, text=t("Export as PNG"), width=15, command=self.export_figure)
        self.btn_export.pack(side="left", padx=10)

        self.canvas = ttk.Frame(self)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas_widget = ttk.Canvas(self.canvas)
        self.canvas_widget.pack(fill="both", expand=True)
        self.canvas_widget.bind("<Configure>", self._on_resize)



    def get_y_options(self):
        return [
            "Center X [pxl]", "Center Y [pxl]",
            "Horizontal Diameter Freefall [mm]", "Vertical Diameter Freefall [mm]",
            "Contact Width [mm]", "Contact Area [mm^2]",
            "Volume [mm^3]", "Left CA [⁰]", "Right CA [⁰]"
        ]

    def plot_data(self):
        headers = self.app.tab_data.sheet.headers()
        data = self.app.tab_data.sheet.get_sheet_data()

        if not headers or not data:
            messagebox.showwarning(t("No data"), t("Please process data first on the 'Data' tab."))
            return

        y_label = self.y_choice.get()
        x_label = self.x_choice.get()  # ⬅️ Получаем выбранную X-ось

        if y_label not in headers:
            messagebox.showerror(t("Invalid selection"), t("Selected Y column not found in data."))
            return

        y_idx = headers.index(y_label)
        x_idx = headers.index(x_label) if x_label in headers else None

        x_vals, y_vals = [], []
        for i, row in enumerate(data):
            try:
                x = (
                    float(row[x_idx]) if x_idx is not None and row[x_idx] is not None
                    else float(i)  # ⬅️ Если "Frame Number", берём индекс
                )
                y = float(row[y_idx]) if row[y_idx] is not None else None
                if x is not None and y is not None:
                    x_vals.append(x)
                    y_vals.append(y)
            except Exception:
                continue

        if not x_vals or not y_vals:
            messagebox.showwarning(t("Empty plot"), t("No valid numeric data available to plot."))
            return

        self.current_plot_data = (x_vals, y_vals, x_label, y_label)  # ⬅️ Сохраняем обе оси
        self._draw_image()

    def _draw_image(self):
        if not self.current_plot_data:
            return

        width = self.canvas_widget.winfo_width()
        height = self.canvas_widget.winfo_height()
        if width <= 1 or height <= 1:
            return

        x_vals, y_vals, x_label, y_label = self.current_plot_data  # ⬅️ Обновлено

        style = self.graph_style.get()
        theme = self.app.style.colors
        bg_color = theme.bg
        line_color = theme.primary if self.app.CURRENT_THEME_NAME != "darkly" else "#6EB5FF"
        fg_color = theme.fg

        fig = plt.Figure(figsize=(width / self.dpi, height / self.dpi), dpi=self.dpi)
        ax = fig.add_subplot(111)

        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=fg_color)
        ax.xaxis.label.set_color(fg_color)
        ax.yaxis.label.set_color(fg_color)
        ax.title.set_color(fg_color)
        for spine in ax.spines.values():
            spine.set_color(fg_color)

        if style == "Points":
            ax.plot(x_vals, y_vals, linestyle='', marker='o', color=line_color)
        elif style == "Spline" and len(x_vals) >= 4:
            x_new = np.linspace(min(x_vals), max(x_vals), 300)
            spline = make_interp_spline(x_vals, y_vals, k=3)
            y_new = spline(x_new)
            ax.plot(x_new, y_new, linestyle='-', color=line_color)
        else:
            ax.plot(x_vals, y_vals, linestyle='-', marker='o', color=line_color)

        ax.set_xlabel(t(x_label))  # ⬅️ Название X-оси по выбору
        ax.set_ylabel(t(y_label))
        ax.grid(True)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        image = Image.open(buf)
        self.plot_image = ImageTk.PhotoImage(image)
        self.canvas_widget.delete("all")
        self.canvas_widget.create_image(0, 0, image=self.plot_image, anchor="nw")
        buf.close()

    def _on_resize(self, event):
        if self.current_plot_data:
            self._draw_image()

    def export_figure(self):
        if not self.plot_image:
            messagebox.showwarning(t("No figure"), t("Please plot the diagram first."))
            return

        initial_dir = self.app.tab_new_project.project_folder or "C:/"
        base_name = "diagram"
        counter = 1
        while True:
            default_name = f"{base_name}_{counter}.png"
            path = os.path.join(initial_dir, default_name)
            if not os.path.exists(path):
                break
            counter += 1

        file_path = filedialog.asksaveasfilename(
            title=t("Save Diagram As"),
            defaultextension=".png",
            filetypes=[(t("PNG Image"), "*.png")],
            initialdir=initial_dir,
            initialfile=default_name
        )
        if file_path:
            try:
                width = self.canvas_widget.winfo_width()
                height = self.canvas_widget.winfo_height()

                theme = self.app.style.colors
                line_color = theme.primary if self.app.CURRENT_THEME_NAME != "darkly" else "#6EB5FF"
                fg_color = theme.fg
                bg_color = theme.bg

                fig = plt.Figure(figsize=(width / self.dpi, height / self.dpi), dpi=self.dpi)
                ax = fig.add_subplot(111)

                fig.patch.set_facecolor(bg_color)
                ax.set_facecolor(bg_color)
                ax.tick_params(colors=fg_color)
                ax.xaxis.label.set_color(fg_color)
                ax.yaxis.label.set_color(fg_color)
                ax.title.set_color(fg_color)
                for spine in ax.spines.values():
                    spine.set_color(fg_color)

                x, y, x_label, y_label = self.current_plot_data  # ⬅️ Обновлено
                style = self.graph_style.get()

                if style == "Points":
                    ax.plot(x, y, linestyle='', marker='o', color=line_color)
                elif style == "Spline" and len(x) >= 4:
                    x_new = np.linspace(min(x), max(x), 300)
                    spline = make_interp_spline(x, y, k=3)
                    y_new = spline(x_new)
                    ax.plot(x_new, y_new, linestyle='-', color=line_color)
                else:
                    ax.plot(x, y, linestyle='-', marker='o', color=line_color)

                ax.set_xlabel(t(x_label))  # ⬅️ Подпись X-оси
                ax.set_ylabel(t(y_label))
                ax.grid(True)
                fig.tight_layout()
                fig.savefig(file_path)
                messagebox.showinfo(t("Success"), f"{t('Diagram saved as:')}\n{file_path}")
            except Exception as e:
                messagebox.showerror(t("Error"), f"{t('Failed to save diagram:')}\n{e}")

    def update_theme(self):
        if self.current_plot_data:
            self._draw_image()

    def update_language(self):
        self.label_x_axis.config(text=t("X axis:"))  # ⬅️ Поддержка смены языка
        self.label_y_axis.config(text=t("Y axis:"))
        self.label_graph_style.config(text=t("Graph style:"))
        self.btn_plot.config(text=t("Plot"))
        self.btn_clear.config(text=t("Clear"))
        self.btn_export.config(text=t("Export as PNG"))

    def reset(self):
        self.canvas_widget.delete("all")
        self.plot_image = None
        self.current_plot_data = None
        self.y_choice.current(0)
        self.x_choice.current(0)  # ⬅️ Сброс X-оси
        self.graph_style.set("Line")
