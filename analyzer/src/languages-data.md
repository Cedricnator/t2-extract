---
theme: dashboard
title: Languages Dashboard
---

<!-- Load and transform the data -->

```js
const data = FileAttachment("data/github_analysis.json").json();
```

<div class="grid grid-cols-4 gap-4">
  <div class="card">
    <h3>Total Repositories</h3>
    <p class="big-number">${data.summary.total_repositories.toLocaleString()}</p>
  </div>
  <div class="card">
    <h3>Average Stars</h3>
    <p class="big-number">${Math.round(data.summary.avg_stars).toLocaleString()}</p>
  </div>
  <div class="card">
    <h3>Average Forks</h3>
    <p class="big-number">${Math.round(data.summary.avg_forks).toLocaleString()}</p>
  </div>
  <div class="card">
    <h3>Average Issues</h3>
    <p class="big-number">${Math.round(data.summary.avg_issues).toLocaleString()}</p>
  </div>
</div>

## Languages Distribution
```js
Plot.plot({
   marginLeft: 100,
   height: 300,
   x: {
      grid: true,
      label: "Number of Repositories"
   },
   y: {
      label: null
   },
   marks: [
      Plot.barX(data.languages.labels.map((label, i) => ({
         language: label,
         count: data.languages.values[i]
      })), {
         x: "count",
         y: "language",
         fill: "language",
         sort: {y: "-x"}
      }),
      Plot.text(data.languages.labels.map((label, i) => ({
         language: label,
         count: data.languages.values[i]
      })), {
         x: d => d.count + 50,
         y: "language",
         text: d => d.count.toLocaleString(),
         textAnchor: "start",
         fontWeight: "bold",
         dx: 5
      })
   ]
})
```



## Repository Creation Over Years
```js
Plot.plot({
  marginBottom: 40,
  height: 400,
  grid: true,
  x: {
    label: "Year",
    tickFormat: d => d.toString()
  },
  y: {
    label: "Number of Repositories"
  },
  marks: [
    Plot.lineY(data.yearly_creation.years.map((year, i) => ({
      year,
      count: data.yearly_creation.counts[i]
    })), {
      x: "year",
      y: "count",
      stroke: "steelblue",
      strokeWidth: 2
    }),
    Plot.dot(data.yearly_creation.years.map((year, i) => ({
      year,
      count: data.yearly_creation.counts[i]
    })), {
      x: "year",
      y: "count",
      fill: "steelblue"
    })
  ]
})
```

## Top 10 Repositories by Stars
```js
Plot.plot({
  marginLeft: 150,
  height: 400,
  x: {
    grid: true,
    label: "Stars"
  },
  y: {
    label: null
  },
  marks: [
    Plot.barX(data.top_repositories.slice(0, 10), {
      x: "stargazers_count",
      y: d => d.full_name,
      fill: d => d.language,
      sort: {y: "-x"}
    }),
    Plot.text(data.top_repositories.slice(0, 10), {
      x: d => d.stargazers_count + 10000,
      y: d => d.full_name,
      text: d => d.stargazers_count.toLocaleString(),
      textAnchor: "start",
      dx: 5
    })
  ]
})
```

## Fork-Star Ratio by Language
```js
Plot.plot({
  height: 300,
  x: {
    label: null
  },
  y: {
    grid: true,
    label: "Fork-Star Ratio (%)",
    tickFormat: d => d + "%"
  },
  marks: [
    Plot.barY(data.fork_star_ratio.languages.map((lang, i) => ({
      language: lang,
      ratio: Math.round(data.fork_star_ratio.ratios[i] * 100 * 10) / 10
    })), {
      x: "language",
      y: "ratio",
      fill: "language"
    }),
    Plot.text(data.fork_star_ratio.languages.map((lang, i) => ({
      language: lang,
      ratio: Math.round(data.fork_star_ratio.ratios[i] * 100 * 10) / 10
    })), {
      x: "language",
      y: d => d.ratio + 2,
      text: d => d.ratio + "%",
      textAnchor: "middle",
      fontWeight: "bold"
    })
  ]
})
```

<style>
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1rem;
  text-align: center;
}

.big-number {
  font-size: 2rem;
  font-weight: bold;
  color: #0066cc;
}
</style>
