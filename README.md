# prj_withdrawal · Cajero web en Go

[![CI](https://github.com/Gabriel-XDDDD/prj_withdrawal/actions/workflows/tests.yml/badge.svg)](https://github.com/Gabriel-XDDDD/prj_withdrawal/actions/workflows/tests.yml)
[![Go](https://img.shields.io/badge/Go-1.20%2B-00ADD8?logo=go&logoColor=white)](https://go.dev/)
[![BDD](https://img.shields.io/badge/BDD-Gherkin-23D96C)](features/)

Proyecto académico de **DSL / Gherkin-BDD** para la Universidad Nacional de Ingeniería. La aplicación permite retirar y abonar efectivo desde una interfaz web, conserva el saldo y registra cada intento en un historial JSON verificable.

**Repositorio:** <https://github.com/Gabriel-XDDDD/prj_withdrawal>  
**Informe:** [Informe de la entrega 3](docs/Informe_Entrega_3_actualizado.pdf)

## Funcionalidades

- Retiro en múltiplos de S/ 10.
- Abono positivo con hasta dos decimales.
- Rechazo por fondos insuficientes sin modificar el saldo.
- Registro de operaciones exitosas, fallidas y erróneas.
- Persistencia atómica en `cuenta.json` mediante archivo temporal y renombrado.
- Validación del saldo, identificadores, eventos y cronología UTC al reabrir.
- Interfaz web local y consola alternativa.
- Pruebas unitarias, concurrentes, HTTP y escenarios Gherkin.
- Integración continua con GitHub Actions.

## Evolución del proyecto

| Entrega | Incremento |
|---|---|
| 1 | Retiro y abono desde consola |
| 2 | Persistencia e integridad del saldo e historial JSON |
| 3 | Refactorización a aplicación web y automatización CI |

## Arquitectura

```mermaid
flowchart LR
    U[Usuario] -->|Formulario| W[Handler HTTP]
    C[Consola] --> A[Reglas de cuenta]
    W --> S[Store]
    S --> A
    S -->|Escritura atómica| J[(cuenta.json)]
    J -->|Reapertura y validación| S
```

```text
prj_withdrawal/
├── account.go            reglas de retiro, abono y conversión a céntimos
├── store.go              persistencia e integridad del historial JSON
├── web.go                rutas GET / y POST /movimiento
├── index.html            formulario e historial web
├── main.go               servidor web y consola alternativa
├── *_test.go             pruebas de negocio, almacenamiento y HTTP
├── features/             escenarios Gherkin y pasos Behave
├── cuenta.json           estado inicial de demostración
└── .github/workflows/    integración continua
```

## Ejecución local

Funciona en **Windows, macOS y Linux**. Requiere [Go 1.20 o
posterior](https://go.dev/dl/) y Git. Python 3 es opcional y solo se necesita
para ejecutar los escenarios Gherkin.

Los siguientes comandos son iguales en Terminal, Bash, Zsh y PowerShell:

```sh
git clone https://github.com/Gabriel-XDDDD/prj_withdrawal.git
cd prj_withdrawal
go run .
```

Abra <http://localhost:8080>. Para detener el servidor use `Ctrl+C`.

Consola alternativa:

```sh
go run . -cli
```

Prueba aislada sin modificar `cuenta.json`:

```sh
go run . -nombre Alice -saldo 234.56 -retiro 200 -test exito
```

## Pruebas

Pruebas disponibles en todos los sistemas:

```sh
go test -count=1 -v ./...
go vet ./...
```

La detección de condiciones de carrera requiere una plataforma y un compilador
C compatibles con el detector de Go:

```sh
go test -race -count=1 ./...
```

Escenarios Gherkin:

### macOS y Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install behave==1.3.3
python -m behave
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install behave==1.3.3
python -m behave
```

Si PowerShell impide activar el entorno, puede ejecutar los comandos sin
activarlo:

```powershell
.\.venv\Scripts\python.exe -m pip install behave==1.3.3
.\.venv\Scripts\python.exe -m behave
```

La suite comprueba retiros, abonos, importes inválidos, fondos insuficientes, concurrencia, corrupción del JSON, fechas UTC, recuperación del saldo y formularios HTTP.

## Demostración esperada

Partiendo de S/ 234.56:

1. Retirar S/ 200.00 produce un saldo de S/ 34.56.
2. Abonar S/ 20.50 produce un saldo de S/ 55.06.
3. Abonar S/ 0 registra un error y conserva S/ 55.06.
4. Reiniciar el servidor recupera el saldo y el historial.

## Consideraciones

- Los valores monetarios se guardan en céntimos enteros.
- Use una sola instancia del programa por archivo `cuenta.json`.
- `cuenta.json` contiene el estado inicial. Para reiniciar la demostración, restaure su contenido desde Git.
- Es una aplicación académica local de una sola cuenta; no incorpora autenticación de clientes ni despliegue bancario real.

## Autor

Gabriel Eustaquio · Ingeniería de Software · UNI FIIS
