package entity

import "time"

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
