package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

// parameters
const (
	inputFile = "inputs/input.txt"

	// part 1
	// startChar      = 'S'
	// startElevation = 'a'
	// endChar        = 'E'
	// endElevation   = 'z'

	// part 2 (also need to update elevationDelta)
	reverseElevationDelta = true
	startChar             = 'E'
	startElevation        = 'z'
	endChar               = 'a'
	endElevation          = 'a'
)

type direction string

// constants
const (
	left  direction = "<"
	right direction = ">"
	up    direction = "^"
	down  direction = "v"
)

// constant variables
var (
	// directionDeltas contains changes in (y,x), where y increases downwards
	directionDeltas = map[direction][2]int{
		left:  {0, -1},
		right: {0, 1},
		up:    {-1, 0},
		down:  {1, 0},
	}
)

type path struct {
	// position is the current location
	position [2]int
	steps    []direction
}

func main() {
	grid := parseInput()

	// find startPos
	startPos := [2]int{-1, -1}
	for i, row := range grid {
		for j, c := range row {
			if c == startChar {
				startPos = [2]int{i, j}
			}
		}
	}
	if startPos[0] == -1 {
		fmt.Println("error: couldn't find start")
		return
	}

	bestPath(grid, startPos)
}

func bestPath(grid [][]rune, startPos [2]int) {
	queue := make([]*path, 0)
	queue = append(queue, &path{
		position: startPos,
		steps:    make([]direction, 0),
	})

	visited := make(map[[2]int]struct{})
	visited[startPos] = struct{}{}

	numRows := len(grid)
	numCols := len(grid[0])
	for len(queue) > 0 {
		p := queue[0]
		queue = queue[1:]
		for dir, delta := range directionDeltas {
			newPos := [2]int{
				p.position[0] + delta[0],
				p.position[1] + delta[1],
			}

			if newPos[0] < 0 || newPos[0] >= numRows || newPos[1] < 0 || newPos[1] >= numCols {
				// out of bounds
				continue
			}

			// ignore visited
			if _, ok := visited[newPos]; ok {
				continue
			}

			// verify this is a legal step
			oldElevation := grid[p.position[0]][p.position[1]]
			if oldElevation == startChar {
				oldElevation = startElevation
			}
			newChar := grid[newPos[0]][newPos[1]]
			newElevation := newChar
			if newElevation == endChar {
				newElevation = endElevation
			}
			// part 1
			// elevationDelta := newElevation - oldElevation
			// part 2
			elevationDelta := oldElevation - newElevation
			if elevationDelta > 1 {
				// too big a climb
				continue
			}

			newSteps := make([]direction, 0, len(p.steps)+1)
			newSteps = append(newSteps, p.steps...)
			newSteps = append(newSteps, dir)
			if newChar == endChar {
				// reached end
				fmt.Printf("best path: %+v\n", newSteps)
				fmt.Printf("number of steps: %d\n", len(newSteps))
				return
			}

			// enqueue next step for DFS
			visited[newPos] = struct{}{}
			queue = append(queue, &path{
				position: newPos,
				steps:    newSteps,
			})
		}
	}

	fmt.Println("error: did not find end")
}

// parseInput returns the grid
func parseInput() [][]rune {
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	graph := make([][]rune, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		text := scanner.Text()
		row := make([]rune, len(text))
		for i, c := range text {
			row[i] = c
		}
		graph = append(graph, row)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return graph
}
