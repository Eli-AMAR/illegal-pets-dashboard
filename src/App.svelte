<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import ChoroplethMap from './components/ChoroplethMap.svelte';
  import CategoryBarChart from './components/CategoryBarChart.svelte';
  import HistogramBrush from './components/HistogramBrush.svelte';
  import { loadDashboardData, applyFilters, countBy, mergeCategoryCounts, zipCountLookup } from './lib/dataUtils.js';

  let complaints = [];
  let zipFeatures = [];
  let isLoading = true;

  let selectedZips = [];
  let selectedAnimals = [];
  let createdRange = null;
  let ageRange = null;

  onMount(async () => {
    const loaded = await loadDashboardData();
    complaints = loaded.complaints;
    zipFeatures = loaded.zipFeatures;
    isLoading = false;
  });

  $: filters = { selectedZips, selectedAnimals, createdRange, ageRange };
  $: filteredComplaints = applyFilters(complaints, filters);

  $: fullZipCounts = zipCountLookup(complaints);
  $: filteredZipCounts = zipCountLookup(filteredComplaints);
  $: mapFeatures = zipFeatures.map((feature) => ({
    ...feature,
    fullCount: fullZipCounts.get(feature.properties.zip) ?? 0,
    filteredCount: filteredZipCounts.get(feature.properties.zip) ?? 0,
  }));

  $: fullAnimalCounts = countBy(complaints, (d) => d.animalDetail);
  $: filteredAnimalCounts = countBy(filteredComplaints, (d) => d.animalDetail);
  $: animalSeries = mergeCategoryCounts(fullAnimalCounts, filteredAnimalCounts);

  $: complaintsWithCreated = complaints.filter((d) => d.created);
  $: filteredWithCreated = filteredComplaints.filter((d) => d.created);
  $: complaintsWithAge = complaints.filter((d) => Number.isFinite(d.caseAgeDays));
  $: filteredWithAge = filteredComplaints.filter((d) => Number.isFinite(d.caseAgeDays));

  $: totalVisible = filteredComplaints.length;
  $: totalAll = complaints.length;
  $: selectedZipComplaintCount = selectedZips.length === 0
    ? totalVisible
    : filteredComplaints.filter((d) => d.zip && selectedZips.includes(d.zip)).length;

  function toggleZip(zip) {
    selectedZips = selectedZips.includes(zip)
      ? selectedZips.filter((d) => d !== zip)
      : [...selectedZips, zip];
  }

  function toggleAnimal(animal) {
    selectedAnimals = selectedAnimals.includes(animal)
      ? selectedAnimals.filter((d) => d !== animal)
      : [...selectedAnimals, animal];
  }

  function clearFilters() {
    selectedZips = [];
    selectedAnimals = [];
    createdRange = null;
    ageRange = null;
  }

  $: activeFilters = [
    selectedZips.length > 0 ? `${selectedZips.length} ZIP${selectedZips.length > 1 ? 's' : ''}` : null,
    selectedAnimals.length > 0 ? `${selectedAnimals.length} animal type${selectedAnimals.length > 1 ? 's' : ''}` : null,
    createdRange ? 'created-date brush' : null,
    ageRange ? 'case-age brush' : null,
  ].filter(Boolean);

  const dateLabel = d3.timeFormat('%b %Y');
</script>

{#if isLoading}
  <main class="loading-state">
    <h1>Loading NYC illegal pets dashboard…</h1>
  </main>
{:else}
  <main class="page-shell">
    <section class="hero">
      <div>
        <h1>Illegal pets in New York City</h1>
        <p class="intro">
          This dashboard crossfilters NYC 311 complaints about illegal animals using four linked views:
          an interactive ZIP-code choropleth, an animal-detail bar chart, a created-date histogram,
          and a case-age histogram.
        </p>
      </div>

      <div class="summary-panel">
        <div class="summary-card">
          <span class="summary-label">Visible complaints</span>
          <strong>{totalVisible}</strong>
          <small>out of {totalAll}</small>
        </div>
        <div class="summary-card">
          <span class="summary-label">ZIP-filtered complaints</span>
          <strong>{selectedZipComplaintCount}</strong>
          <small>{selectedZips.length === 0 ? 'no ZIP filter' : 'within selected ZIPs'}</small>
        </div>
        <div class="summary-card wide">
          <span class="summary-label">Active filters</span>
          <div class="chips">
            {#if activeFilters.length === 0}
              <span class="chip muted">none</span>
            {:else}
              {#each activeFilters as item}
                <span class="chip">{item}</span>
              {/each}
            {/if}
          </div>
          <button class="clear-button" on:click={clearFilters}>Clear all filters</button>
        </div>
      </div>
    </section>

    {#if createdRange || ageRange}
      <section class="selection-caption">
        {#if createdRange}
          <span>Created between {dateLabel(createdRange[0])} and {dateLabel(createdRange[1])}</span>
        {/if}
        {#if ageRange}
          <span>Case age between {Math.round(ageRange[0])} and {Math.round(ageRange[1])} days</span>
        {/if}
      </section>
    {/if}

    <section class="dashboard-grid">
      <div class="map-panel">
        <ChoroplethMap
          features={mapFeatures}
          {selectedZips}
          on:toggleZip={(event) => toggleZip(event.detail)}
        />
      </div>

      <div class="side-panel">
        <CategoryBarChart
          title="Animal detail"
          subtitle="Click one or more bars to keep only those complaint types"
          series={animalSeries}
          selectedValues={selectedAnimals}
          on:toggleValue={(event) => toggleAnimal(event.detail)}
        />

        <HistogramBrush
          title="Created date"
          subtitle="Brush the timeline to restrict the complaint filing period"
          fullData={complaintsWithCreated}
          filteredData={filteredWithCreated}
          accessor={(d) => d.created}
          selection={createdRange}
          type="time"
          bins={28}
          tickFormat={d3.timeFormat('%Y')}
          on:changeSelection={(event) => createdRange = event.detail}
        />

        <HistogramBrush
          title="Case age (days)"
          subtitle="Brush to focus on how long cases have remained open or took to close"
          fullData={complaintsWithAge}
          filteredData={filteredWithAge}
          accessor={(d) => d.caseAgeDays}
          selection={ageRange}
          type="linear"
          bins={30}
          tickFormat={d3.format('~s')}
          on:changeSelection={(event) => ageRange = event.detail}
        />
      </div>
    </section>
  </main>
{/if}
