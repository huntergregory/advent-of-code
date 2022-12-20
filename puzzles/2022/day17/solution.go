package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

// NOTE: all coordinates are in form (y,x)

/*
	Part 2 Brute Force Translation Results:
	Would take **33 hours** for 1 trillion rounds (~2m/1B rounds).

	N=500M. H=25K --> t=1m15s
	N=1B. H=25K --> t=2m19s
	N=1B. H=50K --> t=2m30s
	N=2B. H=25K --> t=4m20s
	N=4B. H=25K --> t=8m20s
*/

type rockType string
type state uint8

// numbers
const (
	thousand = 1000
	million  = 1000000
	billion  = 1000 * million
	// for more than about 2.5 billion, requires system's int to be int64
	trillion = 1000 * billion
)

// parameters
const (
	numRounds = 10000
	inputFile = "inputs/input.txt"
	debug     = false

	gridHeight = numRounds*4 + 3
	// gridHeight = 25 * thousand

	// part 2 (cycle-based)
	rockToExtrapolate   = trillion
	cycleStartRound     = 1000
	lengthToDetectCycle = 100
	minimumCycleLength  = 20
)

// part 2 (brute force translation)
// this approach takes WAY too long
// const (
// 	translate = true
// 	// translateBuffer is the space allowed between top and gridHeight
// 	// must be much less than gridHeight
// 	translateBuffer = 100
// 	// translatedTop is the top after translation
// 	// must be much less than gridHeight
// 	translatedTop = 500
// )

// constants
const (
	clear   state = 0
	falling state = 1
	solid   state = 2

	width             = 7
	largestRockHeight = 4
	startOffsetY      = 3
	startOffsetX      = 2

	minus        rockType = "minus"
	plus         rockType = "plus"
	backwardsL   rockType = "backwards-L"
	verticalLine rockType = "vertical-line"
	square       rockType = "square"
)

// variable constants
var (
	rockTypeOrder = []rockType{
		minus,
		plus,
		backwardsL,
		verticalLine,
		square,
	}
	numRockTypes = len(rockTypeOrder)
	// rockTypeOffsets holds the points of the rock types
	rockTypeOffsets = map[rockType][][2]int{
		minus: {
			{0, 0},
			{0, 1},
			{0, 2},
			{0, 3},
		},
		plus: {
			{1, 0},
			{1, 1},
			{1, 2},
			{0, 1},
			{2, 1},
		},
		backwardsL: {
			{0, 0},
			{0, 1},
			{0, 2},
			{1, 2},
			{2, 2},
		},
		verticalLine: {
			{0, 0},
			{1, 0},
			{2, 0},
			{3, 0},
		},
		square: {
			{0, 0},
			{0, 1},
			{1, 0},
			{1, 1},
		},
	}
	rockTypeHeights = map[rockType]int{
		minus:        1,
		plus:         3,
		backwardsL:   3,
		verticalLine: 4,
		square:       2,
	}

	xDeltas = map[rune]int{
		'<': -1,
		'>': 1,
	}

	stateToChar = map[state]string{
		clear:   ".",
		falling: "@",
		solid:   "#",
	}
)

func main() {
	actions := parseActions()

	var grid [gridHeight][width]state
	top := 0
	// part 2 (cycle based)
	roundTops := make([]int, numRounds)
	// part 2 (brute force translation)
	// topTotal := 0

	actionIndex := 0
	// var round int64
	for round := 0; round < numRounds; round++ {
		rockPos := [2]int{top + startOffsetY, startOffsetX}
		rockType := rockTypeOrder[round%numRockTypes]
		offsets := rockTypeOffsets[rockType]

		updateState := func(s state) {
			for _, o := range offsets {
				y := rockPos[0] + o[0]
				x := rockPos[1] + o[1]
				grid[y][x] = s
			}
		}

		if debug {
			updateState(falling)
			fmt.Printf("rock %d at beginning\n", int(round+1))
			displayGrid(grid, rockPos[0]+rockTypeHeights[rockType]-1, 20)
			updateState(clear)
		}

		for {
			// try action
			xDelta := actions[actionIndex%len(actions)]
			actionIndex++
			// shift
			rockPos[1] += xDelta
			blocked := false
			for _, o := range offsets {
				y := rockPos[0] + o[0]
				x := rockPos[1] + o[1]
				if x < 0 || x >= width || grid[y][x] == solid {
					blocked = true
					break
				}
			}
			if blocked {
				// undo shift
				rockPos[1] -= xDelta
			}

			if debug {
				updateState(falling)
				fmt.Printf("rock %d after action %d before falling\n", int(round+1), int(actionIndex))
				displayGrid(grid, rockPos[0]+rockTypeHeights[rockType]-1, 20)
				updateState(clear)
			}

			// try move down
			rockPos[0] -= 1
			blocked = false
			for _, o := range offsets {
				y := rockPos[0] + o[0]
				x := rockPos[1] + o[1]
				if y < 0 || grid[y][x] == solid {
					blocked = true
					break
				}
			}
			if blocked {
				// undo shift
				rockPos[0] += 1
				// stop processing rock
				break
			}
		}

		newTop := rockPos[0] + rockTypeHeights[rockType]
		if newTop > top {
			top = newTop
		}
		updateState(solid)

		// part 2 (cycle-based)
		roundTops[round] = top

		// part 2 (brute force translation)
		// this approach takes WAY too long
		// if translate {
		// 	if top >= int(gridHeight)-translateBuffer {
		// 		for y := 0; y <= translatedTop; y++ {
		// 			for x := 0; x < width; x++ {
		// 				grid[y][x] = grid[top-translatedTop+y][x]
		// 			}
		// 		}

		// 		for y := translatedTop + 1; y <= top; y++ {
		// 			for x := 0; x < width; x++ {
		// 				grid[y][x] = clear
		// 			}
		// 		}

		// 		topTotal += top - translatedTop
		// 		top = translatedTop
		// 	}
		// }
	}

	fmt.Printf("finished all %d rocks\n", int(numRounds))
	// you can see cycles if you increase the yDiff (last arg) in displayGrid()
	displayGrid(grid, top, 20)
	fmt.Printf("top of tower: %d\n", top)
	// part 2 (brute force translation)
	// fmt.Printf("top of tower: %d\n", top+topTotal)

	// part 2 (cycle-based)
	part2CycleBased(grid, roundTops)
}

