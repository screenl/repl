import Mathlib.Algebra.BigOperators.Group.Finset.Defs

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
