package main

import "fmt"

// create new type of deck
type deck []string

func newDeck() deck {
	cards := deck{}

	cardSuites := []string{"spades", "diamonds", "hearts", "club"}
	cardValues := []string{"ace", "two", "three", "four"}

	for _, suit := range cardSuites {
		for _, value := range cardValues {
			cards = append(cards, suit+" of "+value)
		}
	}

	return cards
}

func (cards deck) print() {
	for i, card := range cards {
		fmt.Println(i, card)
	}
}
