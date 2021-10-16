package cmd

import (
	"github.com/jsburckhardt/expense-tracker/cmd/server"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "extr",
	Short: "Expense tracker",
}

func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

func init() {
	cobra.OnInitialize()

	rootCmd.AddCommand(server.New())
}
