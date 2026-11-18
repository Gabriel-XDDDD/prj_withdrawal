package main

import (
	"net/http"
	"net/http/httptest"
	"net/url"
	"path/filepath"
	"strings"
	"testing"
)

func postMovement(t *testing.T, h http.Handler, operation, amount string) {
	t.Helper()
	form := url.Values{"operacion": {operation}, "monto": {amount}}
	r := httptest.NewRequest(http.MethodPost, "/movimiento", strings.NewReader(form.Encode()))
	r.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	w := httptest.NewRecorder()
	h.ServeHTTP(w, r)
	if w.Code != http.StatusSeeOther {
		t.Fatalf("POST %s %s: estado %d", operation, amount, w.Code)
	}
}

func getPage(t *testing.T, h http.Handler) string {
	t.Helper()
	w := httptest.NewRecorder()
	h.ServeHTTP(w, httptest.NewRequest(http.MethodGet, "/", nil))
	if w.Code != http.StatusOK {
		t.Fatalf("GET /: estado %d", w.Code)
	}
	return w.Body.String()
}

func TestWeb(t *testing.T) {
	h := routes(&Store{path: filepath.Join(t.TempDir(), "cuenta.json")})

	postMovement(t, h, "retiro", "200")
	postMovement(t, h, "abono", "20.50")
	postMovement(t, h, "abono", "0")
	postMovement(t, h, "retiro", "200")

	body := getPage(t, h)
	for _, want := range []string{
		"S/ 55.06",
		"Retiro realizado.",
		"Abono realizado.",
		"Ingrese un monto positivo con hasta dos decimales.",
		"Saldo insuficiente. Intente con un monto menor.",
	} {
		if !strings.Contains(body, want) {
			t.Fatalf("la página no contiene %q", want)
		}
	}
}
