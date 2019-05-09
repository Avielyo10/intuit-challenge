#!/usr/bin/env python
import copy


def diff_even(area, q1_hunters, q1_boxes, q2_hunters, q2_boxes):
    """
    This method returns the value of the hunters that should be added.
    """
    if q1_boxes == q2_boxes:
        return (2 * area) - (q1_boxes + q2_boxes + q1_hunters + q2_hunters)

    else:
        max_boxes = q1_boxes
        min_boxes = q2_boxes
        max_hunters = q1_hunters
        min_hunters = q2_hunters

        if q2_boxes > q1_boxes:
            max_boxes = q2_boxes
            min_boxes = q1_boxes
            max_hunters = q2_hunters
            min_hunters = q1_hunters

        diff_boxes = max_boxes - min_boxes

        if min_boxes + min_hunters + diff_boxes <= area:
            return diff_even(area, max_hunters, max_boxes, min_hunters, min_boxes + diff_boxes)
        else:
            return -1


def diff_odd(n_boxes_up, n_boxes_down, n_boxes_left, n_boxes_right):
    # (left - right) : (up - down)
    return "{},{}".format((n_boxes_left-n_boxes_right), (n_boxes_up-n_boxes_down))


def resolve(diff):
    """
    This method resolves the differences between the halfs and maps it into characters
    :param diff: (left - right) : (up - down)
    :return: ans[0] - how much needs to be added, ans[1] - where we should add a box
    ans[2] - all the available sequences we can add a box into
    """
    ans = []
    possible_val = set()
    splited_diff = diff.split(",")
    x = splited_diff[0]
    y = splited_diff[1]

    char_x = "L"
    char_y = "U"

    x_int = int(x)
    y_int = int(y)

    if x_int == 0:
        char_x = "N"
    elif x_int > 0:
        char_x = "R"

    if y_int == 0:
        char_y = "N"
    elif y_int > 0:
        char_y = "D"

    if char_x != "N":
        possible_val.add("{},{}".format(char_x, "N"))
    if char_y != "N":
        possible_val.add("{},{}".format("N", char_y))

    possible_val.add("{},{}".format(char_x, char_y))
    ans.append("{}:{}".format(abs(x_int), abs(y_int)))
    ans.append("{}:{}".format(char_x, char_y))
    ans.append(possible_val)

    return ans


def how_much_place_is_left(area, n_boxes, n_hunters):
    return area - n_boxes - n_hunters


def get_possible_dict(numbers, letters, possible_vals):
    """
    This method returns a list with all the possible
    boxes combinations from the best solution to the worst
    :param numbers: The diff we need to add
    :param letters: Where e should add it to?
    :param possible_vals: Possible boxes combinations with no value
    :return: A list full of possible boxes combinations as dictionaries,
    specifying where we can add a box and how much
    """
    num_x, num_y = numbers.split(':')
    val_x, val_y = letters.split(':')
    ans = []

    best_case = min(int(num_x), int(num_y))
    no_n = None
    for possible_val in possible_vals:
        if "N" not in possible_val:
            no_n = possible_val

    tmp = {}.fromkeys(possible_vals, 0)
    tmp[no_n] = best_case

    with_n = "{},N".format(val_x)
    sec_best = max(int(num_x), int(num_y)) - best_case
    if num_y > num_x:
        with_n = "N,{}".format(val_y)
    tmp[with_n] = sec_best

    while best_case >= 0:
        ans.append(copy.deepcopy(tmp))
        for key in tmp:
            if key != no_n:
                tmp[key] += 1
        best_case -= 1
        tmp[no_n] = best_case
    return ans


