package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/gocolly/colly/v2"
)

func main() {
	// Create a new collector
	c := colly.NewCollector()

	// Create a slice to store the data
	data := [][]string{{"Category", "Subcategory"}}

	// Set up the callback for handling the category data
	c.OnHTML(".categories_item", func(e *colly.HTMLElement) {
		categoryTitle := strings.TrimSpace(e.ChildText(".categories_title"))

		// Find all subcategories within the current category
		e.ForEach(".categories_subs a", func(_ int, el *colly.HTMLElement) {
			subcategory := strings.TrimSpace(el.Text)

			// Remove commas from the category and subcategory names
			categoryTitle = strings.ReplaceAll(categoryTitle, ",", "")
			subcategory = strings.ReplaceAll(subcategory, ",", "")

			// Append the category and subcategory to the data slice
			data = append(data, []string{categoryTitle, subcategory})
		})
	})

	// Set up the callback for error handling
	c.OnError(func(r *colly.Response, err error) {
		log.Println("Request URL:", r.Request.URL, "failed with response:", r, "\nError:", err)
	})

	// Visit the target website
	err := c.Visit("https://www.sklavenitis.gr/katigories/")
	if err != nil {
		log.Fatal(err)
	}

	// Create a new CSV file
	file, err := os.Create("categories.csv")
	if err != nil {
		log.Fatal("Cannot create file", err)
	}
	defer file.Close()

	// Create a CSV writer
	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write the data to the CSV file
	err = writer.WriteAll(data)
	if err != nil {
		log.Fatal("Cannot write to file", err)
	}

	fmt.Println("Scraping completed successfully. Data saved to categories.csv")
}
