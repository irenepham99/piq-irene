<script lang="ts">
    import { onMount } from "svelte";
    import {
        Chart as ChartJS,
        LineController,
        TimeScale,
        LinearScale,
        LineElement,
        PointElement,
        Tooltip,
        Legend,
        Title,
    } from "chart.js";
    import "chartjs-adapter-date-fns";
    import type { Datapoint } from '../../../types';

    ChartJS.register(LineController, TimeScale, LinearScale, LineElement, PointElement, Tooltip, Legend, Title);

    let chartCanvas : HTMLCanvasElement; // Reference to the canvas element
    let chartInstance : ChartJS; // Store the Chart.js instance
    export let scenarioNum : Number;
    export let results : Datapoint[];

    // Chart configuration
    const config = {
        type: "line",
        data: {
            datasets: [
                {
                    label: "Power (MW)",
                    data: results.map(entry => ({ x: entry.datetime, y: entry.power_MW})),
                    borderColor: "blue",
                    backgroundColor: "rgba(0, 0, 255, 0.3)",
                    tension: 0.3, 
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
                title: {
                    display: true,
                    text: "Time vs Power",
                },
            },
            scales: {
                x: {
                    type: "time",
                    time: {
                        unit: "hour",
                        tooltipFormat: "MM/dd    HH:00", 
                        displayFormats: {
                            hour: "MM/dd    HH:00", 
                 
                        },
                    },
                    title: {
                        display: true,
                        text: "Time",
                    },
                },
                y: {
                    type: "linear",
                    title: {
                        display: true,
                        text: "Power (MW)",
                    },
                },
            },
        },
    };

    // Initialize the chart
    onMount(() => {
        chartInstance = new ChartJS(chartCanvas, config);

        // Cleanup when the component is destroyed
        return () => chartInstance.destroy();
    });
</script>

<canvas bind:this={chartCanvas}></canvas>
