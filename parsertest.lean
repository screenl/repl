import Lean.Parser.Extension
import Lean.Parser.Module
import Lean.Environment
import Lean.Elab.Import
import Lean.Elab.Command
import Lean.Parser.Types
set_option linter.unusedVariables false

section

open Lean

def getHeader (input : String) (fileName : Option String := none) :=  do
  let fileName   := fileName.getD "<input>"
  let inputCtx   := Parser.mkInputContext input fileName
  let (header, parserState, messages) ← Parser.parseHeader inputCtx
  pure header

def commandToAST (head input : String) (fileName : Option String := none) :=  do
  let fileName   := fileName.getD "<input>"
  let inputCtx   := Parser.mkInputContext input fileName
  let (header, parserState, messages) ← Parser.parseHeader inputCtx
  let header <- getHeader head
  let (env, messages) ← Elab.processHeader header {} messages inputCtx
  let cmdState := Elab.Command.mkState env messages {}
  let scope := cmdState.scopes.head!
  let pmctx : Parser.ParserModuleContext := { env := cmdState.env, options := {}, currNamespace := scope.currNamespace, openDecls := scope.openDecls }
  let (s, ps, msg) := Parser.parseCommand inputCtx pmctx parserState Lean.MessageLog.empty
  pure s
end

def testh : String := "
import Mathlib.Tactic.Linarith.Frontend
import Mathlib.Data.Real.Basic"

def test : String := "theorem lean_workbook_plus_11860 (a b c : ℝ) : (b^2 + c^2 - a^2) * (b - c) ^ 2 + (c^2 + a^2 - b^2) * (c - a) ^ 2 + (a^2 + b^2 - c^2) * (a - b) ^ 2 ≥ 0   :=  by
  simp only [sub_eq_add_neg, add_assoc, add_left_neg, add_zero]
  nlinarith [sq_nonneg (a + b + c), sq_nonneg (a + b - c), sq_nonneg (a - b + c), sq_nonneg (a - b - c)]"

def main : IO Unit := do
  /- let res <- commandToAST test -/
  let res <- commandToAST testh test
  IO.println res
