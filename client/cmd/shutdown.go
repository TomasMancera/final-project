package cmd

import (
	utils "client/util"
	"encoding/json"
	"fmt"
	"net"

	"github.com/spf13/cobra"
)

type ShutdownRequest struct {
	Shutdown bool   `json:"shutdown"`
	AuthKey  string `json:"auth_key"`
}

var authKey string

var shutdownCmd = &cobra.Command{
	Use:   "shutdown",
	Short: "Shutdown the system",
	Long:  `Shutdown the system using a provided authentication key.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		// Leer la clave de autenticación desde el archivo password.txt

		fileAuthKey, err := utils.ReadAuthKey("./files/password.txt")
		if err != nil {
			fmt.Println("Error reading authentication key from file:", err)
			return err
		}

		// Comparar la clave proporcionada con la clave del archivo
		if !utils.CheckPasswordHash(authKey, fileAuthKey) {
			fmt.Println("Error: Authentication failed")
			return fmt.Errorf("authentication failed")
		}

		conn, err := net.Dial("tcp", "localhost:65432")
		if err != nil {
			fmt.Println("Error connecting to server:", err)
			return err
		}
		defer conn.Close()

		shutdownRequest := ShutdownRequest{
			Shutdown: true,
			AuthKey:  authKey,
		}

		msgJson, err := json.Marshal(shutdownRequest)
		if err != nil {
			fmt.Println("Error encoding JSON:", err)
			return err
		}

		_, err = conn.Write(msgJson)
		if err != nil {
			fmt.Println("Error sending data:", err)
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

		return nil
	},
}

func init() {
	rootCmd.AddCommand(shutdownCmd)
	shutdownCmd.Flags().StringVarP(&authKey, "auth-key", "k", "", "Authentication key for shutdown")
	shutdownCmd.MarkFlagRequired("auth-key")
}
