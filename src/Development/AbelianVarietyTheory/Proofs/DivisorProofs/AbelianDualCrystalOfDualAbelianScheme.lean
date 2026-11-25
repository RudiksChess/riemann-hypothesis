module

public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.ExistsCrystalPairing
public import Development.AbelianVarietyTheory.Proofs.DivisorProofs.CrystallineSmoothLiftOfRelations

@[expose] public section

namespace GlobalTheory

theorem abelianDualCrystal_of_dualAbelianScheme :
    GlobalTheory.Published.DualAbelianScheme → GlobalTheory.Published.AbelianDualCrystal :=
  fun h ↦ ⟨h, GlobalTheory.SmoothLift.crystallineSmoothLift_of_relations.toCrystallineDeRham⟩

end GlobalTheory
