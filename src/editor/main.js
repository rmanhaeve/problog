async function loadPyodideAndProblog() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install("http://people.cs.kuleuven.be/robin.manhaeve/editor/PySDD-1.0.2-cp312-cp312-pyodide_2024_0_wasm32.whl")
        await micropip.install("http://people.cs.kuleuven.be/robin.manhaeve/editor/problog-3.0.0-py3-none-any.whl")
    `);
    return pyodide;
}

let pyodideReady = loadPyodideAndProblog();


async function runProblog() {
    let pyodide = await pyodideReady;
    let outputElement = document.getElementById("output");
    let modelInput = document.getElementById("problog-input").value;

    let result = await pyodide.runPythonAsync(`
from problog.engine import ground
from problog.program import PrologString
from problog.formula import LogicFormula, LogicDAG
from problog.cycles import break_cycles
from problog.sdd_formula import SDD, build_sdd


model = """${modelInput}"""
p = PrologString(model)
print("p", p)
formula = LogicFormula()
ground(p, formula)
print(formula)
dag = LogicDAG()
break_cycles(formula, dag)
sdd = SDD()
build_sdd(dag,sdd)
result = sdd.evaluate()
str(result)
    `);

    outputElement.textContent = "Result: " + result;
}
