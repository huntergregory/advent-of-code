package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// parameters
const (
	inputFile = "inputs/input.txt"
	DEBUG     = false
)

type pair struct {
	a float64
	b float64
}

func main() {
	input := parseInput()
	if DEBUG {
		fmt.Println(input)
	}

	root, ok := input["root"]
	if !ok {
		log.Fatal("expected root in input")
	}

	// part 1
	memo := make(map[string]int, len(input))
	fmt.Printf("value of root: %d\n", evaluate("root", input, memo))

	// part 2
	leftOperationRight := strings.Split(root, " ")
	if len(leftOperationRight) != 3 {
		log.Fatal("expected the form: <left-var> <operation> <right-var>")
	}

	memo2 := make(map[string]pair, len(input)-1)
	memo2["humn"] = pair{1, 0}
	left := evaluateAlgebraic(leftOperationRight[0], input, memo2)
	right := evaluateAlgebraic(leftOperationRight[2], input, memo2)

	humn := (right.b - left.b) / (left.a - right.a)
	fmt.Printf("value of humn: %f\n", humn)
}

// evaluate returns the value of the named variable
func evaluate(name string, input map[string]string, memo map[string]int) int {
	if val, ok := memo[name]; ok {
		return val
	}

	valString, ok := input[name]
	if !ok {
		log.Fatalf("did not find [%s] in input\n", name)
	}

	valInt, err := strconv.Atoi(valString)
	if err != nil {
		leftOperationRight := strings.Split(valString, " ")
		if len(leftOperationRight) != 3 {
			log.Fatal("expected valString to be of the form: <left-var> <operation> <right-var>")
		}

		leftVal := evaluate(leftOperationRight[0], input, memo)
		rightVal := evaluate(leftOperationRight[2], input, memo)

		switch leftOperationRight[1] {
		case "+":
			valInt = leftVal + rightVal
		case "-":
			valInt = leftVal - rightVal
		case "*":
			valInt = leftVal * rightVal
		case "/":
			valInt = leftVal / rightVal
		}
	}

	memo[name] = valInt
	return valInt
}

// evaluateAlgebraic returns the value of the named variable in the form:
// pair.a * VAR + pair.b
// where VAR has a value of {1, 0} in memo.
// If no such VAR exists in memo, then pair.b equals the result of evaluate().
// Restrictions:
// - VAR must be referenced only once or in such a way that VAR is never a divisor or multiplied with itself.
// - There should not be more than one key in memo initially set to {1, 0}.
func evaluateAlgebraic(name string, input map[string]string, memo map[string]pair) pair {
	if val, ok := memo[name]; ok {
		return val
	}

	valString, ok := input[name]
	if !ok {
		log.Fatalf("did not find [%s] in input\n", name)
	}

	valInt, err := strconv.Atoi(valString)
	result := pair{0, float64(valInt)}
	if err != nil {
		leftOperationRight := strings.Split(valString, " ")
		if len(leftOperationRight) != 3 {
			log.Fatal("expected the form: <left-var> <operation> <right-var>")
		}

		leftVal := evaluateAlgebraic(leftOperationRight[0], input, memo)
		rightVal := evaluateAlgebraic(leftOperationRight[2], input, memo)

		switch leftOperationRight[1] {
		case "+":
			result = pair{leftVal.a + rightVal.a, leftVal.b + rightVal.b}
		case "-":
			result = pair{leftVal.a - rightVal.a, leftVal.b - rightVal.b}
		case "*":
			if leftVal.a != 0 && rightVal.a != 0 {
				log.Fatal("algebraic multiplication not supported")
			}
			a := leftVal.a * rightVal.b
			if leftVal.a == 0 {
				a = rightVal.a * leftVal.b
			}
			result = pair{a, leftVal.b * rightVal.b}
		case "/":
			if rightVal.a != 0 {
				log.Fatal("algebraic division not supported")
			}
			result = pair{leftVal.a / rightVal.b, leftVal.b / rightVal.b}
		}
	}

	memo[name] = result
	if DEBUG {
		fmt.Printf("%s=%+v\n", name, result)
	}
	return result
}

func parseInput() map[string]string {
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	result := make(map[string]string)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		text := scanner.Text()
		varVal := strings.Split(text, ": ")
		result[varVal[0]] = varVal[1]
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}
