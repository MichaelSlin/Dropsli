import cv2
import numpy as np
import math

def select_tangent_points(contour, contact_point, num_points=7, clockwise=True):
    """Select points around the contact point for tangent calculation."""
    contact_index = None
    for i, point in enumerate(contour):
        if tuple(point[0]) == tuple(contact_point):
            contact_index = i
            break

    if contact_index is None:
        return []  # Contact point not found in contour

    selected_points = []
    step = 1 if clockwise else -1

    for i in range(num_points):
        index = (contact_index + i * step) % len(contour)
        selected_points.append(tuple(contour[index][0]))

    return selected_points

def draw_selected_points(outlined_image, selected_points):
    """Draw selected points on the image in red."""
    for point in selected_points:
        outlined_image[point[1], point[0]] = (0, 0, 255)  # Red color for selected points

def calculate_tangent_angle(selected_points):
    """Calculate the angle of the tangent relative to the positive X-axis, always measured clockwise."""
    if len(selected_points) < 2:
        return None  # Not enough points to calculate a tangent

    # Extract x and y coordinates
    x_coords = np.array([p[0] for p in selected_points])
    y_coords = np.array([p[1] for p in selected_points])

    # Проверка на вертикальную линию
    if np.std(x_coords) < 1e-3 or x_coords[-1] == x_coords[0]:  # Верхняя и нижняя координаты x отобранных точек совпадают
        return 90.0, float('inf')  # Вертикальная линия

    # Конструируем матрицу для метода наименьших квадратов
    A = np.vstack([x_coords, np.ones_like(x_coords)]).T
    slope, _ = np.linalg.lstsq(A, y_coords, rcond=None)[0]

    # Вычисляем угол
    tangent_angle = math.degrees(math.atan(slope))
    if tangent_angle < 0:
        tangent_angle += 180  # Приводим к диапазону [0, 180]

    return tangent_angle, slope


def draw_tangent(image, contact_point, slope, color=(255, 255, 0), thickness=1, length=50):
    """Draw the tangent line at the contact point."""
    if slope is None:
        return
    
    x0, y0 = contact_point
    
    if np.isinf(slope) or abs(slope) > 1e6:  # Вертикальная линия
        pt1 = (x0, y0 - length)
        pt2 = (x0, y0 + length)
    else:  # Обычный случай
        dx = int(length / math.sqrt(1 + slope ** 2))
        dy = int(slope * dx)
        pt1 = (x0 - dx, y0 - dy)
        pt2 = (x0 + dx, y0 + dy)
    
    cv2.line(image, pt1, pt2, color, thickness)

def calculate_contact_angle(tangent_angle, line_angle, left=True):
    """Calculate the contact angle measured inside the liquid phase."""
    if tangent_angle is None:
        return None

    if left:
        contact_angle = 180 - (tangent_angle - line_angle)
    else:
        contact_angle = (tangent_angle - line_angle)

    contact_angle = round(contact_angle, 2)

    return contact_angle

def draw_contact_angle(image, line_angle, contact_angle, contact_point, radius=10, color=(0, 255, 255), thickness=1, left=True):
    """Draw the contact angle as an arc inside the liquid phase."""
    if contact_angle is None:
        return
    
    if left:
        start_angle = int(line_angle)
        end_angle = -1 * (int(start_angle) + int(contact_angle))
    else:
        start_angle = int(line_angle) + 180
        end_angle = int(start_angle) + int(contact_angle)
    
    cv2.ellipse(image, contact_point, (radius, radius), 0, start_angle, end_angle, color, thickness)


def find_leftmost_and_rightmost_points(largest_contour, line_coordinates) -> tuple[tuple, tuple, bool]:
    # Define the oblique line based on the selected points
    (x1, y1), (x2, y2) = line_coordinates

    # Find the leftmost and rightmost contact points
    leftmost = None
    rightmost = None
    touch = False
    for point in largest_contour:
        px, py = point[0]
        y_line = int(y1 + (y2 - y1) * (px - x1) / (x2 - x1))
        if abs(py - y_line) <= 1:  # Check if the point is near the blue line
            if leftmost is None or px < leftmost[0]:
                leftmost = (px, py)
            if rightmost is None or px > rightmost[0]:
                rightmost = (px, py)

    if leftmost and rightmost:
        touch = True

    return leftmost, rightmost, touch

