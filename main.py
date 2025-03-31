import os
import json

IN_BUFF = 'temp.lean'
OUT_BUFF = 'temp.json'

def split_by_pos(text: str, pos1: tuple, pos2: tuple) -> tuple:

    def pos_to_index(text, pos):
        line, col = pos
        lines = text.splitlines(keepends=True)
        if line < 1 or line > len(lines):
            raise ValueError(f"Line number {line} out of range (1-{len(lines)}).")
        index = sum(len(l) for l in lines[:line-1]) + (col)
        if index < 0 or index > len(text):
            raise ValueError(f"Column number {col} out of range in line {line}.")
        return index

    idx1 = pos_to_index(text, pos1)
    idx2 = pos_to_index(text, pos2)

    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    return text[:idx1], text[idx1:idx2], text[idx2:]

class LeanError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def check_resp(resp : dict) -> None:
    for m in resp["messages"]:
        if m["severity"] == "error":
            raise LeanError(m["data"])

def run_code(code: str) -> dict:
    with open(IN_BUFF, 'w') as f:
        f.write(code)

    query1 = json.dumps({"path": IN_BUFF, "allTactics": True})
    os.system(f"""echo '{query1}' | lake env .lake/build/bin/repl > {OUT_BUFF}""")
    # os.system(f"""echo '{query1}' | lake exe repl > {OUT_BUFF}""")
    resp = {}

    with open(OUT_BUFF,'r') as f:
        resp = json.loads(f.read())

    check_resp(resp)
    return resp

def fill_and_run(code : str, pos : int, subst : str) -> str:
    resp = run_code(code)

    if "sorries" not in resp or len(resp["sorries"]) == 0:
      return code

    pos1 = (resp["sorries"][pos]["pos"]["line"], resp["sorries"][pos]["pos"]["column"])
    pos2 = (resp["sorries"][pos]["endPos"]["line"], resp["sorries"][pos]["endPos"]["column"])
    c1, _, c2 = split_by_pos(code, pos1, pos2)
    newcode = c1 + subst + c2
    # print(newcode)
    newresp = run_code(newcode)
    return newcode

s = '''import Mathlib.Algebra.BigOperators.Group.Finset.Defs

def F (n: Nat) :=
  match n with
  | 0 => 1
  | 1 => 1
  | Nat.succ (Nat.succ m) => (F m) + (F (Nat.succ m))

def prob3' (n : ℕ) : ∑ (x ∈ (Finset.range (n+1))), (F x) * (F x)= (F n) * (F (n + 1)) := by
  induction n with
  | zero => sorry
  | succ n ih =>
    have h1: ∑ (x ∈ (Finset.range (n+1+1))), (F x) * (F x) = (F n) * (F (n+1)) + (F (n+1)) * (F (n+1)) := by sorry
    have h2: (F n) * (F (n+1)) + (F (n+1)) * (F (n+1)) = (F (n + 1)) * (F (n) + F (n+1)) := by sorry
    have h3: (F (n + 1)) * (F (n) + F (n+1)) = (F (n + 1)) * (F (n+2)) := by sorry
    sorry
'''

print(fill_and_run(s, 0, 'rfl'))
