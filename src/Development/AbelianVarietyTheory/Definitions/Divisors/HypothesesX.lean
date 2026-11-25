module

public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.ToroidalCompactificationBis
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.InterNumDetNonposSplitTorus
public import Development.AbelianVarietyTheory.PublishedTheorems.GaloisCohomology2.GreenCuspidalIff
public import Development.AbelianVarietyTheory.PublishedTheorems.Divisors2.PointSeparationPair

@[expose] public section

namespace GlobalTheory.CovTop

structure HypothesesX : Prop where

  ks : GlobalTheory.Published.ToroidalForFanKS

  lie : GlobalTheory.Published.SemiAbelianLieSeminegative

  green : GlobalTheory.Published.GreenCuspidal

  sep : GlobalTheory.Published.PointSeparationPair

end GlobalTheory.CovTop
