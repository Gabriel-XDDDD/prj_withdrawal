from behave import given, when, then
import subprocess
@given('que {nombre} tiene {saldo} soles')
def cuenta(ctx,nombre,saldo):
    ctx.nombre,ctx.saldo=nombre,saldo
@when('solicita un {op} de {monto}')
def mover(ctx,op,monto):
    r=subprocess.run(["go","run",".","-nombre",ctx.nombre,"-saldo",ctx.saldo,"-"+op,monto],capture_output=True,text=True,check=True)
    ctx.resultado=r.stdout.strip().split(" | ")
@then('obtiene {estado} y un saldo de {saldo} soles')
def verificar(ctx,estado,saldo):
    assert ctx.resultado[1:3]==[estado,saldo],ctx.resultado
