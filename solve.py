#!/usr/bin/env python

import sys
from case import Case

NUMBER_OF_CASES = None
ITR = 1


def where_to_go_odd(n_grid, x, y):
    mid = n_grid / 2
    if x == mid + 1 and y == mid + 1:
        return "N,N"
    elif x <= mid and y <= mid:
        return "L,U"
    elif x == mid + 1 and y <= mid:
        return "L,N"
    elif x > mid + 1 and y <= mid:
        return "L,D"
    elif x > mid + 1 and y == mid + 1:
        return "N,D"
    elif x > mid + 1 and y > mid + 1:
        return "R,D"
    elif x == mid + 1 and y > mid + 1:
        return "R,N"
    elif x <= mid and y > mid + 1:
        return "R,U"
    else:
        return "N,U"


def where_to_go_even(n_grid, x, y):
    mid = n_grid / 2
    if x <= mid and y <= mid:
        return 1
    elif x <= mid and y > mid:
        return 2
    elif x > mid and y <= mid:
        return 3
    else:
        return 4


def parse_and_play(input_file):
    n_grid = 0
    n_boxes = 0
    n_hunters = 0

    boxes_points_even = {}.fromkeys([1, 2, 3, 4], 0)
    hunters_points_even = {}.fromkeys([1, 2, 3, 4], 0)
    boxes_points_odd = {}.fromkeys(["L,U", "L,N", "L,D", "N,D", "R,D", "R,N", "R,U", "N,U", "N,N"], 0)
    hunters_points_odd = {}.fromkeys(["L,U", "L,N", "L,D", "N,D", "R,D", "R,N", "R,U", "N,U", "N,N"], 0)

    with open(input_file, "r") as in_file:
        global NUMBER_OF_CASES
        global ITR
        for line in in_file:
            if NUMBER_OF_CASES is None:
                NUMBER_OF_CASES = int(line)

            else:
                if n_grid == 0:
                    splited_line = line.split(' ')
                    n_grid = int(splited_line[0])
                    n_boxes = int(splited_line[1])
                    n_hunters = int(splited_line[2])

                elif n_boxes > 0:
                    n_boxes -= 1
                    splited = line.split(' ')
                    if n_grid % 2 == 0:
                        boxes_points_even[where_to_go_even(n_grid, int(splited[0]), int(splited[1]))] += 1
                    else:
                        boxes_points_odd[where_to_go_odd(n_grid, int(splited[0]), int(splited[1]))] += 1

                elif n_boxes == 0 and n_hunters > 0:
                    n_hunters -= 1
                    splited = line.split(' ')
                    if n_grid % 2 == 0:
                        hunters_points_even[where_to_go_even(n_grid, int(splited[0]), int(splited[1]))] += 1
                    else:
                        hunters_points_odd[where_to_go_odd(n_grid, int(splited[0]), int(splited[1]))] += 1

            if n_boxes == 0 and n_hunters == 0 and n_grid > 0:
                if n_grid % 2 == 0:
                    print "Case #{}: {}".format(ITR, Case(n_grid, boxes_points_even, hunters_points_even).play_even())
                    boxes_points_even = {}.fromkeys([1, 2, 3, 4], 0)
                    hunters_points_even = {}.fromkeys([1, 2, 3, 4], 0)
                else:
                    print "Case #{}: {}".format(ITR, Case(n_grid, boxes_points_odd, hunters_points_odd).play_odd())
                    boxes_points_odd = {}.fromkeys(["L,U", "L,N", "L,D", "N,D", "R,D", "R,N", "R,U", "N,U", "N,N"], 0)
                    hunters_points_odd = {}.fromkeys(["L,U", "L,N", "L,D", "N,D", "R,D", "R,N", "R,U", "N,U", "N,N"], 0)
                n_grid = 0
                ITR += 1
        NUMBER_OF_CASES = None


def main():
    if len(sys.argv) == 2:
        parse_and_play(sys.argv[1])

    else:
        print "Usage: python solve.py [FILE]"


if __name__ == '__main__':
    main()