def calculate_contact_width(leftmost:tuple, rightmost:tuple, touch:bool) -> float:
    # Calculate the contact width using the Pythagorean theorem
    if touch is True:
        contact_width = math.sqrt((rightmost[0] - leftmost[0]) ** 2 + (rightmost[1] - leftmost[1]) ** 2)
        contact_width = round(contact_width, 4)
    else:
        contact_width = None
        leftmost = None
        rightmost = None

    return contact_width
    
def compute_center_of_mass(largest_contour) -> tuple[int, int]:
    # Compute the center of mass
    moments = cv2.moments(largest_contour)
    if moments["m00"] != 0:
        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])
    else:
        center_x, center_y = None, None

    return center_x, center_y

def compute_horizontal_diameter_while_freefall(largest_contour, center_y:int, touch:bool) -> tuple[float, tuple, tuple]:
    # Вычисление ширины капли в ее в центре при свободном падении
    if touch is False:
        left_and_right_x_list = []

        for point in largest_contour:
            px, py = point[0]
            if py == center_y:
                left_and_right_x_list.append(px)

        left_x = min(left_and_right_x_list)
        right_x = max(left_and_right_x_list)

        left_freefall = (left_x, center_y)
        right_freefall = (right_x, center_y)
        horizontal_diameter_freefall = right_x - left_x
    else:
        left_freefall = None
        right_freefall = None
        horizontal_diameter_freefall = None

    return horizontal_diameter_freefall, left_freefall, right_freefall


def compute_vertical_diameter_while_freefall(largest_contour, center_x:int, touch:bool) -> tuple[float, tuple, tuple]:
    # Вычисление ширины капли в ее в центре при свободном падении
    if touch is False:
        up_and_down_y_list = []

        for point in largest_contour:
            px, py = point[0]
            if px == center_x:
                up_and_down_y_list.append(py)

        up_y = min(up_and_down_y_list)
        down_y = max(up_and_down_y_list)

        up_freefall = (center_x, up_y)
        down_freefall = (center_x, down_y)
        vertical_diameter_freefall = down_y - up_y
    else:
        up_freefall = None
        down_freefall = None
        vertical_diameter_freefall = None

    return vertical_diameter_freefall, up_freefall, down_freefall


def compute_drop_volume(largest_contour) -> float:
    # Переменная line_coordinates не нужна, так как контур капли уже создан с учетом наклона поверхности
    def get_y_width(largest_contour, y_current):
        left_and_right_x_list = []
        for point in largest_contour:
            px, py = point[0]
            if py == y_current:
                left_and_right_x_list.append(px)

        left_x = min(left_and_right_x_list)
        right_x = max(left_and_right_x_list)
        y_width = (right_x - left_x) + 1
        # Единица добавляется, т.к. при (left_x == right_x) (y_width == 0), хотя ширина, очевидно, равна одному пикселю
        return y_width

    y_coordinates_set = {point[0][1] for point in largest_contour}

    y_sorted_tuple = sorted(tuple(y_coordinates_set))

    area_list = []

    for y in y_sorted_tuple:
        y_width = get_y_width(largest_contour, y)
        area = (math.pi * (y_width ** 2)) / 4
        area_list.append(area)

    volume_pxl = sum(area_list)

    volume_mm3 = volume_pxl * ((1 / 57) ** 3)

    volume_mm3 = round(volume_mm3, 4)
    return volume_mm3
             

def draw_diameter_while_freefall(outlined_img, freefall_point_1:tuple, freefall_point_2:tuple, touch:bool):
    if touch is False:
        cv2.line(outlined_img, freefall_point_1, freefall_point_2, (0, 250, 255), 1)


def draw_contact_points(outlined_img, leftmost:tuple, rightmost:tuple, touch:bool):
    if touch is True:
        cv2.circle(outlined_img, leftmost, 1, (0, 250, 255), -1)  # Yellow dot for leftmost
        cv2.circle(outlined_img, rightmost, 1, (0, 250, 255), -1)  # Yellow dot for rightmost
