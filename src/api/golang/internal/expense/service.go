package expense

import (
	"context"
	"fmt"
	"time"

	"github.com/jsburckhardt/expense-tracker/internal/db"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Expense struct {
	Index       int64     `json:"index"`
	Date        time.Time `json:"date"`
	CreatedAt   time.Time `json:"created_at                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    "`
	UpdatedAt   time.Time `json:"updated_at"`
	Store       string    `json:"store"`
	Category    string    `json:"category"`
	Amount      float64   `json:"amount"`
	ExcludeWE   string    `json:"excludeWE"`
	Description string    `json:"description"`
}

type Service interface {
	List(ctx context.Context) ([]Expense, error)
	// Get(ctx context.Context, id string) (Album, error)
	// Query(ctx context.Context, offset, limit int) ([]Album, error)
	// Count(ctx context.Context) (int, error)
	// Create(ctx context.Context, input CreateAlbumRequest) (Album, error)
	// Update(ctx context.Context, id string, input UpdateAlbumRequest) (Album, error)
	// Delete(ctx context.Context, id string) (Album, error)
}

type service struct {
	repo *mongo.Collection
	// logger log.Logger
}

// NewService creates a new album service.
func NewService() Service {
	fmt.Println("NewService called")
	client := db.Connect()
	repo := client.Database("expensedb").Collection("expenses")

	fmt.Println("returning service")
	return service{repo}
}

func (s service) List(ctx context.Context) ([]Expense, error) {
	fmt.Print("List called")
	options := options.Find()
	options.SetLimit(10)

	filterCursor, err := s.repo.Find(ctx, bson.M{"Category": "Gift"}, options)
	if err != nil {
		return nil, err
	}

	var expensesFiltered []Expense
	if err = filterCursor.All(ctx, &expensesFiltered); err != nil {
		return nil, err
	}

	return expensesFiltered, nil
}
