import * as d3 from 'd3';

export async function loadDashboardData() {
  const [complaintsRaw, geojson] = await Promise.all([
    d3.json('/illegal-animal-complaints.json'),
    d3.json('/nyc-zip-boundaries.geojson')
  ]);

  const complaints = complaintsRaw
    .filter((d) => d.created)
    .map((d) => ({
      ...d,
      created: new Date(d.created),
      closed: d.closed ? new Date(d.closed) : null,
      caseAgeDays: +d.caseAgeDays,
      borough: d.borough ?? 'Unknown',
      animalDetail: d.animalDetail ?? 'Unknown',
      complaintType: d.complaintType ?? 'Unknown',
      locationType: d.locationType ?? 'Unknown',
      status: d.status ?? 'Unknown',
      zip: d.zip ?? null,
    }));

  return {
    complaints,
    zipFeatures: geojson.features,
  };
}

export function applyFilters(complaints, filters) {
  return complaints.filter((d) => {
    const zipOk = filters.selectedZips.length === 0 || (d.zip && filters.selectedZips.includes(d.zip));
    const animalOk = filters.selectedAnimals.length === 0 || filters.selectedAnimals.includes(d.animalDetail);
    const createdOk =
      !filters.createdRange ||
      (d.created >= filters.createdRange[0] && d.created <= filters.createdRange[1]);
    const ageOk =
      !filters.ageRange ||
      (d.caseAgeDays >= filters.ageRange[0] && d.caseAgeDays <= filters.ageRange[1]);

    return zipOk && animalOk && createdOk && ageOk;
  });
}

export function countBy(items, accessor, preferredOrder = null) {
  const counts = d3.rollups(
    items,
    (values) => values.length,
    accessor,
  ).map(([key, value]) => ({ key, value }));

  if (preferredOrder) {
    const position = new Map(preferredOrder.map((value, index) => [value, index]));
    counts.sort((a, b) => (position.get(a.key) ?? Number.MAX_SAFE_INTEGER) - (position.get(b.key) ?? Number.MAX_SAFE_INTEGER));
    return counts;
  }

  return counts.sort((a, b) => d3.descending(a.value, b.value) || d3.ascending(a.key, b.key));
}

export function mergeCategoryCounts(fullCounts, filteredCounts) {
  const filteredLookup = new Map(filteredCounts.map((d) => [d.key, d.value]));
  return fullCounts.map((d) => ({
    key: d.key,
    fullValue: d.value,
    filteredValue: filteredLookup.get(d.key) ?? 0,
  }));
}

export function zipCountLookup(items) {
  return new Map(d3.rollups(items.filter((d) => d.zip), (values) => values.length, (d) => d.zip));
}
