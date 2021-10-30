package expense

import (
	"context"
	"fmt"

	"github.com/jsburckhardt/expense-tracker/internal/db"
	"github.com/jsburckhardt/expense-tracker/internal/entity"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Service interface {
	List(ctx context.Context) ([]entity.Expense, error)
	Get(ctx context.Context, index int64) (*entity.Expense, error)
	// Query(ctx context.Context, offset, limit int) ([]Album, error)
	// Count(ctx context.Context) (int, error)
	Create(ctx context.Context, input *entity.Expense) (*entity.Expense, error)
	// Update(ctx context.Context, id string, input UpdateAlbumRequest) (Album, error)
	// Delete(ctx context.Context, id string) (Album, error)
}

type service struct {
	repo *mongo.Collection
	// logger log.Logger
}

// NewService creates a new album service.
func NewService() Service {
	client := db.Connect()
	repo := client.Database("expensedb").Collection("expenses")
	return service{repo}
}

func (s service) List(ctx context.Context) ([]entity.Expense, error) {
	options := options.Find()
	options.SetLimit(10)

	filterCursor, err := s.repo.Find(ctx, bson.M{"Category": "Gift"}, options)
	if err != nil {
		return nil, err
	}

	var expenses []entity.Expense
	if err = filterCursor.All(ctx, &expenses); err != nil {
		return nil, err
	}

	return expenses, nil
}

func (s service) Get(ctx context.Context, index int64) (*entity.Expense, error) {
	options := options.Find()
	options.SetLimit(10)

	filterCursor, err := s.repo.Find(ctx, bson.M{"Index": index}, options)
	if err != nil {
		return nil, err
	}

	var expenses []entity.Expense
	if err = filterCursor.All(ctx, &expenses); err != nil {
		return nil, err
	}

	if len(expenses) == 0 {
		return nil, nil
	}

	if len(expenses) > 1 {
		return nil, fmt.Errorf("Multiple items with the same index")
	}

	return &(expenses[0]), nil
}

func (s service) Create(ctx context.Context, input *entity.Expense) (*entity.Expense, error) {
	_, err := s.repo.InsertOne(ctx, input)
	if err != nil {
		return nil, err
	}

	return input, nil
}
