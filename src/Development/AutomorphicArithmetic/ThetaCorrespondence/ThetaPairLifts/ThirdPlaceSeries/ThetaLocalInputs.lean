module

public import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.WeightsConj
public import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.HeckeLAdicParameterAbove
public import Development.AbelianVarietyTheory.PublishedTheorems.AutomorphicForms2.DeRhamPotSemistable
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.ChebotarevDegreeOneIffCheb
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.HeckeLAdicCharacterAboveIff
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisGeometry2.DepthZeroJacquetInjective
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisGeometry2.UnlinkedProductIrreducible
public import Development.AbelianVarietyTheory.PublishedTheorems.TwistedTraceFormula.BernsteinUnitaryProductIrreducible
public import Development.AbelianVarietyTheory.PublishedTheorems.TwistedTraceFormula.HasFiniteLengthOfIsIrreducible
import Development.AbelianVarietyTheory.Definitions.GaloisGeometry.IsobaricDiscreteSelfDualStrongMultiplicityOne

@[expose] public section



section
section
noncomputable section
namespace GlobalTheory.NRows
open Formalism.BasicNotions Formalism.MainNotions Formalism.MainNotions.N GlobalTheory.RowCopy
structure ThetaLocalInputsAlt : Prop where
  bz : GlobalTheory.Published.BernsteinZelevinskyFiniteness
  bern : GlobalTheory.Published.BernsteinUnitaryProductIrreducible
  geo : GlobalTheory.Published.GeometricLemma
  unl : GlobalTheory.Published.UnlinkedProductIrreducible
  mp : GlobalTheory.Published.DepthZeroJacquetInjective
  js : GlobalTheory.Published.JacquetShalika
  fin : GlobalTheory.Published.AutomorphicFormsFiniteGL
  gal : _root_.UpperTheory.GalS.CuspUAlt
  car : _root_.UpperTheory.GalS.CarUAlt
  clo : GlobalTheory.Published.RegularAlgebraicPurity
  art : GlobalTheory.Published.GlobalArtinReciprocity
  chA : GlobalTheory.Published.HeckeLAdicCharacterAbove
  chP : _root_.GlobalTheory.Published.HeckeLAdicParameterAboveAlt
  berger : GlobalTheory.Published.DeRhamPotSemistable
  cheb : GlobalTheory.Published.ChebotarevDegreeOne
namespace Inputs
end Inputs
end GlobalTheory.NRows
end
end
end
