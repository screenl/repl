import Mathlib.Algebra.Algebra.Basic
import Mathlib.Algebra.Order.Floor
import Mathlib.Algebra.Associated
import Mathlib.Algebra.BigOperators.Basic

import Mathlib.Algebra.BigOperators.Pi
import Mathlib.Algebra.GeomSum
import Mathlib.Algebra.Group.Pi.Basic
import Mathlib.Algebra.Group.Pi.Lemmas
import Mathlib.Algebra.Group.Commute.Basic
import Mathlib.Algebra.Group.Commute.Defs
import Mathlib.Algebra.Group.Commute.Hom
import Mathlib.Algebra.Group.Commute.Units
import Mathlib.Algebra.GroupPower.Basic
import Mathlib.Algebra.GroupPower.Identities
import Mathlib.Algebra.Order.Floor
import Mathlib.Algebra.QuadraticDiscriminant
import Mathlib.Algebra.Ring.Basic
import Mathlib.Analysis.MeanInequalitiesPow
import Mathlib.Analysis.Asymptotics.AsymptoticEquivalent
import Mathlib.Analysis.NormedSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Base
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Complex.Exponential
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Card

import Mathlib.Data.Int.GCD
import Mathlib.Data.Int.ModEq
import Mathlib.Data.Int.Parity
import Mathlib.Data.List.Intervals
import Mathlib.Data.List.Palindrome
import Mathlib.Data.Multiset.Basic

import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Nat.Digits
import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Data.Nat.Fib.Zeckendorf
import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Nat.Multiplicity
import Mathlib.Data.Nat.Parity
import Mathlib.Data.Nat.Prime
import Mathlib.Data.PNat.Basic
import Mathlib.Data.PNat.Prime

import Mathlib.Data.Rat.BigOperators
import Mathlib.Data.Rat.Cast.CharZero
import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Data.Rat.Cast.Lemmas
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Denumerable
import Mathlib.Data.Rat.Encodable
import Mathlib.Data.Rat.Field
import Mathlib.Data.Rat.Floor
import Mathlib.Data.Rat.Init
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Rat.Order
import Mathlib.Data.Rat.Sqrt

import Mathlib.Data.Rat.Star
import Mathlib.Data.Real.Basic
import Mathlib.Data.ENNReal.Basic
import Mathlib.Data.ENNReal.Inv
import Mathlib.Data.ENNReal.Operations
import Mathlib.Data.ENNReal.Real
import Mathlib.Data.Real.ENatENNReal
import Mathlib.Data.Real.Irrational
import Mathlib.Data.Real.NNReal
import Mathlib.Data.Real.Sqrt

import Mathlib.Data.Set.Finite
import Mathlib.Data.Sym.Sym2
import Mathlib.Data.ZMod.Basic
import Mathlib.Dynamics.FixedPoints.Basic

import Mathlib.LinearAlgebra.AffineSpace.AffineMap
import Mathlib.LinearAlgebra.AffineSpace.Independent
import Mathlib.LinearAlgebra.AffineSpace.Ordered
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.Logic.Equiv.Basic

import Mathlib.Order.Filter.Basic

import Mathlib.Order.WellFounded
import Mathlib.Topology.Basic
import Mathlib.Topology.Instances.NNReal

import Mathlib.Data.ZMod.Basic
import Mathlib.RingTheory.Int.Basic


import Aesop
open BigOperators

open Nat

open Real

open Rat

theorem lean_workbook_plus_65375 (a b c : ℝ) (habc : a + b + c = 2 * π) : 1 - cos a ^ 2 - cos b ^ 2 - cos c ^ 2 + 2 * cos a * cos b * cos c = 0   :=  by 
  have : c = 2 * π - (a + b) := by linarith
  simp [this, cos_sub, cos_add, cos_two_mul, sin_two_mul]
  nlinarith [cos_sq_add_sin_sq a, cos_sq_add_sin_sq b]


