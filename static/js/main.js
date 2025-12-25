function initCharts() {
    if (!document.getElementById('goldChart')) return;

    createPriceChart('gold', 'goldChart', 'rgb(255, 215, 0)');
    createPriceChart('silver', 'silverChart', 'rgb(192, 192, 192)');
}

async function createPriceChart(metal, canvasId, color) {
    try {
        const response = await fetch(`/api/historical/${metal}`);
        const data = await response.json();

        const ctx = document.getElementById(canvasId).getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.date),
                datasets: [{
                    label: `${metal.charAt(0).toUpperCase() + metal.slice(1)} Price (USD/oz)`,
                    data: data.map(d => d.price),
                    borderColor: color,
                    backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.1)'),
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(2);
                            }
                        }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error(`Error creating ${metal} chart:`, error);
    }
}

function startPriceRefresh() {
    setInterval(async () => {
        try {
            const response = await fetch('/api/prices');
            const prices = await response.json();
            
            console.log('Prices updated:', prices);
        } catch (error) {
            console.error('Error refreshing prices:', error);
        }
    }, 300000); 
}

document.addEventListener('DOMContentLoaded', () => {

});