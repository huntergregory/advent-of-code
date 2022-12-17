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
	inputFile  = "inputs/small-input.txt"
	startTime  = 10
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

type person struct {
	valveName string
	path      string
	visited   map[string]struct{}
}

func main() {
	graph := parseGraph()
	// for _, node := range graph {
	// 	fmt.Printf("%+v\n", node)
	// }

	d := &drainer{
		graph: graph,
	}
	// d.drain(startValve, startTime, 0, 0, startValve, make(map[string]struct{}))
	d.drain(startTime, 0, 0, []*person{
		{
			valveName: startValve,
			path:      startValve,
			visited:   make(map[string]struct{}),
		},
		{
			valveName: startValve,
			path:      startValve,
			visited:   make(map[string]struct{}),
		},
	})

	fmt.Printf("start time: %d. start valve: %s\n", startTime, startValve)
	fmt.Printf("max pressure: %d\n", d.maxPressure)
	fmt.Printf("path:\n%s\n", d.bestPath)
	fmt.Printf("total iterations: %d\n", d.steps)
}

// with double visited resets, get to >180000000 for 26 small-input
func (d *drainer) drain(t, totalFlow, pressure int, people []*person) {
	d.steps += 1
	if d.steps%10000000 == 0 {
		fmt.Printf("steps: %d\n", d.steps)
	}

	if t == 0 {
		// fmt.Printf("here. t=%d. totalFlow=%d. pressure=%d. p0=%+v. p1=%+v\n", t, totalFlow, pressure, people[0], people[1])
		if pressure > d.maxPressure {
			d.maxPressure = pressure
			path := "PERSON0: " + people[0].path + "\nPERSON1: " + people[1].path
			d.bestPath = path
			fmt.Printf("best pressure [%d] with total flow [%d]\n", pressure, totalFlow)
		}
		return
	}

	t -= 1
	pressure += totalFlow

	anyOptions := false

	p0 := people[0]
	p1 := people[1]
	v0 := d.graph[p0.valveName]
	v1 := d.graph[p1.valveName]

	p0.visited[p0.valveName] = struct{}{}
	p1.visited[p1.valveName] = struct{}{}

	// p0 neighbors with p1 neighbors or p1 open
	for n0 := range v0.neighbors {
		if _, ok := p0.visited[n0]; ok {
			// assuming there will always be at least one neighbor to go to
			continue
		}

		newP0 := &person{
			valveName: n0,
			path:      p0.path + pathDelim + n0,
			visited:   p0.visited,
		}

		for n1 := range v1.neighbors {
			if _, ok := p1.visited[n1]; ok {
				continue
			}

			newP1 := &person{
				valveName: n1,
				path:      p1.path + pathDelim + n1,
				visited:   p1.visited,
			}

			d.drain(t, totalFlow, pressure, []*person{newP0, newP1})
			anyOptions = true
		}

		if v1.flowRate > 0 {
			// newP0.visited = make(map[string]struct{})

			oldFlow1 := v1.flowRate
			v1.flowRate = 0
			newP1 := &person{
				valveName: v1.name,
				path:      p1.path + pathDelim + fmt.Sprintf("OPEN(%d)", oldFlow1),
				visited: map[string]struct{}{
					v1.name: {},
				},
			}

			d.drain(t, totalFlow+oldFlow1, pressure, []*person{newP0, newP1})
			anyOptions = true

			v1.flowRate = oldFlow1
		}
	}

	// p1 neighbors with p0 open
	for n1 := range v1.neighbors {
		if _, ok := p1.visited[n1]; ok {
			// assuming there will always be at least one neighbor to go to
			continue
		}

		newP1 := &person{
			valveName: n1,
			path:      p1.path + pathDelim + n1,
			visited:   p1.visited, // make(map[string]struct{}),
		}

		if v0.flowRate > 0 {
			oldFlow0 := v0.flowRate
			v0.flowRate = 0
			newP0 := &person{
				valveName: v0.name,
				path:      p0.path + pathDelim + fmt.Sprintf("OPEN(%d)", oldFlow0),
				visited: map[string]struct{}{
					v0.name: {},
				},
			}

			d.drain(t, totalFlow+oldFlow0, pressure, []*person{newP0, newP1})
			anyOptions = true

			v0.flowRate = oldFlow0
		}
	}

	// p0 and p1 open
	if v0.flowRate > 0 {
		oldFlow0 := v0.flowRate
		v0.flowRate = 0
		newP0 := &person{
			valveName: v0.name,
			path:      p0.path + pathDelim + fmt.Sprintf("OPEN(%d)", oldFlow0),
			visited: map[string]struct{}{
				v0.name: {},
			},
		}

		if v1.flowRate > 0 {
			oldFlow1 := v1.flowRate
			v1.flowRate = 0
			newP1 := &person{
				valveName: v1.name,
				path:      p1.path + pathDelim + fmt.Sprintf("OPEN(%d)", oldFlow1),
				visited: map[string]struct{}{
					v1.name: {},
				},
			}

			d.drain(t, totalFlow+oldFlow0+oldFlow1, pressure, []*person{newP0, newP1})
			anyOptions = true

			v1.flowRate = oldFlow1
		}

		v0.flowRate = oldFlow0
	}

	if !anyOptions {
		d.drain(t, totalFlow, pressure, people)
	}

	delete(p0.visited, p0.valveName)
	delete(p1.visited, p1.valveName)
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
