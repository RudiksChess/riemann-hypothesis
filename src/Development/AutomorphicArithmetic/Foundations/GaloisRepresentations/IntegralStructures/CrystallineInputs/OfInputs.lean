module

public import Development.AbelianVarietyTheory.PublishedTheorems.AutomorphicForms2.DeRhamPotSemistable
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.IrreducibleAdmissibleGL
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.StandardFunctorsFiniteLength
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.HeckeLAdicCharacterAboveIff
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.IsComplementaryProductOfIsCuspidal
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.LanglandsExhaustionGL
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisGeometry2.AlgebraicCharacterWD
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisGeometry2.ArthurClozelStrongTC
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisGeometry2.GelfandKazhdanDual

@[expose] public section

namespace UpperTheory.Gal.Int.Inp

structure Inp : Prop where
  js : GlobalTheory.Published.JacquetShalikaRigidity
  gk : GlobalTheory.Published.GelfandKazhdanDual
  adm : GlobalTheory.Published.IrreducibleAdmissibleGL
  len : GlobalTheory.Published.StandardFunctorsFiniteLength
  exh : GlobalTheory.Published.LanglandsExhaustionGL
  zel : GlobalTheory.Published.ZelevinskyPolynomialRing
  gen : GlobalTheory.Published.GenericUnitaryDualGL
  ac : GlobalTheory.Published.ArthurClozelStrongTC
  hk : GlobalTheory.Published.HeckeLAdicCharacterAbove
  alg : GlobalTheory.Published.AlgebraicCharacterWD
  pst : GlobalTheory.Published.DeRhamPotSemistable

end UpperTheory.Gal.Int.Inp
