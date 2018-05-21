package main

import "fmt"

func main() {
	cards := []string{"ace of diamonds", newCard()}
	cards = append(cards, "six of spades")
	for i, card := range cards {
		fmt.Println(i, card)
	}
}

func newCard() string {
	return "five of diamonds"
}
