package cmd

import (
	"encoding/json"
	"fmt"
	"net"
	"os"

	"github.com/spf13/cobra"
)

type Problem struct {
	ProblemName  string `json:"name"`
	QuantityData int64  `json:"quantity_data"`
	LowLimit     int64  `json:"low_limit"`
	MaxLimit     int64  `json:"max_limit"`
	OutputFile   string `json:"output_file"`
}

var ProblemName string
var QuantityData int64
var LowLimit int64
var MaxLimit int64
var OutputFile string

var rootCmd = &cobra.Command{
	Use:   "client",
	Short: "A brief description of your application",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		conn, err := net.Dial("tcp", "localhost:65432")
		if err != nil {
			fmt.Println("Error connecting to server", err)
			return err
		}
		defer conn.Close()

		problem := Problem{
			ProblemName:  ProblemName,
			QuantityData: QuantityData,
			LowLimit:     LowLimit,
			MaxLimit:     MaxLimit,
			OutputFile:   OutputFile,
		}

		msgJson, err := json.Marshal(problem)
		if err != nil {
			fmt.Println("Error encoding JSON:", err)
			return err
		}

		_, err = conn.Write(msgJson)
		if err != nil {
			fmt.Println("Error sending data: ", err)
			return err
		}

		buffer := make([]byte, 1024)
		n, err := conn.Read(buffer)
		if err != nil {
			fmt.Println("Error reading response:", err)
			return err
		}

		response := string(buffer[:n])
		fmt.Println("Server response:", response)

		if OutputFile != "" {
			err = os.WriteFile(OutputFile, []byte(response), 0644)
			if err != nil {
				fmt.Println("Error writing to file:", err)
				return err
			}
			fmt.Println("Response saved to", OutputFile)
		}

		return nil
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().StringVarP(&ProblemName, "problem", "p", "", "Problem to be resolved")
	rootCmd.Flags().Int64VarP(&QuantityData, "quantity", "a", 10, "Amount of numbers")
	rootCmd.Flags().Int64VarP(&LowLimit, "min", "x", 10, "Minimum number")
	rootCmd.Flags().Int64VarP(&MaxLimit, "max", "y", 10, "Maximum number")
	rootCmd.Flags().StringVarP(&OutputFile, "output", "o", "", "Output file")

}
