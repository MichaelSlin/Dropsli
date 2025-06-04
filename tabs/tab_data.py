import os
import math
import threading
import tempfile
import shutil
import pandas as pd
from tksheet import Sheet
from processing.module_process_frame import Frame
from tkinter import messagebox
from ttkbootstrap import Frame as TTKFrame, Button as TTKButton, Label as TTKLabel
from ttkbootstrap.widgets import Progressbar as TTKProgressbar
from PIL import Image, ImageTk
import tkinter.font as tkFont
import tkinter as tk
import cv2
from i18n.i18n import t


class TabData(TTKFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.style = self.app.style
        self.current_image = None
        self._lock = threading.Lock()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.init_ui()

    def init_ui(self):
        self.process_btn = TTKButton(self, text=t("Process"), width=20, command=self.start_processing, bootstyle="primary")
        self.process_btn.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.progress_bar = TTKProgressbar(self, orient="horizontal", mode="determinate", length=400, bootstyle="success")
        self.progress_bar.grid(row=0, column=1, padx=10, pady=15, sticky="w")

        self.status_label = TTKLabel(self, text=t("Ready"), font=("Segoe UI", 11))
        self.status_label.grid(row=0, column=2, padx=10, pady=15, sticky="e")

        self.btn_export_excel = TTKButton(self, text=t("Export Data to Excel"), width=22, command=self.app.export_to_xl)
        self.btn_export_excel.grid(row=0, column=3, padx=10, pady=15, sticky="e")
        self.btn_export_excel.config(state="disabled")

        self.btn_save_frames = TTKButton(self, text=t("Save Processed Frames"), width=22, command=self.save_processed_frames)
        self.btn_save_frames.grid(row=0, column=4, padx=10, pady=15, sticky="e")
        self.btn_save_frames.config(state="disabled")

        self.sheet = Sheet(self, height=500)
        self.sheet.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 20), sticky="nsew")
        self.sheet.enable_bindings(("single_select", "row_select", "arrowkeys", "drag_select"))
        self.sheet.extra_bindings("row_select", self.on_row_select)
        self.sheet.extra_bindings("cell_select", self.on_cell_select)
        self.sheet.set_options(freeze_columns=1)

        self.image_canvas = tk.Canvas(self, bg="black", width=500, height=500)
        self.image_canvas.grid(row=1, column=3, columnspan=2, padx=10, pady=(0, 20), sticky="nsew")

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        self.update_sheet_theme()

    def update_sheet_theme(self):
        colors = self.style.colors
        self.sheet.set_options(
            header_bg=colors.secondary,
            header_fg=colors.fg,
            header_font=('Segoe UI', 11, 'bold'),
            index_bg=colors.secondary,
            index_fg=colors.fg,
            index_font=('Segoe UI', 11, 'bold'),
            table_bg=colors.bg,
            table_fg=colors.fg,
            table_font=('Segoe UI', 10, 'normal'),
            header_grid_fg=colors.border,
            index_grid_fg=colors.border,
            align="center",
            align_vertical="center",
            highlight_bg=colors.primary,
            highlight_fg=colors.fg,
            selected_rows_bg=colors.secondary,
            selected_rows_fg=colors.fg,
            box_bg=colors.bg,  # фон за пределами таблицы
            outline_color=colors.border  # границы таблицы
        )
        self.sheet.refresh()


    def start_processing(self):
        if not self.app.tab_exp_param.is_ready():
            messagebox.showwarning(t("Warning"), t("Please finish setting experiment parameters before processing."))
            return
        self.process_btn.config(state="disabled")
        self.app.tab_diagrams.reset()
        threading.Thread(target=self._safe_process_wrapper, daemon=True).start()

    def _safe_process_wrapper(self):
        try:
            self.process_all_frames()
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.status_label.config(text=t("Error"))
            self.process_btn.config(state="normal")
            messagebox.showerror(t("Error"), f"{t('An error occurred during processing:')}\n{e}")

    def process_all_frames(self):
        input_folder = self.app.tab_new_project.input_folder
        tmp_dir = self.temp_dir.name
        line_coords = self.app.tab_exp_param.get_baseline()
        roi_rect = self.app.tab_exp_param.get_roi()

        if not input_folder or not line_coords:
            messagebox.showerror(t("Error"), t("Input folder or baseline not set."))
            self.process_btn.config(state="normal")
            return

        try:
            scale = 1 / float(self.app.tab_exp_param.scale_var.get())
            fps = float(self.app.tab_exp_param.fps_var.get())
        except Exception:
            messagebox.showerror(t("Error"), t("Could not read FPS and scale."))
            self.process_btn.config(state="normal")
            return

        filenames = sorted(os.listdir(input_folder))
        total = len(filenames)
        results = []
        period = 1 / fps

        for i, filename in enumerate(filenames):
            frame = Frame(
                input_folder, tmp_dir, filename,
                line_coords, draw=True, save_to_disk=True,
                roi_rect=roi_rect
            )
            frame.process(method="otsu")
            time_ms = i * period * 1000

            def r(x, d): return round(x, d) if isinstance(x, (int, float)) else None

            hor_mm = r(frame.hor_diameter_freefall * scale, 4) if frame.hor_diameter_freefall else None
            vert_mm = r(frame.vert_diameter_freefall * scale, 4) if frame.vert_diameter_freefall else None
            contact_mm = r(frame.contact_width * scale, 5) if frame.contact_width else None
            contact_area = r((math.pi * contact_mm ** 2) / 4, 5) if contact_mm else None
            volume = r(frame.volume_drop, 5) if frame.volume_drop else None
            left_angle = r(frame.left_angle, 2) if frame.left_angle is not None else None
            right_angle = r(frame.right_angle, 2) if frame.right_angle is not None else None

            row = [
                filename,
                r(time_ms, 4),
                frame.center_x,
                frame.center_y,
                hor_mm,
                vert_mm,
                contact_mm,
                contact_area,
                volume,
                left_angle,
                right_angle
            ]
            results.append(row)

            self.progress_bar["value"] = int((i + 1) / total * 100)
            self.status_label.config(text=f"{i + 1}/{total} {t('Processed')}")
            self.update_idletasks()

        headers = [
            "Frame name", "Time [ms]",
            "Center X [pxl]", "Center Y [pxl]",
            "Horizontal Diameter Freefall [mm]",
            "Vertical Diameter Freefall [mm]",
            "Contact Width [mm]", "Contact Area [mm^2]",
            "Volume [mm^3]",
            "Left CA [⁰]", "Right CA [⁰]"
        ]
        self.sheet.headers(headers)
        self.sheet.set_sheet_data(results)
        self.autosize_columns(headers)
        self.update_sheet_theme()
        self.status_label.config(text=t("Processing complete"))
        messagebox.showinfo(t("Dropsli Message"), t("Processing completed. All {n} frames were processed.").format(n=len(results)))
        self.process_btn.config(state="normal")
        self.btn_export_excel.config(state="normal")
        self.btn_save_frames.config(state="normal")

        # Выбрать первую строку и отобразить первый кадр
        if results:
            self.sheet.set_currently_selected((0, 0))
            self.display_image_by_row(0)
        

    def save_processed_frames(self):
        tmp_dir = self.temp_dir.name
        if not os.path.exists(tmp_dir):
            messagebox.showwarning(
                t("Warning"),
                t("No processed frames found. Please process data first.")
            )
            return

        files = os.listdir(tmp_dir)
        num_files = len(files)

        if num_files == 0:
            messagebox.showinfo(
                t("No files"),
                t("There are no processed frames to save.")
            )
            return

        confirm = messagebox.askyesno(
            t("Confirm Save"),
            t("Are you sure you want to save {count} processed frames to the project folder?").format(count=num_files)
        )
        if not confirm:
            return

        # ⬇️ Центрируем окно прогресса
        def center_window(win, width=300, height=100):
            win.update_idletasks()
            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            win.geometry(f"{width}x{height}+{x}+{y}")

        # Получаем текущую тему
        colors = self.style.colors

        progress_win = tk.Toplevel(self)
        progress_win.title(t("Saving"))
        center_window(progress_win)
        progress_win.configure(bg=colors.bg)
        progress_win.grab_set()
        progress_win.resizable(False, False)

        label = TTKLabel(progress_win, text=t("Saving frames..."), background=colors.bg, foreground=colors.fg)
        label.pack(pady=10)

        progress_bar = TTKProgressbar(progress_win, length=250, mode="determinate", maximum=num_files, bootstyle="info")
        progress_bar.pack(pady=5)

        self.update_idletasks()

        dst_dir = os.path.join(self.app.tab_new_project.project_folder, "Processed_frames")

        def copy_files():
            os.makedirs(dst_dir, exist_ok=True)
            for i, f in enumerate(files, 1):
                shutil.copy(os.path.join(tmp_dir, f), os.path.join(dst_dir, f))
                progress_bar["value"] = i
                progress_win.update_idletasks()
            progress_win.destroy()
            messagebox.showinfo(
                t("Success"),
                t("All processed frames saved to:\n{dst}").format(dst=dst_dir)
            )

        threading.Thread(target=copy_files, daemon=True).start()


    def on_row_select(self, event):
        selected = self.sheet.get_currently_selected()
        if selected:
            row = selected[0]
            self.display_image_by_row(row)

    def on_cell_select(self, event):
        selected = self.sheet.get_currently_selected()
        if selected:
            row = selected[0]
            self.display_image_by_row(row)


    def display_image_by_row(self, row):
        if self._lock.locked():
            return

        with self._lock:
            try:
                filename = self.sheet.get_cell_data(row, 0)

                frame = Frame(
                    self.app.tab_new_project.input_folder,
                    self.temp_dir.name,
                    filename,
                    self.app.tab_exp_param.get_baseline(),
                    draw=True,
                    save_to_disk=False,
                    roi_rect=self.app.tab_exp_param.get_roi()
                )
                frame.process(method="otsu")
                img = frame.outlined_img

                if img is None:
                    return

                h_canvas = self.image_canvas.winfo_height()
                w_canvas = self.image_canvas.winfo_width()
                h_img, w_img = img.shape[:2]
                scale = min(w_canvas / w_img, h_canvas / h_img)
                new_size = (int(w_img * scale), int(h_img * scale))

                img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
                img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(img_rgb)
                self.current_image = ImageTk.PhotoImage(image_pil)

                self.image_canvas.delete("all")
                self.image_canvas.create_image(w_canvas // 2, h_canvas // 2, image=self.current_image, anchor="center")

            except Exception as e:
                print(f"Image loading failed: {e}")



    def autosize_columns(self, headers):
        font = tkFont.Font(family="Segoe UI", size=10)
        for i, h in enumerate(headers):
            column_width = font.measure(h) * 2
            self.sheet.column_width(i, min(500, max(120, column_width)))

    def get_table_data(self):
        headers = self.sheet.headers()
        data = self.sheet.get_sheet_data()
        return [dict(zip(headers, row)) for row in data if any(cell not in ('', None) for cell in row)]

    def load_table_data(self, df):
        self.btn_save_frames.config(state="normal")
        self.btn_export_excel.config(state="normal")
        headers = list(df.columns)
        data = df.fillna('').values.tolist()
        self.sheet.headers(headers)
        self.sheet.set_sheet_data(data)
        self.autosize_columns(headers)
        self.update_sheet_theme()
        # Выбрать первую строку и отобразить первый кадр
        if data:
            self.sheet.set_currently_selected((0, 0))
            self.display_image_by_row(0)

    def update_theme(self):
        self.update_sheet_theme()

    def update_language(self):
        self.process_btn.config(text=t("Process"))
        self.status_label.config(text=t("Ready"))
        self.btn_export_excel.config(text=t("Export Data to Excel"))
        self.btn_save_frames.config(text=t("Save Processed Frames"))

    def reset(self):
        self.sheet.set_sheet_data([])
        self.sheet.headers([])
        self.progress_bar["value"] = 0
        self.status_label.config(text=t("Ready"))
        self.process_btn.config(state="normal")
        self.btn_export_excel.config(state="disabled")
        self.btn_save_frames.config(state="disabled")
        self.image_canvas.delete("all")
        self.current_image = None
        self.temp_dir.cleanup()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.update_idletasks()
