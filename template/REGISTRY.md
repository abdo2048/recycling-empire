# Method registry — <material>

One entry per known method (patented, published, company disclosure, hypothesized, failed). **Append-only; never delete.** Update status fields only with citations.

## Entry format (one entry per method)

- id: M-XX
  name:
  source_type: patent | patent+company | company disclosure | peer-reviewed | thesis | report | press | failed attempt
  assignee:
  mechanism_class: mechanical | thermal | wet-chemical | solvent | supercritical-fluid | biological | construction-material | polymer-processing | other
  disclosed: (parameters with units and mass basis; `parameter_not_located` where absent)
  equipment:
  outputs:
  gaps: [list]
  legal_status:
  citations: [URLs]
  status: harvested | summary-card | full-plan | deprioritized
  priority: true | false