class Case:
    def __init__(self, n_grid, boxes_points, hunters_points):
        self.n_grid = n_grid
        self.boxes_points = boxes_points
        self.hunters_points = hunters_points

    def get_grid_area(self):
        return int(self.n_grid) ** 2

    def play_even(self):
        n_all_hunters = sum(list(self.hunters_points.values()))
        n_all_boxes = sum(list(self.boxes_points.values()))

        # If there are no boxes, fill it all with hunters
        if n_all_boxes == 0:
            return self.get_grid_area() - n_all_hunters

        # If all the carpet is full of boxes,
        # so its already balanced and we can't add anymore hunters
        if n_all_boxes == self.get_grid_area():
            return 0

        q_area = (self.n_grid / 2) ** 2
        if q_area == self.boxes_points[1] == self.boxes_points[2] or \
            q_area == self.boxes_points[1] == self.boxes_points[3] or \
            q_area == self.boxes_points[4] == self.boxes_points[3] or \
            q_area == self.boxes_points[4] == self.boxes_points[2]:
            return -1

        a = diff_even(
            q_area, self.hunters_points[1], self.boxes_points[1], self.hunters_points[4], self.boxes_points[4])
        b = diff_even(
            q_area, self.hunters_points[2], self.boxes_points[2], self.hunters_points[3], self.boxes_points[3])

        if a == -1 or b == -1:
            return -1

        return a + b

    def play_odd(self):
        # Special case when there is no cross [1X1] so we don't need
        # to make any calculation since there are only 3 situations
        if self.n_grid == 1:
            if self.boxes_points["N,N"] == 1 or self.hunters_points["N,N"] == 1:
                return 0
            else:
                return 1

        # But if it's larger ..
        n_all_hunters = sum(list(self.hunters_points.values()))
        n_all_boxes = sum(list(self.boxes_points.values()))

        # If there are no boxes, fill it all with hunters
        if n_all_boxes == 0:
            return self.get_grid_area() - n_all_hunters

        # If all the carpet is full of boxes,
        # so its already balanced and we can't add anymore hunters
        if n_all_boxes == self.get_grid_area():
            return 0
        
        q_cross_size = self.n_grid/2
        q_size = q_cross_size ** 2
        half_size = 2 * q_size + 3* q_cross_size + 1

        n_boxes_up = self.boxes_points["L,U"] + \
            self.boxes_points["N,U"] + self.boxes_points["R,U"]
        n_boxes_down = self.boxes_points["L,D"] + \
            self.boxes_points["N,D"] + self.boxes_points["R,D"]
        n_boxes_left = self.boxes_points["L,U"] + \
            self.boxes_points["L,N"] + self.boxes_points["L,D"]
        n_boxes_right = self.boxes_points["R,U"] + \
            self.boxes_points["R,N"] + self.boxes_points["R,D"]

        n_row_cross = self.boxes_points["N,N"] + self.boxes_points["L,N"] + self.boxes_points["R,N"]
        n_column_cross = self.boxes_points["N,N"] + self.boxes_points["N,U"] + self.boxes_points["N,D"]
        # If some half of the carpet is full of boxes it's not a valid situation
        if n_boxes_up + n_row_cross == half_size or \
                n_boxes_down + n_row_cross == half_size or \
                n_boxes_left + n_column_cross == half_size or \
                n_boxes_right + n_column_cross == half_size:
            return -1

        diff = diff_odd(n_boxes_up, n_boxes_down, n_boxes_left, n_boxes_right)
        if diff == "0,0":
            return self.get_grid_area() - n_all_boxes - n_all_hunters

        # So its diff isn't 0,0 [which means unstable] and the carpet is already
        # full ==> not valid
        elif self.get_grid_area() == (n_all_hunters + n_all_boxes):
            return -1

        else:
            data = resolve(diff)
            splited_val = data[0].split(':')

            best_case = max(int(splited_val[0]), int(splited_val[1]))

            dict_data = {}.fromkeys(data[2], 0)
            for i in data[2]:
                tmp_area = q_size
                if "N" in i:
                    tmp_area = q_cross_size
                dict_data[i] = how_much_place_is_left(
                    tmp_area, self.boxes_points[i], self.hunters_points[i])

            # If we don't have enough space even for the best case, return -1
            if sum(list(dict_data.values())) < best_case:
                return -1

            all_possible_dicts = get_possible_dict(data[0], data[1], data[2])

            for possible_dict in all_possible_dicts:
                tmp = {
                    key: dict_data[key] - possible_dict.get(key, 0) for key in dict_data.keys()}
                if all(value >= 0 for value in tmp.values()):
                    return self.get_grid_area() - n_all_boxes - n_all_hunters - sum(list(possible_dict.values()))

            # If you get so far, you don't have a possible match ==> return -1
            return -1
