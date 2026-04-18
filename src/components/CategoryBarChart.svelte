<script>
  import * as d3 from 'd3';
  import { createEventDispatcher } from 'svelte';

  export let series = [];
  export let selectedValues = [];
  export let title = 'Animal detail';
  export let subtitle = 'Click bars to toggle categories';
  export let width = 560;
  export let height = 280;

  const dispatch = createEventDispatcher();
  const margin = { top: 12, right: 16, bottom: 88, left: 44 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  $: xScale = d3.scaleBand()
    .domain(series.map((d) => d.key))
    .range([0, innerWidth])
    .padding(0.18);

  $: yMax = d3.max(series, (d) => d.fullValue) ?? 1;
  $: yScale = d3.scaleLinear().domain([0, yMax]).nice().range([innerHeight, 0]);
  $: hasSelection = selectedValues.length > 0;
  $: overlayWidth = xScale.bandwidth() * 0.7;

  let xAxis;
  let yAxis;

  $: if (xAxis) {
    d3.select(xAxis)
      .call(d3.axisBottom(xScale))
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('dx', '-0.5em')
      .attr('dy', '0.15em')
      .attr('transform', 'rotate(-32)');
  }

  $: if (yAxis) {
    d3.select(yAxis).call(d3.axisLeft(yScale).ticks(5).tickSizeOuter(0));
  }

  function toggle(value) {
    dispatch('toggleValue', value);
  }

  function handleKeydown(event, value) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggle(value);
    }
  }
</script>

<div class="chart-card">
  <div class="chart-header">
    <div>
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </div>
    <div class="chart-note">{selectedValues.length} selected</div>
  </div>

  <svg {width} {height} aria-label={title}>
    <g transform={`translate(${margin.left},${margin.top})`}>
      {#each series as d}
        <g class="bar-group" transform={`translate(${xScale(d.key)},0)`} role="button" tabindex="0" aria-label={`Toggle ${d.key}`} on:click={() => toggle(d.key)} on:keydown={(event) => handleKeydown(event, d.key)}>
          <rect
            class="background-bar"
            x="0"
            y={yScale(d.fullValue)}
            width={xScale.bandwidth()}
            height={innerHeight - yScale(d.fullValue)}
            rx="6"
          />
          <rect
            class:selected={selectedValues.includes(d.key)}
            class:faded={hasSelection && !selectedValues.includes(d.key)}
            class="foreground-bar"
            x={(xScale.bandwidth() - overlayWidth) / 2}
            y={yScale(d.filteredValue)}
            width={overlayWidth}
            height={innerHeight - yScale(d.filteredValue)}
            rx="6"
          />
          <title>{`${d.key}: ${d.filteredValue} filtered • ${d.fullValue} total`}</title>
        </g>
      {/each}

      <g bind:this={yAxis} />
      <g bind:this={xAxis} transform={`translate(0,${innerHeight})`} />
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

  .bar-group {
    cursor: pointer;
  }

  .background-bar {
    fill: #e5e7eb;
  }

  .foreground-bar {
    fill: #0891b2;
    transition: opacity 140ms ease, fill 140ms ease;
  }

  .foreground-bar.selected {
    fill: #0f766e;
  }

  .foreground-bar.faded {
    opacity: 0.35;
  }

  :global(.tick text) {
    fill: #4b5563;
    font-size: 0.72rem;
  }

  :global(.tick line),
  :global(path.domain) {
    stroke: #cbd5e1;
  }
</style>
