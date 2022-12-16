package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	inputFile  = "inputs/small-input.txt" // input.txt"
	startTime  = 30
	startValve = "AA"
	pathDelim  = "->"
)

type node struct {
	name      string
	flowRate  int
	neighbors map[string]struct{}
}

type drainer struct {
	graph       map[string]*node
	steps       int
	maxPressure int
	bestPath    string
}

func main() {
	graph := parseGraph()
	// for _, node := range graph {
	// 	fmt.Printf("%+v\n", node)
	// }

	d := &drainer{
		graph: graph,
	}
	d.drain(startValve, startTime, 0, 0, startValve, make(map[string]struct{}))

	fmt.Printf("start time: %d. start valve: %s\n", startTime, startValve)
	fmt.Printf("max pressure: %d. path: %s\n", d.maxPressure, d.bestPath)
	fmt.Printf("total iterations: %d\n", d.steps)
}

func (d *drainer) drain(valveName string, t, totalFlow, pressure int, path string, visited map[string]struct{}) {
	d.steps += 1
	if d.steps%10000000 == 0 {
		fmt.Printf("steps: %d\n", d.steps)
	}

	if t == 0 {
		if pressure > d.maxPressure {
			d.maxPressure = pressure
			d.bestPath = path
		}
		return
	}

	t = t - 1
	pressure += totalFlow
	visited[valveName] = struct{}{}
	valve := d.graph[valveName]

	for n := range valve.neighbors {
		if _, ok := visited[n]; ok {
			continue
		}

		newPath := path + pathDelim + n
		d.drain(n, t, totalFlow, pressure, newPath, visited)
	}

	if valve.flowRate > 0 {
		oldFlow := valve.flowRate
		valve.flowRate = 0
		oldVisited := visited
		visited = map[string]struct{}{
			valveName: {},
		}

		newPath := path + pathDelim + fmt.Sprintf("OPEN(%d)", oldFlow)
		d.drain(valveName, t, totalFlow+oldFlow, pressure, newPath, visited)

		valve.flowRate = oldFlow
		visited = oldVisited
	}

	delete(visited, valveName)
}

func parseGraph() map[string]*node {
	graph := make(map[string]*node)
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		srcValve := line[6:8]

		flowStr := strings.Split(line, "rate=")[1]
		flowStr = strings.Split(flowStr, ";")[0]

		dstValveStr := line[strings.Index(line, "valve"):]
		dstValveStr = dstValveStr[strings.Index(dstValveStr, " ")+1:]
		dstValves := make(map[string]struct{})
		for _, v := range strings.Split(dstValveStr, ", ") {
			dstValves[v] = struct{}{}
		}

		fr, _ := strconv.Atoi(flowStr)
		graph[srcValve] = &node{
			name:      srcValve,
			flowRate:  fr,
			neighbors: dstValves,
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return graph
}
