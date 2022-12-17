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
	startValve = "AA"
	pathDelim  = "->"
	sameSpot   = "STAY"

	startTime = 26
	inputFile = "../inputs/small-input.txt"
	DEBUG     = false
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

func newPersonAt(valve string) *person {
	return &person{
		valveName: startValve,
		path:      startValve,
		visited: map[string]struct{}{
			startValve: {},
		},
	}
}

func (p *person) moveTo(valve string) *person {
	if valve == sameSpot {
		return &person{
			valveName: p.valveName,
			path:      p.path + pathDelim + sameSpot,
			visited:   copy(p.visited), // technically don't need to copy
		}
	}

	return &person{
		valveName: valve,
		path:      p.path + pathDelim + valve,
		visited:   copy(p.visited),
	}
}

func (p *person) open(flow int) *person {
	return &person{
		valveName: p.valveName,
		path:      p.path + pathDelim + fmt.Sprintf("OPEN(%d)", flow),
		visited: map[string]struct{}{
			p.valveName: {},
		},
	}
}

func main() {
	graph := parseGraph()
	if DEBUG {
		for _, node := range graph {
			fmt.Printf("%+v\n", node)
		}
	}

	d := &drainer{
		graph: graph,
	}
	d.drain(startTime, 0, 0, []*person{newPersonAt(startValve), newPersonAt(startValve)})

	fmt.Printf("start time: %d. start valve: %s\n", startTime, startValve)
	fmt.Printf("max pressure: %d\n", d.maxPressure)
	fmt.Printf("path:\n%s\n", d.bestPath)
	fmt.Printf("total iterations: %d\n", d.steps)
}

func (d *drainer) drain(t, totalFlow, pressure int, people []*person) {
	d.steps += 1
	if d.steps%10000000 == 0 {
		fmt.Printf("steps: %d\n", d.steps)
	}

	if DEBUG {
		fmt.Printf("here. t=%d. totalFlow=%d. pressure=%d. p0=%+v. p1=%+v\n", t, totalFlow, pressure, people[0], people[1])
	}

	if t == 0 {
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

	p0 := people[0]
	p1 := people[1]
	v0 := d.graph[p0.valveName]
	v1 := d.graph[p1.valveName]

	options0 := make([]string, 0)
	for n := range v0.neighbors {
		if _, ok := p0.visited[n]; ok {
			continue
		}
		options0 = append(options0, n)
		p0.visited[n] = struct{}{}
	}
	if len(options0) == 0 && v0.flowRate == 0 {
		options0 = append(options0, sameSpot)
	}

	options1 := make([]string, 0)
	for n := range v1.neighbors {
		if _, ok := p1.visited[n]; ok {
			continue
		}
		options1 = append(options1, n)
		p1.visited[n] = struct{}{}
	}
	if len(options1) == 0 && (v1.flowRate == 0 || v0 == v1) {
		options1 = append(options1, sameSpot)
	}

	for _, n0 := range options0 {
		if v1.flowRate > 0 {
			oldFlow1 := v1.flowRate
			v1.flowRate = 0
			d.drain(t, totalFlow+oldFlow1, pressure, []*person{p0.moveTo(n0), p1.open(oldFlow1)})
			v1.flowRate = oldFlow1
		}
	}

	for _, n1 := range options1 {
		if v0.flowRate > 0 {
			oldFlow0 := v0.flowRate
			v0.flowRate = 0
			d.drain(t, totalFlow+oldFlow0, pressure, []*person{p0.open(oldFlow0), p1.moveTo(n1)})
			v0.flowRate = oldFlow0
		}
	}

	if v0 != v1 && v0.flowRate > 0 && v1.flowRate > 0 {
		oldFlow0 := v0.flowRate
		v0.flowRate = 0
		oldFlow1 := v1.flowRate
		v1.flowRate = 0
		d.drain(t, totalFlow+oldFlow0+oldFlow1, pressure, []*person{p0.open(oldFlow0), p1.open(oldFlow1)})
		v0.flowRate = oldFlow0
		v1.flowRate = oldFlow1
	}

	for _, n0 := range options0 {
		for _, n1 := range options1 {
			d.drain(t, totalFlow, pressure, []*person{p0.moveTo(n0), p1.moveTo(n1)})
		}
	}
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

func copy(m map[string]struct{}) map[string]struct{} {
	result := make(map[string]struct{}, len(m))
	for k := range m {
		result[k] = struct{}{}
	}
	return result
}
