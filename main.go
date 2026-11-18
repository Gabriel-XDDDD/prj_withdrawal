package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func cli() {
	if scenario() {
		return
	}
	store := Store{path: "cuenta.json"}
	sc := bufio.NewScanner(os.Stdin)
	for {
		st, err := store.view()
		if err != nil {
			fmt.Println(err)
			return
		}
		fmt.Printf("\nSaldo S/ %s | retiro / abono / salir\n> ", soles(st.Balance))
		if !sc.Scan() {
			return
		}
		op := strings.ToLower(strings.TrimSpace(sc.Text()))
		if op == "salir" {
			return
		}
		if op != "retiro" && op != "abono" {
			fmt.Println("Elija una opción del menú.")
			continue
		}
		fmt.Print("Monto en soles: ")
		if !sc.Scan() {
			return
		}
		e, err := store.move(op, sc.Text())
		if err != nil {
			fmt.Println("Error al guardar:", err)
			continue
		}
		fmt.Println(e.Message)
	}
}
