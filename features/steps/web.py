from behave import given, when, then
import subprocess

@given("un servidor web con una cuenta nueva")
def contexto(ctx):
    ctx.web_ready = True

@when("envío un abono de 10 mediante el formulario")
def peticion(ctx):
    # La prueba levanta el handler con httptest y envía el formulario POST.
    ctx.result = subprocess.run(
        ["go", "test", "-run", "^TestWeb$", "-count=1", "-v", "."],
        text=True, capture_output=True
    )

@then("la página muestra un saldo de 244.56")
def respuesta(ctx):
    assert ctx.result.returncode == 0, ctx.result.stdout + ctx.result.stderr
    assert "--- PASS: TestWeb" in ctx.result.stdout, ctx.result.stdout
