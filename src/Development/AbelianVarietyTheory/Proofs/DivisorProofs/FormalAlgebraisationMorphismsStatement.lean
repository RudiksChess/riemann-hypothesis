module

public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.FormalAlgebraisation
public import Development.AbelianVarietyTheory.Proofs.DivisorProofs.FormalAlgebraisationMorphisms

@[expose] public section


theorem _root_.GlobalTheory.T.formalAlgebraisation_morphisms' : GlobalTheory.Published.FormalAlgebraisation.Morphisms := by
  first | exact @GlobalTheory.FormalAlgMorphisms.formalAlgebraisation_morphisms
