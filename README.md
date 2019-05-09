# Intuit Challenge - Solution Explanation

The idea behind the solution was to relate the carpet as a grid and hunter/box as a point.  
We have to main problems:  

1. Even grid.
2. Odd grid.  

We will map every point to its right position according to the problem we are dealing with.  
To make this solution as efficient as possible I programmed it such it will parse and play the right case on run time, this will save memory space and time (all the calculations are made during the file reading).  
There is no meaning to the x & y point values only to the kind of the point (hunter/box) and to the position of it on top of the grid. Which means we don't have to hold so much data, only to extract all the information we can from each point.  

## Even grid

Example of how I mapped the even grid:

| 1 | 2 |  
| 3 | 4 |  

The solution for the even grid is very straightforward, we can balance the grid if and only if every two opposite quarters (1 & 4, 2 & 3) are having the same number of boxes, if not we will try to add boxes as minimum we can so the number of the boxes will be even.  
Of course we need to consider pre-seated hunters.

## Odd grid  

Example of how I mapped the odd grid:

| L,U | N,U | R,U |  
| L,N | N,N | R,N |  
| L,D | N,D | R,D |  

Here the solution is much more complicated.  
The first step was to calculate the number of the boxes **(Left - Right)** and **(Up - Down)** [without the middle row/column - since its weight splits equally between the halves] and make some coordinate like `-5:7` which means we are missing 5 boxes Left and 7 on Down.  
Second step is resolving the coordinate.  
For example `-5:7` into:  

1. `5:7` - The amount of boxes we need to add.
2. `L,D` - Where we are missing boxes.
3. `L,D`, `L,N`, `N,D` - All the places we can add boxes to balance the grid.

The third step is to get all the possible divisions, using the second step example we get:

1. `L,D:5`, `N,D:2`, `L,N:0`. - The best division only 7 boxes to add in total.
2. `L,D:4`, `N,D:3`, `L,N:1`.
3. `L,D:3`, `N,D:4`, `L,N:2`.
4. `L,D:2`, `N,D:5`, `L,N:3`.
5. `L,D:1`, `N,D:6`, `L,N:4`.
6. `L,D:0`, `N,D:7`, `L,N:5`. - The worst division, 12 boxes in total.

The fourth step is to check all the available space within `L,D`, `L,N`, `N,D`, considering already seated hunters. For example we will get `L,D:3`, `L,N:5`, `N,D:4`, we now compare it against all the possible divisions, options 1 & 2 can't fit so we will jump right into option 3 sum up all the boxes for this option and we have 9 more boxes to add.

If there is no possible match, return -1.