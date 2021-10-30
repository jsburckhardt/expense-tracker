package expense

import (
	"context"
	"strconv"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/jsburckhardt/expense-tracker/internal/entity"
	"github.com/jsburckhardt/expense-tracker/internal/expense"
)

func Get(c *fiber.Ctx) error {
	param := c.Params("id")
	index, _ := strconv.ParseInt(param, 10, 64)

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	data, _ := expense.NewService().Get(ctx, index)
	if data == nil {
		c.Status(fiber.StatusNotFound)
	} else {
		c.Status(fiber.StatusOK).JSON(fiber.Map{
			"data":    data,
			"success": true,
		})
	}
	return nil
}

func List(c *fiber.Ctx) error {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	data, _ := expense.NewService().List(ctx)
	c.Status(fiber.StatusOK).JSON(fiber.Map{
		"data":    data,
		"success": true,
	})
	return nil
}

func Create(c *fiber.Ctx) error {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

	input := new(entity.Expense)
	if err := c.BodyParser(input); err != nil {
		c.Status(fiber.StatusServiceUnavailable).SendString(err.Error())
		return err
	}
	new, err := expense.NewService().Create(ctx, input)
	if err != nil {
		c.Status(fiber.StatusBadRequest).SendString(err.Error())
		return err
	}

	c.JSON(new)
	return nil
}
