<script>
  import * as d3 from 'd3';
  import { createEventDispatcher } from 'svelte';

  export let fullData = [];
  export let filteredData = [];
  export let accessor;
  export let selection = null;
  export let title = 'Histogram';
  export let subtitle = 'Brush to filter';
  export let width = 560;
  export let height = 280;
  export let type = 'linear';
  export let bins = 24;
  export let tickFormat = null;

  const dispatch = createEventDispatcher();
  const margin = { top: 12, right: 16, bottom: 40, left: 44 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  let xAxis;
  let yAxis;
  let brushLayer;

  const brush = d3.brushX();

  function domainToRange(domain) {
    if (!domain) return null;
    return [xScale(domain[0]), xScale(domain[1])];
  }

  function brushed(event) {
    if (!event.sourceEvent) return; // ignore les updates programmatiques
    if (!event.selection) return;

    const [x0, x1] = event.selection;
    const range = [xScale.invert(x0), xScale.invert(x1)];
    dispatch('changeSelection', range);
  }

  function brushEnded(event) {
    if (!event.sourceEvent) return; // ignore brush.move()
    if (!event.selection) {
      dispatch('changeSelection', null);
    }
  }

  $: values = fullData.map(accessor).filter((d) => d !== null && d !== undefined && !Number.isNaN(+d));
  $: xDomain = d3.extent(values);
  $: xScale = type === 'time'
    ? d3.scaleTime().domain(xDomain).range([0, innerWidth])
    : d3.scaleLinear().domain(xDomain).nice().range([0, innerWidth]);

  function makeBinner(dataset) {
    if (type === 'time') {
      return d3.bin()
        .value((d) => accessor(d))
        .domain(xScale.domain())
        .thresholds(bins);
    }

    return d3.bin()
      .value((d) => accessor(d))
      .domain(xScale.domain())
      .thresholds(xScale.ticks(bins));
  }

  $: histogram = makeBinner(fullData);
  $: backgroundBins = histogram(fullData);
  $: binsFiltered = histogram(filteredData);
  $: yMax = d3.max(backgroundBins, (d) => d.length) ?? 1;
  $: yScale = d3.scaleLinear().domain([0, yMax]).nice().range([innerHeight, 0]);
  $: overlayWidth = backgroundBins.length > 0
    ? Math.max(2, (xScale(backgroundBins[0].x1) - xScale(backgroundBins[0].x0)) * 0.72)
    : 0;

  $: axisFormatter = tickFormat
    ? tickFormat
    : type === 'time'
      ? d3.timeFormat('%Y')
      : d3.format('~s');

  $: if (xAxis) {
    d3.select(xAxis).call(d3.axisBottom(xScale).ticks(type === 'time' ? 6 : 5).tickFormat(axisFormatter));
  }

  $: if (yAxis) {
    d3.select(yAxis).call(d3.axisLeft(yScale).ticks(5).tickSizeOuter(0));
  }

  $: if (brushLayer) {
    brush
      .extent([[0, 0], [innerWidth, innerHeight]])
      .on('brush', brushed)
      .on('end', brushEnded);

    const layer = d3.select(brushLayer).call(brush);
    layer.call(brush.move, domainToRange(selection));
  }
</script>

<div class="chart-card">
  <div class="chart-header">
    <div>
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </div>
    <div class="chart-note">{selection ? 'filtered' : 'all values'}</div>
  </div>

  <svg {width} {height} aria-label={title}>
    <g transform={`translate(${margin.left},${margin.top})`}>
      {#each backgroundBins as bin}
        <rect
          class="background-bar"
          x={xScale(bin.x0)}
          y={yScale(bin.length)}
          width={Math.max(0, xScale(bin.x1) - xScale(bin.x0) - 1)}
          height={innerHeight - yScale(bin.length)}
          rx="4"
        />
      {/each}

      {#each binsFiltered as bin}
        <rect
          class="foreground-bar"
          x={xScale(bin.x0) + ((xScale(bin.x1) - xScale(bin.x0)) - overlayWidth) / 2}
          y={yScale(bin.length)}
          width={overlayWidth}
          height={innerHeight - yScale(bin.length)}
          rx="4"
        />
      {/each}

      <g bind:this={yAxis} />
      <g bind:this={xAxis} transform={`translate(0,${innerHeight})`} />
      <g bind:this={brushLayer} class="brush-layer" />
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

  .background-bar {
    fill: #e5e7eb;
  }

  .foreground-bar {
    fill: #f59e0b;
  }

  :global(.tick text) {
    fill: #4b5563;
    font-size: 0.72rem;
  }

  :global(.tick line),
  :global(path.domain) {
    stroke: #cbd5e1;
  }

  :global(.brush-layer .selection) {
    fill: rgba(14, 165, 233, 0.16);
    stroke: #0284c7;
  }
</style>
