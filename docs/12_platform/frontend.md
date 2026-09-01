# Chapter 35: Frontend Design (React)

> The user interface that renders pipeline results as interactive
> dashboards, charts, and tables -- the final layer of the platform.

---

## 1. What is it?

The **frontend** is Layer 4 of the platform (Ch 33). Built with
**React + TypeScript + Tailwind CSS**, it calls the FastAPI backend
(Ch 34) and renders ready-studied QC, differential expression, and
pathway results.

It is a **read-only** dashboard oriented around the GSE52778 study.

---

## 2. Why do we need it?

- A scientist-friendly way to explore results without running commands.
- Interactive charts (PCA, volcano, heatmap) make analysis intuitive.
- Tables let users search, sort, and filter DE genes.
- React Query gives a stable, cached data layer over the API.

---

## 3. Where does it fit?

```
API (Ch 34) <-- HTTP --> UI (React + TS + Tailwind)
                              |
                     Dashboard | QC | Results | Pathways
```

The UI is the top (visible) layer of the stack.

---

## 4. Input

- JSON responses from the FastAPI endpoints.

---

## 5. Output

- Interactive web pages bundled for the browser.

---

## 6. How it works (the stack)

| Concern | Tool |
|---------|------|
| Framework | React + TypeScript |
| Styling | Tailwind CSS |
| Routing | React Router v6 |
| Server state | React Query |
| Charts | Recharts / Plotly |
| Tables | TanStack Table |
| Icons | Lucide React |

### 6.1 Pages (v1 scope)

| Route | Content |
|-------|---------|
| `/` | Dashboard overview |
| `/qc` | Quality control metrics & charts |
| `/results` | DE results / counts table |
| `/pathways` | Enrichment results |

### 6.2 Read-only mock data

v1 uses static mock data from `ui/src/data/mockData.ts` so the UI is
fully functional before the API/DB are built. Later it swaps to real
API calls.

---

## 7. Biology behind it

- The frontend surfaces biological findings: DE genes (CRISPLD2,
  FKBP5, DUSP1...), pathway enrichments, and QC quality.
- Charts (volcano, PCA, heatmap) are the visual language biologists
  use to interpret the analysis.

---

## 8. Command

```bash
# scaffold & run the UI (Phase 2)
cd ui
npm install
npm run dev
# open http://localhost:5173
```

---

## 9. Example

The **Results** page renders a TanStack table of DE genes with sortable
columns (gene, log2FC, padj) and a linked volcano plot.

---

## 10. How to read the output

- **Dashboard** = overall status and key numbers.
- **QC** = FastQC/fastp metrics as charts.
- **Results** = DE table + volcano/heatmap.
- **Pathways** = GO/GSEA/Reactome term tables.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| White screen | Check dev server / build |
| API calls fail | Point to correct API base URL / CORS |
| Missing deps | `npm install` |
| Route not found | Configure React Router v6 routes |

---

## 12. Limitations

- v1 is read-only with mock data (real runs trigger later).
- Charts reflect pre-computed results, not live streaming.
- Requires the API (Ch 34) for dynamic data (future).

---

## 13. How our project uses it

- **Future / Phase 2**: `ui/` (Vite + React + TS).
- v1 read-only dashboard from mock data.
- The 6 data points and key genes (from overview) are surfaced here.

---

## 14. Official documentation

- **React**:
  https://react.dev/
- **Vite**:
  https://vite.dev/
- **Tailwind CSS**:
  https://tailwindcss.com/
- **TanStack Table**:
  https://tanstack.com/table

---

## 15. Mini exercise

1. Name the CSS framework, chart library, and table library used.
2. Why does v1 use mock data (`mockData.ts`)?
3. What are the 4 planned pages/routes?
4. How does React Query help the UI talk to the API?
5. How do the UI charts (volcano, PCA) connect to Ch 19-20?

---

**End of the 35-Chapter Learning Guide.**
