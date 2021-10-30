package endpoint

import (
	"context"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/jsburckhardt/expense-tracker/internal/expense"
)

func Expenses(c *fiber.Ctx) error {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	data, _ := expense.NewService().List(ctx)
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"data":    data,
		"success": true,
	})
}
