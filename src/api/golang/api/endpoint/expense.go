package endpoint

import (
	"context"
	"log"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/jsburckhardt/expense-tracker/internal/db"
	"github.com/jsburckhardt/expense-tracker/internal/entity"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func Expenses(c *fiber.Ctx) error {
	data := getExpenses()
	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"data":    data,
		"success": true,
	})
}

func getExpenses() []entity.Expense {

	client := db.Connect()

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)

	expensesDb := client.Database("expensedb")
	expensesCollection := expensesDb.Collection("expenses")

	options := options.Find()
	options.SetLimit(10)
	filterCursor, err := expensesCollection.Find(ctx, bson.M{"Category": "Gift"}, options)
	if err != nil {
		log.Fatal(err)
	}
	var expensesFiltered []entity.Expense
	if err = filterCursor.All(ctx, &expensesFiltered); err != nil {
		log.Fatal(err)
	}

	return expensesFiltered
}
