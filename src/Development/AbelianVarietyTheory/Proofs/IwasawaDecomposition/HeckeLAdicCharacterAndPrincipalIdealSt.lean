module

public import Development.AbelianVarietyTheory.PublishedTheorems.AutomorphicForms2.ExistsUniqueHcharOfFiniteOrder
public import Development.AbelianVarietyTheory.PublishedTheorems.AutomorphicForms2.IsPrincipalMapOfAlgHom
public import Development.AbelianVarietyTheory.Proofs.IwasawaDecomposition.IsOpenKerOfInfConn
public import Development.AbelianVarietyTheory.Proofs.IwasawaDecomposition.PrincipalIdealSt

@[expose] public section

namespace GlobalTheory.Published

theorem GlobalArtinReciprocity.heckeLAdicCharacter_and_principalIdealSt :
    GlobalArtinReciprocity → HeckeLAdicCharacter ∧ PrincipalIdealSt :=
  fun h => ⟨h.heckeLAdicCharacter, h.principalIdealSt⟩

end GlobalTheory.Published
