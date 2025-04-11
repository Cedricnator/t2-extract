---
theme: dashboard
title: GitHub Repository Analysis Dashboard
---

<!-- Load and transform the data -->

```js
const data = FileAttachment("data/github_analysis.json").json();
```

<div class="grid grid-cols-4 gap-4">
  <div class="card">
    <h3>Número total de repositorios analizados</h3>
    <p class="big-number">${data.summary.total_repositories.toLocaleString()}</p>
  </div>
  <div class="card">
    <h3>Promedio de estrellas</h3>
    <p class="big-number">${Math.round(data.summary.avg_stars).toLocaleString()}</p>
  </div>
  <div class="card">
    <h3>Promedio de Forks</h3>
    <p class="big-number">${Math.round(data.summary.avg_forks).toLocaleString()}</p>
  </div>
  <div class="card">
    <h3>Promedio de issues/problemas</h3>
    <p class="big-number">${Math.round(data.summary.avg_issues).toLocaleString()}</p>
  </div>
</div>

## Distribución de lenguajes de programación
```js
Plot.plot({
  height: 300,
  width: 2000,
   x: {
      grid: true,
      label: "Número de repositorios"
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

## Creación de repositorios a lo largo de los años
```js
Plot.plot({
  marginBottom: 40,
  height: 400,
  grid: true,
  width: 2000,
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

## Los 10 mejores repositorios según sus estrellas
```js
Plot.plot({
  marginLeft: 150,
  height: 600,
  width: 2000,
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

## Relación Fork-Star por lenguaje de programación
```js
Plot.plot({
  height: 300,
  width: 2000,
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

## Determinación óptima del grupo: análisis del método del codo

<div class="explanation-box">
  <p>El Método del Codo nos ayuda a identificar el número ideal de clústeres para agrupar repositorios con características similares. El gráfico muestra cómo la Suma de Cuadrados Dentro del Clúster (WCSS) disminuye a medida que añadimos más clústeres. El "elbow point" (highlighted in red) at k=${data.elbow_method.optimal_k} representa el equilibrio óptimo entre simplicidad y precisión, donde añadir más clústeres produce rendimientos decrecientes.</p>
  <p>Nuestro análisis confirma que las distintas categorías de repositorios (${data.elbow_method.optimal_k}) capturan los patrones naturales en las métricas de los repositorios de GitHub, en consonancia con nuestra clasificación de repositorios  del tipo Standard, Popular, and Superstar.</p>
</div>

```js
Plot.plot({
  height: 400,
  grid: true,
  x: {
    label: "Número de Clústeres (k)",
    domain: [1, 10]
  },
  y: {
    label: "Suma de Cuadrados Dentro del Clúster (WCSS)",
    domain: [0, Math.max(...data.elbow_method.points.map(d => d.wcss)) * 1.1]
  },
  marks: [
    Plot.lineY(data.elbow_method.points, {
      x: "k", 
      y: "wcss",
      stroke: "steelblue",
      strokeWidth: 2
    }),
    Plot.dot(data.elbow_method.points, {
      x: "k", 
      y: "wcss",
      fill: d => d.k === data.elbow_method.optimal_k ? "red" : "steelblue",
      r: d => d.k === data.elbow_method.optimal_k ? 8 : 5
    }),
    // Resaltar el punto de codo
    Plot.text([{
      x: data.elbow_method.optimal_k,
      y: data.elbow_method.points.find(d => d.k === data.elbow_method.optimal_k)?.wcss,
      text: `K óptimo = ${data.elbow_method.optimal_k}`
    }], {
      dy: -15,
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
