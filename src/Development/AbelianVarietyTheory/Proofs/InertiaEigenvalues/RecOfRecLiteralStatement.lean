module

public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.DepthZeroCuspidalLL
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.LanglandsExhaustionGL
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.DepthZeroInduction
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.LanglandsMultisegments
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.StandardCosocleGL
public import Development.AbelianVarietyTheory.PublishedTheorems.TwistedTraceFormula.HasFiniteLengthOfIsIrreducible
public import Development.AbelianVarietyTheory.Proofs.InertiaEigenvalues.RecOfRecLiteral

@[expose] public section

open NumberField IsDedekindDomain ValuativeRel Matrix Polynomial Formalism.ConjugateSelfDual ReciprocityTheory.Gal GlobalTheory.PRep GlobalTheory.SmGL GlobalTheory.SplitWeil GlobalTheory.LocGL GlobalTheory.WeilDeligne GlobalTheory.LocLanglands GlobalTheory.Published

theorem _root_.GlobalTheory.T.rec_of_rec_literal : DepthZeroCuspidalLL → DepthZeroInduction → LanglandsExhaustionGL → LanglandsMultisegments → StandardCosocleGL → ZelevinskyPolynomialRing → GeometricLemma → BernsteinZelevinskyFiniteness → ∀ (E Ω : Type) [Field E] [NumberField E] [Field Ω] [Algebra E Ω] [IsAlgClosure E Ω] (A : ValuationSubring Ω) (w : HeightOneSpectrum (𝓞 E)) (h : IsPlaceOver A w) (rc : IrrGL (k := w.adicCompletion E) → WD h), IsRecLit h rc → IsRec h rc := by
  first | exact @GlobalTheory.LocLanglands.isRec_of_isRecLit
