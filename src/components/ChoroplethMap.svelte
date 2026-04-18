<script>
  import * as d3 from 'd3';
  import { createEventDispatcher } from 'svelte';

  export let features = [];
  export let selectedZips = [];
  export let width = 700;
  export let height = 520;
  export let title = 'Complaints by ZIP code';

  const dispatch = createEventDispatcher();
  const margin = { top: 12, right: 16, bottom: 24, left: 16 };
  const legendWidth = 180;
  const legendHeight = 10;

  $: featureCollection = { type: 'FeatureCollection', features };
  $: drawableFeatures = features.filter((d) => d?.geometry);
  $: projection = d3.geoMercator().fitSize(
    [width - margin.left - margin.right, height - margin.top - margin.bottom],
    featureCollection,
  );
  $: path = d3.geoPath(projection);
  $: maxCount = d3.max(features, (d) => d.fullCount ?? 0) ?? 1;
  $: colorScale = d3.scaleSequential(d3.interpolateOrRd).domain([0, Math.max(1, maxCount)]);
  $: legendTicks = colorScale.ticks ? colorScale.ticks(4) : [0, maxCount / 3, (2 * maxCount) / 3, maxCount];
  $: hasZipSelection = selectedZips.length > 0;

  function fillColor(feature) {
    if ((feature.filteredCount ?? 0) === 0) return '#f3f4f6';
    return colorScale(feature.filteredCount);
  }

  function handleToggle(zip) {
    dispatch('toggleZip', zip);
  }

  function handleKeydown(event, zip) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleToggle(zip);
    }
  }
</script>

<div class="chart-card">
  <div class="chart-header">
    <div>
      <h2>{title}</h2>
      <p>Click a ZIP polygon to filter all charts.</p>
    </div>
    <div class="chart-note">{selectedZips.length} selected</div>
  </div>

  <svg {width} {height} aria-label={title}>
    <defs>
      <linearGradient id="zipLegend" x1="0%" x2="100%" y1="0%" y2="0%">
        {#each d3.range(0, 1.01, 0.1) as stop}
          <stop offset={`${stop * 100}%`} stop-color={colorScale(stop * maxCount)} />
        {/each}
      </linearGradient>
    </defs>

    <g transform={`translate(${margin.left},${margin.top})`}>
      {#each drawableFeatures as feature}
        <path
          d={path(feature)}
          fill={fillColor(feature)}
          stroke={selectedZips.includes(feature.properties.zip) ? '#111827' : '#9ca3af'}
          stroke-width={selectedZips.includes(feature.properties.zip) ? 2.2 : 0.7}
          opacity={hasZipSelection && !selectedZips.includes(feature.properties.zip) ? 0.45 : 1}
          class:selected={selectedZips.includes(feature.properties.zip)}
          class="zip-path"
          role="button"
          tabindex="0"
          aria-label={`Toggle ZIP ${feature.properties.zip}`}
          on:click={() => handleToggle(feature.properties.zip)}
          on:keydown={(event) => handleKeydown(event, feature.properties.zip)}
        >
          <title>{`${feature.properties.zip} • ${feature.filteredCount ?? 0} filtered complaints • ${feature.fullCount ?? 0} total complaints`}</title>
        </path>
      {/each}
    </g>

    <g transform={`translate(${width - legendWidth - 26}, ${height - 50})`}>
      <text x="0" y="-8" class="legend-label">Filtered complaint count</text>
      <rect width={legendWidth} height={legendHeight} fill="url(#zipLegend)" rx="5" />
      {#each legendTicks as tick}
        <g transform={`translate(${(tick / Math.max(1, maxCount)) * legendWidth}, 0)`}>
          <line y1={legendHeight} y2={legendHeight + 6} stroke="#4b5563" />
          <text y={legendHeight + 18} x="0" text-anchor="middle" class="legend-tick">{Math.round(tick)}</text>
        </g>
      {/each}
    </g>
  </svg>
</div>

<style>
  .chart-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 0.85rem;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
  }

  .chart-header {
    align-items: start;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.35rem;
  }

  h2 {
    font-size: 1rem;
    margin: 0;
  }

  p {
    color: #6b7280;
    font-size: 0.86rem;
    margin: 0.15rem 0 0;
  }

  .chart-note {
    color: #374151;
    font-size: 0.82rem;
    font-weight: 600;
    white-space: nowrap;
  }

  .zip-path {
    cursor: pointer;
    transition: opacity 140ms ease, stroke-width 140ms ease;
  }

  .zip-path:hover {
    stroke: #111827;
    stroke-width: 1.8;
  }

  .legend-label,
  .legend-tick {
    fill: #4b5563;
    font-size: 0.72rem;
  }
</style>
