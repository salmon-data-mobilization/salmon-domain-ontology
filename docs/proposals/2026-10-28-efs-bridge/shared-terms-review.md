# Draft shared terms for effective female-spawner data

These are proposed definitions for review, outside every ontology import
spine, flattened ontology and release. The candidate IRIs remain unminted;
merging this documentation does not admit them to the shared core.

The proposed `smn:UnspawnedEggAdjustment` is a SKOS method concept and
`sosa:Procedure`: a calculation procedure that derives effective female
spawner abundance by reducing estimated female spawner abundance according to
the estimated proportion of eggs not spawned. Its evidence is
[PSC Table 3, page 9](https://www.psc.org/download/130/frp-data/19739/stock-recruit-data-documentation.pdf#page=9)
and [Grant et al. (2011), printed page 27](https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/344553.pdf#page=35).
Partial spawning contributes proportionally; field sampling and imputation
remain separately documented provenance.

The proposed `smn:SpawnerAbundance` is an OWL **result class** under
`smn:ObservedRateOrAbundance`: a measurement datum recording the abundance of
salmon in a declared spawning-stage population component for a specified
assessment unit and time. It follows the existing SDO
[CatchAbundance and RecruitAbundance result pattern](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/66571e05a49296688ac60fb6d007671fb06fccbd/ontology/modules/03-assessment-benchmarks.ttl).
The measured characteristic remains `smn:Abundance`. Sex, origin, jack
inclusion, measurement boundary and spawning-success adjustment remain
explicit, so sharing the result category does not establish measurement
equivalence.

The complete candidate annotations and source citations are in
[`shared-terms.ttl`](shared-terms.ttl). Neither candidate asserts equivalence
to an existing DFO class, and no new female vocabulary value is proposed.
Domain admission remains a separate decision from merging this draft.
