import Mathlib.Algebra.Group.Defs
import Mathlib.Algebra.Group.Units.Defs
import Mathlib.Algebra.Group.MinimalAxioms

example {α : Type} [Monoid α] (a l r: α) (h₁ : l * a = 1) (h₂ : a * r = 1) : (l = r) := by
  sorry


def op {S : Type} (a : S) (b : S) : S := a

theorem op_assoc {S : Type} (a b c : S) : op a (op b c) = op (op a b) c := by
  rfl
