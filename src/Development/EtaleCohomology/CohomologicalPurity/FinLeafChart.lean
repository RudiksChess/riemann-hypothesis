module

public import Development.EtaleCohomology.CohomologicalPurity.LeafChartCut
public import Development.EtaleCohomology.CohomologicalPurity.LeafCoordPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafEtPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafLocPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafNbhdPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafPickPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafPolyPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafRankPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafSecPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafShrinkPf
public import Development.EtaleCohomology.CohomologicalPurity.LeafSpanPf

@[expose] public section

namespace LateralTheory.Fin.LeafChart

theorem etale_chart_localization_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafLoc :=
  LateralTheory.CohomologicalPurity.ChartCut.LeafLoc_of

theorem etale_chart_shrinking_open_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafShrink :=
  LateralTheory.CohomologicalPurity.ChartCut.LeafShrink_of

theorem etale_chart_conormal_rank_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafRank :=
  LateralTheory.CohomologicalPurity.ChartCut.LeafRank_of

theorem etale_chart_generator_choice_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafPick :=
  LateralTheory.CohomologicalPurity.ChartCut.LeafPick_of

theorem etale_chart_ideal_span_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafSpan :=
  LateralTheory.CohomologicalPurity.LeafSpanPf.LeafSpan_of

theorem etale_chart_etaleness_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafEt :=
  LateralTheory.CohomologicalPurity.LeafEtPf.LeafEt_of

theorem etale_chart_coordinate_functions_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafCoord :=
  LateralTheory.CohomologicalPurity.ChartCut.LeafCoord_of
    etale_chart_conormal_rank_property_holds
    etale_chart_generator_choice_property_holds
    etale_chart_ideal_span_property_holds
    etale_chart_etaleness_property_holds

theorem etale_chart_section_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafSec :=
  LateralTheory.CohomologicalPurity.LeafSecPf.LeafSec_of

theorem etale_chart_polynomial_algebra_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafPoly :=
  LateralTheory.CohomologicalPurity.LeafPolyPf.LeafPoly_of

theorem etale_chart_neighborhood_property_holds : LateralTheory.CohomologicalPurity.ChartCut.LeafNbhd :=
  LateralTheory.CohomologicalPurity.ChartCut.LeafNbhd_of
    etale_chart_section_property_holds
    etale_chart_polynomial_algebra_property_holds

theorem etale_coordinate_chart_existence : LateralTheory.CohomologicalPurity.LeafChart :=
  LateralTheory.CohomologicalPurity.ChartCut.goal_of
    etale_chart_localization_property_holds
    etale_chart_shrinking_open_property_holds
    etale_chart_coordinate_functions_property_holds
    etale_chart_neighborhood_property_holds

theorem intersectionNumber_baseChange : LateralTheory.CohomologicalPurity.LeafChart :=
  etale_coordinate_chart_existence

end LateralTheory.Fin.LeafChart
