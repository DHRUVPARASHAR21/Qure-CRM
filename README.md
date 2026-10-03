# Qure.ai India Life Sciences CRM

Evidence-first CRM workspace for Qure.ai's India Life Sciences Business Development team.

## Primary deliverables

- `outputs/qure-life-sciences-crm-qure-styled/qure_india_life_sciences_crm_qure_styled.xlsx` - Qure-branded Excel CRM with accounts, contacts, opportunities, activities, research sources, controls, formulas, and dashboard.
- `output/pdf/qure_crm_full_scale_vertical_onboarding_poster.pdf` - full-scale vertical onboarding poster with detailed CRM screenshots and operating guidance.
- `output/pdf/qure_crm_single_page_operating_poster.pdf` - compact A3 operating-poster variant.
- `outputs/qure-crm-onboarding-field-guide/qure_crm_india_field_guide.pdf` - eight-page field guide.

The CRM research uses public professional information only. Unverified data is explicitly marked and must not be used as outreach-ready contact data.

## Rebuild artifacts

Use the supplied scripts to reproduce the workbook and posters. The output PDFs are generated with ReportLab; Excel workbooks are generated with the bundled spreadsheet runtime.

---

# Qure.ai Life Sciences BD Operating Cadence

Responsive front-end prototype for FY26 goal tracking, weekly reviews, risks and decision follow-up.

## Run

`npm install` then `npm run dev`.

## Main workflows

- **Executive overview:** annual attainment, forecast, KPI movement, RAG and blockers.
- **Goal tracker:** filter milestones, open a row for context and export a CSV.
- **Weekly review:** use the auto-generated agenda, record a decision, follow up commitments and export a meeting pack.
- **Analytics:** identify velocity, capacity and dependency interventions.
- **Data & admin:** see mock source health, roles and entity boundaries.

## Data model and backend path

The current client-side seed represents `AnnualObjective → KeyResult → Milestone → ActionItem`, with `Owner` and `DataSource` supporting entities. Replace the seeded arrays in `src/main.jsx` with a repository module, such as `src/data/goalsRepository.js`, that calls REST or GraphQL and normalizes CRM, PM and evidence-source data into this model. Apply role-scoped API results for leadership, owner and analyst views.

## Design basis

The interface is based on Qure.ai's public clinical, global and evidence-led brand presence: a white clinical canvas, restrained teal/blue emphasis, outcome-forward language and minimal decorative treatment. The selected Awesome DESIGN.md IBM reference informed data-density, flat borders and table/chart discipline only. It does not copy IBM branding.

## States and accessibility

Includes populated data, a saved-view empty state, a source-sync warning, keyboard-focusable table rows, visible focus treatment, semantic status colors and responsive reflow.
