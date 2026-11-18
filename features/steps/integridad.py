from behave import given, when, then
import json, pathlib, subprocess, tempfile

@given("un archivo de cuenta nuevo")
def nuevo(c):
    c.tmp = tempfile.TemporaryDirectory()
    c.dir = pathlib.Path(c.tmp.name)
    c.bin = c.dir / "cajero"
    subprocess.run(["go","build","-o",str(c.bin),"."],check=True)
@when("retiro 200 dos veces e ingreso un abono negativo")
def operar(c):
    subprocess.run([str(c.bin),"-cli"],cwd=c.dir,input="retiro\n200\nretiro\n200\nabono\n-1\nsalir\n",text=True,check=True)
@then("el archivo registra éxito, fallo y error y conserva 34.56 soles")
def comprobar(c):
    data=json.loads((c.dir/"cuenta.json").read_text())
    assert data["Balance"]==3456
    assert [r["Status"] for r in data["History"]]==["éxito","fallo","error"]
    result=subprocess.run([str(c.bin),"-cli"],cwd=c.dir,input="salir\n",text=True,capture_output=True,check=True)
    assert "34.56" in result.stdout
    c.tmp.cleanup()
