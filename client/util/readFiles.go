package utils

import (
	"bufio"
	"fmt"
	"os"
)

// ReadAuthKey reads the authentication key from a file
func ReadAuthKey(filename string) (string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return "", err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	if scanner.Scan() {
		return scanner.Text(), nil
	}
	if err := scanner.Err(); err != nil {
		return "", err
	}
	return "", fmt.Errorf("file is empty")
}
