import os
import typing

from . import evaluator
from . import formula
from . import ddnnf_formula
from . import sdd_formula
from . import sdd_formula_explicit
from . import bdd_formula
from . import forward
#from . import kbest
# from . import core
# from . import engine
# from . import logic
# from . import cnf_formula
# from . import parser
# from . import program
# from . import cycles
# from . import util
# from . import tasks
# from . import debug


_evaluatables: typing.Dict[str, typing.Type[evaluator.Evaluatable]] = {
    "sdd": sdd_formula.SDD,
    "sddx": sdd_formula_explicit.SDDExplicit,
    "bdd": bdd_formula.BDD,
    "nnf": ddnnf_formula.DDNNF,
    "ddnnf": ddnnf_formula.DDNNF,
 #   "kbest": kbest.KBestFormula,
    "fsdd": forward.ForwardSDD,
    "fbdd": forward.ForwardBDD,
}
_semirings: typing.Dict[str, typing.Type[evaluator.Semiring]] = {
    "prob": evaluator.SemiringProbability,
    "logprob": evaluator.SemiringLogProbability,
    "symbolic": evaluator.SemiringSymbolic,
}


def get_semirings() -> typing.Collection[str]:
    """Get the set of registered semirings."""
    return _semirings.keys()


def register_semiring(name: str, cls: typing.Type[evaluator.Semiring]):
    """Register a semiring in the semiring registry."""
    assert (
        name not in _semirings
    ), "A semi-ring with the same name is already registered."
    _semirings[name] = cls


def get_semiring(name: typing.Optional[str] = None) -> typing.Type[evaluator.Semiring]:
    """Lookup a semiring."""
    if name is None:
        return _semirings["prob"]
    return _semirings.get(name, None)


def get_evaluatables() -> typing.Collection[str]:
    return _evaluatables.keys()


def get_evaluatable(
    name: typing.Optional[str] = None,
    semiring: typing.Optional[evaluator.Semiring] = None,
) -> typing.Type[evaluator.Evaluatable]:
    if name is None:
        if semiring is None or semiring.is_dsp():
            return evaluator.EvaluatableDSP
        else:
            return formula.LogicNNF
    else:
        return _evaluatables[name]


def root_path(*args):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *args))


library_paths = [root_path("problog", "library")]
