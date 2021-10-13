package server

import (
	"fmt"
	"log"
	"os"
	"os/signal"

	"github.com/spf13/cobra"

	"github.com/jsburckhardt/expense-tracker/api"
)

var (
	port int

	serverCmd = &cobra.Command{
		Use:   "server",
		Short: "Start expense-tracker api",
		Run: func(cmd *cobra.Command, args []string) {
			app := api.New()

			c := make(chan os.Signal, 1)
			signal.Notify(c, os.Interrupt)
			go func() {
				<-c
				fmt.Println("Gracefully shutting down...")
				app.Shutdown()
			}()

			fmt.Printf("starting server on the port %d", port)
			if err := app.Listen(fmt.Sprintf(":%d", port)); err != nil {
				log.Panic(err)
			}

			fmt.Println("Running cleanup tasks...")
			// Any cleanup tasks go here
		},
	}
)

// New initialises 'server' command
func New() *cobra.Command {
	serverCmd.Flags().IntVarP(&port, "port", "p", 3000, "port to accept incoming http requests")

	return serverCmd
}
