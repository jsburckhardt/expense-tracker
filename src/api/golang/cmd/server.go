package cmd

import (
	"context"
	"log"
	"time"

	"github.com/gofiber/fiber/v2"

	"github.com/spf13/cobra"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/jsburckhardt/expense-tracker/internal/entity"
)

// serverCmd represents the server command
var serverCmd = &cobra.Command{
	Use:   "server",
	Short: "Start expense-tracker api",
	Run: func(cmd *cobra.Command, args []string) {

		app := fiber.New()

		app.Get("/expenses", func(c *fiber.Ctx) error {
			data := getExpenses()
			return c.Status(fiber.StatusOK).JSON(fiber.Map{
				"data":    data,
				"success": true,
			})
		})

		app.Listen(":3000")
	},
}

func init() {
	rootCmd.AddCommand(serverCmd)
}

type Expense struct {
	Details bson.M `bson:"someNumber"`
}

func getExpenses() []entity.Expense {
	// Set client options
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")

	// Connect to MongoDB
	client, err := mongo.Connect(context.TODO(), clientOptions)

	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(context.TODO(), nil)

	if err != nil {
		log.Fatal(err)
	}

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
