const barEl = document.getElementById('barChart');
const lineEl = document.getElementById('lineChart');

// Guard if elements are missing
if (barEl) {
  const barCtx = barEl.getContext('2d');
  const storeLabels = JSON.parse(barEl.dataset.labels || '[]');
  const storeValues = JSON.parse(barEl.dataset.values || '[]');

  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: storeLabels,
      datasets: [
        {
          label: 'Hours',
          data: storeValues,
          backgroundColor: '#3B82F6'
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}

if (lineEl) {
  const lineCtx = lineEl.getContext('2d');
  const dailyLabels = JSON.parse(lineEl.dataset.labels || '[]');
  const dailyValues = JSON.parse(lineEl.dataset.values || '[]');

  new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: dailyLabels,
      datasets: [
        {
          label: 'Hours Worked',
          data: dailyValues,
          borderColor: '#3B82F6',
          backgroundColor: 'rgba(59,130,246,0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}
