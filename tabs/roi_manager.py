import tkinter as tk

class ROIManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.mode = None
        self.baseline = None  # [x1, y1, x2, y2] в координатах исходного изображения
        self.roi = None       # [x1, y1, x2, y2] в координатах исходного изображения
        self.theme = {
            'baseline_color': 'fuchsia',
            'roi_color': 'orange'
        }

        self._start_x = self._start_y = None
        self._dragging_point = None
        self.handle_radius = 10
        self.hit_radius = 16
        self.scale_ratio = 1.0
        self.editable = True  # Флаг, разрешающий редактирование

    def set_mode(self, mode):
        if self.editable:
            self.mode = mode

    def reset(self):
        self.baseline = None
        self.roi = None
        self._start_x = self._start_y = None
        self._dragging_point = None
        self.redraw()

    def set_theme(self, theme):
        self.theme['roi_color'] = theme.get('highlight', 'orange')

    def load_image(self, path, ratio):
        self.scale_ratio = ratio

    def set_editable(self, value: bool):
        self.editable = value
        self.mode = None
        self._dragging_point = None

    def on_click(self, event):
        if not self.editable:
            return

        self._start_x = event.x
        self._start_y = event.y
        self._dragging_point = None

        x, y = self._unscale(event.x, event.y)

        if self.baseline and self._near(event.x, event.y, *self._scale(self.baseline[:2])):
            self._dragging_point = 'start_baseline'
        elif self.baseline and self._near(event.x, event.y, *self._scale(self.baseline[2:])):
            self._dragging_point = 'end_baseline'
        elif self.roi and self._near(event.x, event.y, *self._scale(self.roi[:2])):
            self._dragging_point = 'tl_roi'
        elif self.roi and self._near(event.x, event.y, *self._scale(self.roi[2:])):
            self._dragging_point = 'br_roi'
        else:
            if self.mode == 'baseline':
                self.baseline = [x, y, x, y]
            elif self.mode == 'roi':
                self.roi = [x, y, x, y]

        self.redraw()

    def on_drag(self, event):
        if not self.editable:
            return

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        x_canvas = min(max(event.x, 0), w)
        y_canvas = min(max(event.y, 0), h)
        x, y = self._unscale(x_canvas, y_canvas)

        if self._dragging_point == 'start_baseline':
            self.baseline[0] = x
            self.baseline[1] = y
        elif self._dragging_point == 'end_baseline':
            self.baseline[2] = x
            self.baseline[3] = y
        elif self._dragging_point == 'tl_roi':
            self.roi[0] = x
            self.roi[1] = y
        elif self._dragging_point == 'br_roi':
            self.roi[2] = x
            self.roi[3] = y
        elif self.mode == 'baseline':
            self.baseline[2] = x
            self.baseline[3] = y
        elif self.mode == 'roi':
            self.roi[2] = x
            self.roi[3] = y

        self.redraw()

    def on_release(self, event):
        if not self.editable:
            return
        self.mode = None
        self._dragging_point = None

    def redraw(self):
        for item in self.canvas.find_all():
            if self.canvas.type(item) != 'image':
                self.canvas.delete(item)

        if self.baseline:
            coords = self._scale(self.baseline)
            self.canvas.create_line(*coords, fill=self.theme['baseline_color'], width=2)
            self._draw_point(*coords[:2])
            self._draw_point(*coords[2:])

        if self.roi:
            coords = self._scale(self.roi)
            self.canvas.create_rectangle(*coords, outline=self.theme['roi_color'], width=2)
            self._draw_point(*coords[:2])
            self._draw_point(*coords[2:])

    def _draw_point(self, x, y):
        r = self.handle_radius
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='lime', outline='black')

    def _near(self, x, y, px, py):
        return (x - px) ** 2 + (y - py) ** 2 <= self.hit_radius ** 2

    def _scale(self, coords):
        return [c * self.scale_ratio for c in coords]

    def _unscale(self, x, y):
        return x / self.scale_ratio, y / self.scale_ratio