func part2CycleBased(grid [gridHeight][width]state, roundTops []int) {
	foundCycle := false
	for rightStart := cycleStartRound + lengthToDetectCycle; rightStart+lengthToDetectCycle < len(roundTops); rightStart++ {
		if foundCycle {
			break
		}

		for diff := 0; rightStart+diff < len(roundTops); diff++ {
			leftTop := roundTops[cycleStartRound+diff] - roundTops[cycleStartRound]
			rightTop := roundTops[rightStart+diff] - roundTops[rightStart]
			if leftTop != rightTop {
				break
			}

			if diff == lengthToDetectCycle {
				foundCycle = true
				break
			}
		}
	}

	if !foundCycle {
		fmt.Println("did NOT find cycle")
		return
	}

	// determine cycle length
	cycleLength := minimumCycleLength
	for {
		success := true
		for diff := 0; diff < cycleLength; diff++ {
			leftTop := roundTops[cycleStartRound+diff] - roundTops[cycleStartRound]
			rightTop := roundTops[cycleStartRound+cycleLength+diff] - roundTops[cycleStartRound+cycleLength]
			if leftTop != rightTop {
				success = false
				break
			}
		}
		if success {
			break
		}
		cycleLength++
	}

	periodicDiff := roundTops[cycleStartRound+cycleLength] - roundTops[cycleStartRound]
	fmt.Printf("cycle starting at round %d (top=%d) with length %d\n", cycleStartRound, roundTops[cycleStartRound], cycleLength)
	fmt.Printf("periodic diff is %d every %d rounds\n", periodicDiff, cycleLength)

	// roundTop[i] is top after i+1 rocks have fallen...
	// want index == rockToExtrapolate-1
	// index == numRepeats*cycleLength + remainder
	numRepeats := (rockToExtrapolate - 1 - cycleStartRound) / cycleLength
	remainder := (rockToExtrapolate - 1 - cycleStartRound) % cycleLength
	periodicDiff = roundTops[cycleStartRound+remainder+cycleLength] - roundTops[cycleStartRound+remainder]
	extrapolatedTop := roundTops[cycleStartRound+remainder] + periodicDiff*numRepeats

	fmt.Printf("(extrapolated) top after %d rounds is %d\n", rockToExtrapolate, extrapolatedTop)
}

func displayGrid(grid [gridHeight][width]state, top, yDiff int) {
	bottom := top - yDiff
	if bottom < 0 {
		bottom = 0
	}
	for y := top; y >= bottom; y-- {
		fmt.Print("|")
		for x := 0; x < width; x++ {
			fmt.Print(stateToChar[grid[y][x]])
		}
		fmt.Println("|")
	}
	fmt.Print("+")
	for x := 0; x < width; x++ {
		fmt.Print("-")
	}
	fmt.Println("+")
	fmt.Println()
}

func parseActions() []int {
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var line string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line = scanner.Text()
		break
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	actions := make([]int, len(line))
	for i, c := range line {
		xDelta, ok := xDeltas[c]
		if !ok {
			fmt.Println("INVALID ACTION!")
		}
		actions[i] = xDelta
	}

	if debug {
		fmt.Println(actions)
	}

	return actions
}
