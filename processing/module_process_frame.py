import cv2
import numpy as np
import math
import os
from processing import module_parameters as param

class Frame:

    def __init__(self, input_folder, output_folder, filename, line_coordinates, draw=True, save_to_disk=False, roi_rect=None):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.filename = filename
        self.line_coordinates = line_coordinates
        self.draw = draw
        self.save_to_disk = save_to_disk
        self.roi_rect = roi_rect  # ROI: (x, y, w, h)
        self.file_path = os.path.join(input_folder, filename)

        # === Инициализация всех атрибутов ДО возможного return ===
        self.img = None
        self.gray = None
        self.binary = None
        self.mask = None
        self.outlined_img = None

        self.valid = False
        self.center_x = None
        self.center_y = None
        self.hor_diameter_freefall = None
        self.vert_diameter_freefall = None
        self.contact_width = None
        self.volume_drop = None
        self.leftmost = None
        self.rightmost = None
        self.left_angle = None
        self.right_angle = None

        # === Попытка загрузки изображения ===
        self.img = cv2.imread(self.file_path)
        if self.img is None:
            print(f"Warning: Could not read image file '{self.filename}'. Skipping...")
            return

        self.valid = True
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.outlined_img = self.img.copy()


    def apply_threshold(self, method, **kwargs):
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        if method == 'global':
            thresh_val = kwargs.get('threshold', 127)
            _, binary = cv2.threshold(self.gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
        elif method == 'mean':
            blocksize = kwargs.get('blocksize', 11)
            C = kwargs.get('C', 2)
            binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY_INV, blocksize, C)
        elif method == 'gaussian':
            blocksize = kwargs.get('blocksize', 11)
            C = kwargs.get('C', 2)
            binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, blocksize, C)
        elif method == 'otsu':
            _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            raise ValueError(f"Unknown thresholding method: {method}")
        return binary

    def process(self, method='otsu', **kwargs):
        if not self.valid or self.line_coordinates is None:
            print(f"Error: Skipping {self.filename} due to invalid data.")
            return

        (x1, y1), (x2, y2) = self.line_coordinates
        line_angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        # Построение наклонной линии
        height, width = self.img.shape[:2]
        if x2 == x1:
            x = x1
            pt1 = (x, 0)
            pt2 = (x, height - 1)
        else:
            k = (y2 - y1) / (x2 - x1)
            b = y1 - k * x1
            y_left = int(b)
            y_right = int(k * (width - 1) + b)
            pt1 = (0, y_left)
            pt2 = (width - 1, y_right)

        cv2.line(self.outlined_img, pt1, pt2, (255, 0, 255), 1)

        # Маска выше линии
        mask_line = np.zeros_like(self.gray, dtype=np.uint8)
        for x in range(width):
            y_line = int(k * x + b) if x2 != x1 else height
            if 0 <= y_line < height:
                mask_line[:y_line, x] = 255
            elif y_line >= height:
                mask_line[:, x] = 255

        # Прямоугольная ROI маска
        mask_roi = np.zeros_like(self.gray, dtype=np.uint8)
        if self.roi_rect is not None:
            x, y, w, h = self.roi_rect
            mask_roi[y:y+h, x:x+w] = 255
        else:
            mask_roi[:, :] = 255  # если ROI не задана, использовать всю область

        # Пересечение маски линии и ROI
        self.mask = cv2.bitwise_and(mask_line, mask_roi)

        # Бинаризация и применение маски
        thresh = self.apply_threshold(method, **kwargs)
        self.binary = cv2.bitwise_and(thresh, self.mask)

        contours, _ = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            return

        # Остальная обработка без изменений
        largest_contour = max(contours, key=cv2.contourArea)
        self.center_x, self.center_y = param.compute_center_of_mass(largest_contour)
        self.leftmost, self.rightmost, touch = param.find_leftmost_and_rightmost_points(largest_contour, self.line_coordinates)
        self.contact_width = param.calculate_contact_width(self.leftmost, self.rightmost, touch)
        self.hor_diameter_freefall, left_ff, right_ff = param.compute_horizontal_diameter_while_freefall(largest_contour, self.center_y, touch)
        self.vert_diameter_freefall, up_ff, down_ff = param.compute_vertical_diameter_while_freefall(largest_contour, self.center_x, touch)
        self.volume_drop = param.compute_drop_volume(largest_contour)

        should_draw = self.draw or self.save_to_disk

        if should_draw:
            cv2.drawContours(self.outlined_img, [largest_contour], -1, (0, 255, 0), 1)
            cv2.circle(self.outlined_img, (self.center_x, self.center_y), 3, (0, 0, 255), -1)
            param.draw_diameter_while_freefall(self.outlined_img, left_ff, right_ff, touch)
            param.draw_diameter_while_freefall(self.outlined_img, up_ff, down_ff, touch)

        if self.leftmost:
            left_pts = param.select_tangent_points(largest_contour, self.leftmost, clockwise=False)
            left_tangent_angle, slope = param.calculate_tangent_angle(left_pts)
            self.left_angle = param.calculate_contact_angle(left_tangent_angle, line_angle, left=True) if left_tangent_angle else None
            if should_draw:
                param.draw_tangent(self.outlined_img, self.leftmost, slope)
                param.draw_contact_angle(self.outlined_img, line_angle, self.left_angle, self.leftmost, left=True)
                param.draw_selected_points(self.outlined_img, left_pts)

        if self.rightmost:
            right_pts = param.select_tangent_points(largest_contour, self.rightmost, clockwise=True)
            right_tangent_angle, slope = param.calculate_tangent_angle(right_pts)
            self.right_angle = param.calculate_contact_angle(right_tangent_angle, line_angle, left=False) if right_tangent_angle else None
            if should_draw:
                param.draw_tangent(self.outlined_img, self.rightmost, slope)
                param.draw_contact_angle(self.outlined_img, line_angle, self.right_angle, self.rightmost, left=False)
                param.draw_selected_points(self.outlined_img, right_pts)

        if self.save_to_disk:
            self.processed_file_name = f'processed_{self.filename}'
            output_path = os.path.join(self.output_folder, self.processed_file_name)
            cv2.imwrite(output_path, self.outlined_img)

    def get_final_image(self):
        return self.outlined_img if self.valid else None
