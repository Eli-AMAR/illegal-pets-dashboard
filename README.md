# NYC Illegal Pets Dashboard
A crossfiltered dashboard built with **Svelte** and **D3** for exploring NYC complaints about illegal animals.
**Deployment URL:** 
`https://keen-pony-4310b8.netlify.app/`
## What the dashboard includes
1. **Interactive choropleth map** of NYC ZIP codes, colored by the number of filtered complaints.
2. **Animal-detail bar chart** with click-to-select categories.
3. **Created-date histogram** with a brush selection.
4. **Case-age histogram** with a brush selection.
All views are linked through crossfiltering. A selection in any chart updates the other views.
## Notes on design choices
- The choropleth uses a **sequential color scale** because complaint count is quantitative.
- The map aggregates complaints by ZIP code for a choropleth view.
- The dashboard uses **reusable chart components** so the views remain modular.
- The case-age histogram is a derived variable based on the number of days between complaint creation and complaint closure, or the latest complaint date when a complaint is still open.