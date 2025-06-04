import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from tabs.roi_manager import ROIManager
from i18n.i18n import t

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 960

class TabExpParam(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.input_folder = None
        self.canvas_img = None
        self.current_image_path = None

        self.scale_var = ttk.StringVar()
        self.fps_var = ttk.StringVar()
        self.scale_confirmed = False
        self.image_confirmed = False

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()

        self.roi_manager = ROIManager(self.canvas)
        self.canvas.bind("<Button-1>", self.roi_manager.on_click)
        self.canvas.bind("<B1-Motion>", self.roi_manager.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.roi_manager.on_release)

        self.btn_define_baseline.config(state='disabled')
        self.btn_define_roi.config(state='disabled')
        self.btn_confirm_next.config(state='disabled')

    def create_widgets(self):
        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=0, column=0, columnspan=2, sticky='n', padx=10, pady=10)

        self.label_title = ttk.Label(self.control_frame, text=t("Experiment Parameters"), font=("Segoe UI", 18))
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))

        self.label_scale = ttk.Label(self.control_frame, text=t("Scale (pixels per mm):"))
        self.label_scale.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_scale = ttk.Entry(self.control_frame, textvariable=self.scale_var, width=20)
        self.entry_scale.grid(row=1, column=1, sticky='e', padx=5, pady=5)

        self.label_fps = ttk.Label(self.control_frame, text=t("Frames per second (fps):"))
        self.label_fps.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_fps = ttk.Entry(self.control_frame, textvariable=self.fps_var, width=20)
        self.entry_fps.grid(row=2, column=1, sticky='e', padx=5, pady=5)

        self.btn_confirm_scale = ttk.Button(self.control_frame, text=t("Confirm"), width=20, command=self.confirm_scale)
        self.btn_confirm_scale.grid(row=3, column=0, padx=5, pady=5)

        self.btn_edit_scale = ttk.Button(self.control_frame, text=t("Edit"), width=20, command=self.edit_scale, state='disabled')
        self.btn_edit_scale.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.control_frame, text="").grid(row=4, column=0, columnspan=2, pady=5)

        self.label_tools = ttk.Label(self.control_frame, text=t("Image Tools"), font=("Segoe UI", 18))
        self.label_tools.grid(row=5, column=0, columnspan=2, sticky='w', pady=(0, 5))

        self.btn_define_baseline = ttk.Button(self.control_frame, text=t("Define baseline"), width=30, command=self.activate_baseline)
        self.btn_define_baseline.grid(row=6, column=0, columnspan=2, pady=(10, 5))

        self.btn_define_roi = ttk.Button(self.control_frame, text=t("Define ROI"), width=30, command=self.activate_roi)
        self.btn_define_roi.grid(row=7, column=0, columnspan=2, pady=5)

        self.btn_select_image = ttk.Button(self.control_frame, text=t("Select Image"), width=30, command=self.select_image)
        self.btn_select_image.grid(row=8, column=0, columnspan=2, pady=5)

        self.btn_confirm_image = ttk.Button(self.control_frame, text=t("Confirm"), width=20, command=self.confirm_image)
        self.btn_confirm_image.grid(row=9, column=0, padx=5, pady=5)

        self.btn_edit_image = ttk.Button(self.control_frame, text=t("Edit"), width=20, command=self.edit_image, state='disabled')
        self.btn_edit_image.grid(row=9, column=1, padx=5, pady=5)

        self.canvas = ttk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=2, padx=10, pady=10, sticky='n')

        self.btn_confirm_next = ttk.Button(self, text=t("Confirm and Next"), width=20, command=self.confirm_and_next, state='disabled')
        self.btn_confirm_next.grid(row=1, column=2, sticky='se', padx=10, pady=10)

    def update_language(self):
        self.label_title.config(text=t("Experiment Parameters"))
        self.label_scale.config(text=t("Scale (pixels per mm):"))
        self.label_fps.config(text=t("Frames per second (fps):"))
        self.btn_confirm_scale.config(text=t("Confirm"))
        self.btn_edit_scale.config(text=t("Edit"))
        self.label_tools.config(text=t("Image Tools"))
        self.btn_define_baseline.config(text=t("Define baseline"))
        self.btn_define_roi.config(text=t("Define ROI"))
        self.btn_select_image.config(text=t("Select Image"))
        self.btn_confirm_image.config(text=t("Confirm"))
        self.btn_edit_image.config(text=t("Edit"))
        self.btn_confirm_next.config(text=t("Confirm and Next"))

    def confirm_and_next(self):
        self.app.notebook.select(2)
        messagebox.showinfo(t("Dropsli Message"), t("Good! Now everything is ready for data collection!"))
        # self.btn_confirm_next.config(state='disabled')
        # self.btn_edit_scale.config(state='disabled')
        # self.btn_edit_image.config(state='disabled')

    def confirm_scale(self):
        if not self.is_positive_float(self.scale_var.get()) or not self.is_positive_float(self.fps_var.get()):
            messagebox.showerror(t("Error"), t("Please enter positive numeric values for Scale and FPS."))
            return
        self.entry_scale.config(state='readonly')
        self.entry_fps.config(state='readonly')
        self.btn_confirm_scale.config(state='disabled')
        self.btn_edit_scale.config(state='normal')
        self.scale_confirmed = True
        self.update_next_state()

    def confirm_image(self):
        if not self.current_image_path:
            messagebox.showerror(t("Error"), t("No image selected."))
            return
        if not self.roi_manager.baseline or not self.roi_manager.roi:
            messagebox.showerror(t("Error"), t("Both baseline and ROI must be drawn before confirming."))
            return
        self.btn_define_baseline.config(state='disabled')
        self.btn_define_roi.config(state='disabled')
        self.btn_select_image.config(state='disabled')
        self.btn_confirm_image.config(state='disabled')
        self.btn_edit_image.config(state='normal')
        self.roi_manager.set_editable(False)
        self.image_confirmed = True
        self.update_next_state()

    def edit_scale(self):
        self.entry_scale.config(state='normal')
        self.entry_fps.config(state='normal')
        self.btn_confirm_scale.config(state='normal')
        self.btn_edit_scale.config(state='disabled')
        self.scale_confirmed = False
        self.btn_confirm_next.config(state='disabled')

    def edit_image(self):
        self.btn_define_baseline.config(state='normal')
        self.btn_define_roi.config(state='normal')
        self.btn_select_image.config(state='normal')
        self.btn_confirm_image.config(state='normal')
        self.btn_edit_image.config(state='disabled')
        self.roi_manager.set_editable(True)
        self.image_confirmed = False
        self.btn_confirm_next.config(state='disabled')

    def update_next_state(self):
        if self.scale_confirmed and self.image_confirmed:
            self.btn_confirm_next.config(state='normal')

    def activate_baseline(self):
        self.roi_manager.set_mode('baseline')

    def activate_roi(self):
        self.roi_manager.set_mode('roi')

    def resize_image_by_height(self, image, target_height):
        width, height = image.size
        ratio = target_height / height
        return image.resize((int(width * ratio), target_height), Image.LANCZOS), ratio

    def set_image(self, path):
        try:
            img = Image.open(path)
        except Exception as e:
            messagebox.showerror(t("Error"), t("Failed to load image: {e}").format(e=e))
            return

        old_baseline = self.roi_manager.baseline
        old_roi = self.roi_manager.roi
        old_ratio = self.roi_manager.scale_ratio

        img, new_ratio = self.resize_image_by_height(img, CANVAS_HEIGHT)
        self.canvas.config(width=img.width)
        self.canvas_img = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.canvas_img)
        self._canvas_img_ref = self.canvas_img

        self.roi_manager.load_image(path, new_ratio)

        if old_baseline:
            self.roi_manager.baseline = [x * old_ratio / new_ratio for x in old_baseline]
        if old_roi:
            self.roi_manager.roi = [x * old_ratio / new_ratio for x in old_roi]

        self.roi_manager.redraw()
        self.btn_define_baseline.config(state='normal')
        self.btn_define_roi.config(state='normal')

    def select_image(self):
        if not self.input_folder:
            messagebox.showwarning(t("Warning"), t("Input folder not set."))
            return
        path = filedialog.askopenfilename(
            initialdir=self.input_folder,
            title=t("Select image"),
            filetypes=[("Image Files", "*.bmp *.jpg *.jpeg *.png *.tif *.tiff *.webp *.gif")]
        )
        if path:
            self.current_image_path = path
            self.set_image(path)

    def reset(self):
        self.edit_scale()
        self.edit_image()
        self.entry_fps.delete(0, ttk.END)
        self.entry_scale.delete(0, ttk.END)
        self.btn_define_baseline.config(state='disabled')
        self.btn_define_roi.config(state='disabled')
        self.input_folder = None
        self.roi_manager.reset()
        self.canvas.delete("all")
        self.canvas_img = None
        self.current_image_path = None

    def is_positive_float(self, value):
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    def get_baseline(self):
        b = self.roi_manager.baseline
        if b and len(b) == 4:
            return (b[0], b[1]), (b[2], b[3])
        return None

    def get_roi(self):
        r = self.roi_manager.roi
        if r and len(r) == 4:
            x1, y1, x2, y2 = r
            return int(min(x1, x2)), int(min(y1, y2)), int(abs(x2 - x1)), int(abs(y2 - y1))
        return None

    def get_experiment_parameters(self):
        return {
            'fps': float(self.fps_var.get()) if self.is_positive_float(self.fps_var.get()) else None,
            'scale': float(self.scale_var.get()) if self.is_positive_float(self.scale_var.get()) else None,
            'baseline': self.roi_manager.baseline,
            'roi': self.roi_manager.roi,
            'scale_ratio': self.roi_manager.scale_ratio
        }

    def load_experiment_parameters(self, data):
        self.input_folder = data.get('input_folder') or self.app.tab_new_project.input_folder
        scale = data.get('scale')
        fps = data.get('fps')
        baseline = data.get('baseline')
        roi = data.get('roi')
        saved_ratio = data.get('scale_ratio', 1.0)

        if scale is not None:
            self.scale_var.set(str(scale))
        if fps is not None:
            self.fps_var.set(str(fps))

        self.confirm_scale()

        if self.input_folder:
            image_files = [f for f in os.listdir(self.input_folder)
                           if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp', '.gif'))]
            if image_files:
                image_path = os.path.join(self.input_folder, image_files[0])
                self.current_image_path = image_path
                self.set_image(image_path)

        current_ratio = self.roi_manager.scale_ratio

        if baseline:
            self.roi_manager.baseline = [x * current_ratio / saved_ratio for x in baseline]
        if roi:
            self.roi_manager.roi = [x * current_ratio / saved_ratio for x in roi]

        self.roi_manager.set_editable(False)
        self.roi_manager.redraw()

        self.image_confirmed = True
        self.update_next_state()
        self.btn_define_baseline.config(state='disabled')
        self.btn_define_roi.config(state='disabled')
        self.btn_confirm_image.config(state='disabled')
        self.btn_select_image.config(state='disabled')
        self.btn_edit_image.config(state='normal')

    def is_ready(self):
        try:
            fps = float(self.fps_var.get())
            scale = float(self.scale_var.get())
            return fps > 0 and scale > 0 and self.get_baseline() is not None
        except Exception:
            return False
