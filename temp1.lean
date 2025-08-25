import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Nat.Log
import Mathlib.Data.Complex.Exponential
import Mathlib.NumberTheory.Divisors
import Mathlib.Data.ZMod.Defs
import Mathlib.Data.ZMod.Basic
import Mathlib.Topology.Basic

open Real
open Nat
open Topology
theorem mathd_algebra_338
  (a b c : ℝ)
  (h₀ : 3 * a + b + c = -3)
  (h₁ : a + 3 * b + c = 9)
  (h₂ : a + b + 3 * c = 19) :
  a * b * c = -56 := by
  have h₃ := congr_arg (fun x => x - 1) h₀
  have h₄ := congr_arg (fun x => x - 1) h₁
  have h₅ := congr_arg (fun x => x - 1) h₂
  ring_nf at h₃ h₄ h₅ ⊢
  nlinarith [sq_nonneg (a - b), sq_nonneg (a - c), sq_nonneg (b - c)]
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith
  <;> linarith<｜Assistant｜><｜User｜>proof states: {'sorries': [{'proofState': 0, 'pos': {'line': 18, 'column': 21}, 'goal': 'a b c : ℝ\nh₀ : 3 * a + b + c = -3\nh₁ : a + 3 * b + c = 9\nh₂ : a + b + 3 * c = 19\n⊢ a * b * c = -56', 'endPos': {'line': 18, 'column': 26}}], 'messages': [{'severity': 'warning', 'pos': {'line': 13, 'column': 8}, 'endPos': {'line': 13, 'column': 25}, 'data': "declaration uses 'sorry'"}], 'env': 0}<｜Assistant｜><｜User｜>unexpected token '`'; expected command<｜Assistant｜>