module

public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.DenseInterior
public import Development.AbelianVarietyTheory.Definitions.Divisors.NefFibOfIsNef
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.VolHomog
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.EqOfIsometricTrivShift
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.CrysToDRBijective
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.TamagawaSpecialUnitary
public import Development.AbelianVarietyTheory.PublishedTheorems.PublishedFoundations.NonemptyAlgHomOfIsRayOfDvd
public import Development.AbelianVarietyTheory.PublishedTheorems.SemistableReduction2.SemistableReductionSt
public import Development.AbelianVarietyTheory.PublishedTheorems.TwistedTraceFormula.NotIsCompactUnivFv
public import Development.AbelianVarietyTheory.PublishedTheorems.PublishedFoundations.GreenSeriesSt
public import Development.AbelianVarietyTheory.PublishedTheorems.AutomorphicForms2.MumfordProportionality
public import Development.AbelianVarietyTheory.PublishedTheorems.AdelicLattices2.ExistsFiniteUnitaryClassesOfDualEqSmul
public import Development.AbelianVarietyTheory.PublishedTheorems.Landherr2.LandherrStIffLandherr
public import Development.AbelianVarietyTheory.PublishedTheorems.Landherr2.ExistsNormTensor
public import Development.AbelianVarietyTheory.PublishedTheorems.SemiabelianTori.GeometricallyConnectedSplitTorusAff
public import Development.AbelianVarietyTheory.PublishedTheorems.GlobalTheta.WeylDualWeylLatticesAgreeOfLowestAlcove
public import Development.AbelianVarietyTheory.PublishedTheorems.AbelianLaws.PrincipalPolarisationOneSection
public import Development.AbelianVarietyTheory.PublishedTheorems.Landherr2.DimEqZero

@[expose] public section

namespace GlobalTheory.CovTop

structure Hypotheses₂ : Prop where
  p1 : GlobalTheory.Published.ToroidalCompactification
  p4 : GlobalTheory.Published.ArCalc
  p5 : GlobalTheory.Published.AbelianDeRham
  p6 : GlobalTheory.Published.TamagawaSpecialUnitary
  p8 : GlobalTheory.Published.RayClassFieldSt
  p12 : GlobalTheory.Published.SemistableReductionSt
  p13 : GlobalTheory.Published.StrongApproxSU
  p14 : GlobalTheory.Published.GreenSeriesSt
  p16 : GlobalTheory.Published.MumfordProportionality
  p18 : GlobalTheory.Published.FinitenessOfHermitianClasses
  p19 : GlobalTheory.Published.LandherrSt
  p20 : GlobalTheory.Published.HasseNormSt
  p22 : GlobalTheory.Published.SemiAbelianHomExtension
  p23 : GlobalTheory.Published.InducedSimpleLowestAlcove
  p25 : GlobalTheory.Published.principalPolarisationOneSection
  p26 : GlobalTheory.Published.AbMulNSt

end GlobalTheory.CovTop
