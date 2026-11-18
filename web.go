package main

import (
	_ "embed"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"strconv"
)

//go:embed index.html
var markup string
var page = template.Must(template.New("cuenta").Funcs(template.FuncMap{"soles": soles}).Parse(markup))

func routes(store *Store) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		if r.Method != "GET" {
			http.Error(w, "Método inválido", 405)
			return
		}
		st, err := store.view()
		if err != nil {
			http.Error(w, "No se pudo leer la cuenta.", 500)
			return
		}
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		if err := page.Execute(w, st); err != nil {
			log.Print(err)
		}
	})
	mux.HandleFunc("/movimiento", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "Use POST", 405)
			return
		}
		r.Body = http.MaxBytesReader(w, r.Body, 4096)
		if err := r.ParseForm(); err != nil {
			http.Error(w, "Formulario inválido", 400)
			return
		}
		_, err := store.move(r.PostForm.Get("operacion"), r.PostForm.Get("monto"))
		if err != nil {
			http.Error(w, "No se guardó el movimiento.", 500)
			return
		}
		http.Redirect(w, r, "/", http.StatusSeeOther)
	})
	return mux
}
func main() {
	if len(os.Args) > 1 {
		if os.Args[1] == "-cli" {
			os.Args = os.Args[:1]
		}
		cli()
		return
	}
	s := Store{path: "cuenta.json"}
	port := 8080
	fmt.Println("Abra http://localhost:8080")
	log.Fatal(http.ListenAndServe("127.0.0.1:"+strconv.Itoa(port), routes(&s)))
}
