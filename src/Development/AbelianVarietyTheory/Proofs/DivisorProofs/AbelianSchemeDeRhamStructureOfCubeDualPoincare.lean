module

public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.ExistsCrystalPairing
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.PoincareDeRhamDuality
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.CubeTheorem
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.AbelianHodgeDeRham
public import Development.AbelianVarietyTheory.Proofs.DivisorProofs.AbelianDeRhamPoincareDualityOfCubeDual
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.AbelianDeRhamStructure
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.BijectiveCechDeRhamComparisonDegreeOne
public import Development.AbelianVarietyTheory.Proofs.DivisorProofs.CrystallineDeRhamAbelianStructureOfStatements
public import Development.AbelianVarietyTheory.Proofs.DivisorProofs.CrystallineSmoothLiftOfRelations
public import Development.AbelianVarietyTheory.Proofs.DivisorProofs.RigidOfFreeOfCrystallineDeRham
import Development.AbelianVarietyTheory.Proofs.DivisorProofs.PullOverOneEqZero

@[expose] public section

namespace GlobalTheory

theorem abelianDeRham_of_hodge_cube_dual_poincare :
    GlobalTheory.Published.AbelianHodgeDeRham → GlobalTheory.Published.CubeTheorem → GlobalTheory.Published.DualAbelianScheme →
      GlobalTheory.Published.PoincareDeRhamDuality → GlobalTheory.Published.AbelianDeRham :=
  by
    intro hH hC hD hP
    obtain ⟨⟨hfree, hhodge, hbc⟩, hcrys⟩ :=
      _root_.GlobalTheory.Published.abelianDeRhamStructure_crystallineDeRham_of_hypotheses
        GlobalTheory.SmoothLift.crystallineSmoothLift_of_relations hH
    have hF : GlobalTheory.Published.AbelianDeRham.Free :=
      GlobalTheory.AbelianPrim.abelianDeRham_free hfree
    exact ⟨hF, hhodge, hbc,
      GlobalTheory.Published.AbelianDeRham.rigid_of_free_of_crystallineDeRham hF hcrys,
      _root_.GlobalTheory.CubeDual.abelianDeRham_duality hC hD hP hF⟩

end GlobalTheory
