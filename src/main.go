package main

import (
	"encoding/json"
	"fmt"

	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	// app.Get("/", func(c *fiber.Ctx) error {
	// 	return c.SendString("Hello, World!")
	// })

	// GET http://localhost:8080/hello%20world

	app.Get("/api/v1/:value", func(c *fiber.Ctx) error {
		return c.SendString("value: " + c.Params("value"))
		// => Get request with value: hello world
	})

	// GET http://localhost:3000/john
	app.Get("/api/v2/:name?", func(c *fiber.Ctx) error {
		if c.Params("name") != "" {
			return c.SendString("Hello " + c.Params("name"))
			// => Hello john
		}
		return c.SendString("Where is john?")
	})

	// GET http://localhost:3000/api/user/john
	app.Get("/api/v3/*", func(c *fiber.Ctx) error {
		return c.SendString("API path: " + c.Params("*"))
		// => API path: user/john
	})

	data, _ := json.MarshalIndent(app.Stack(), "", "  ")
	fmt.Println(string(data))

	app.Static("/", "./public")

	app.Listen(":3000")

}
