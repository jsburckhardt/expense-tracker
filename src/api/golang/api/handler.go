package api

import (
	// _ "extr/docs" // This line is necessary for go-swagger to find docs // TODO: not yet implemented

	"github.com/gofiber/fiber/v2"
	"github.com/jsburckhardt/expense-tracker/api/endpoint/expense"
)

// API constructs fiber.App with all application routes defined.
// @title EXTR Service API
// @description Endpoints in the EXTR service
// @version 1.0
func New() *fiber.App {

	app := fiber.New()

	app.Get("/expenses", expense.List)
	app.Get("/expenses/:id", expense.Get)
	app.Post("/expenses", expense.Create)

	return app
}
