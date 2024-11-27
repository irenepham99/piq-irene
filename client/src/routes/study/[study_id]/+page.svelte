<script lang="ts">
    import { onMount } from 'svelte';
    import Chart from './Chart.svelte';
    import { Tabs, TabItem, Button } from 'flowbite-svelte';
    import { goto } from '$app/navigation';
    import type { Datapoint } from '../../../types';
    

    export let data;
    let results : Datapoint[] = [];
    let loading = false; 
    let error : string | null = null;
    let startTime : Date | null = null; 
    let endTime : Date | null = null; 
    let scenarioType : string = ""; 

    // Fetch results from the study
    onMount(async () => {
        try {
            loading = true; 
            error = null;

            const response = await fetch(`http://127.0.0.1:8000/studies/${data.study_id}`);
            if (!response.ok) {
                throw new Error(`Error when trying to fetch results ${response.status}`);
            }
            let responseData = await response.json(); 

            results = responseData.results;
            startTime = new Date(responseData.start_time);
            endTime = new Date(responseData.end_time);
            scenarioType = responseData.scenario_type;
        } catch (err) {
            error = "Error when trying to fetch results" 
            if (err && err.message) {
                error += `: ${err.message}`;
            }
        } finally { 
            loading = false; 
        }
    })
</script>


    {#if loading}
        <h3>Loading</h3>
    {:else if error}
        <h3 style="color: red;">Error: {error}</h3>
    {:else}
    <div>
        <h1 class="mt-4 mb-4">
            Study Results
        </h1>
        <div class="details-container">
            <p class="text-gray-500"><b>Start Time:</b> {startTime instanceof Date ? startTime.toLocaleString() : 'Invalid date'}</p>
            <p class="text-gray-500"><b>End Time:</b> {endTime instanceof Date ? endTime.toLocaleString() : 'Invalid date'}</p>
            <p class="text-gray-500"><b>Scenario Type:</b> {scenarioType && scenarioType}</p>
        </div>
        
        <Tabs>
            {#each Array(2).fill(0).map((_, i) => i) as scenarioNum}
                <TabItem open={scenarioNum == 0 ? true : false} title={`Scenario ${scenarioNum}`}>
                    <Chart {scenarioNum} results={results.filter(datapoint => datapoint.scenario == scenarioNum)} />
                </TabItem>
            {/each}
        </Tabs>
        <div class="w-full grid grid-cols-1 content-center">
            <Button class="mt-4" on:click={() => goto('/')}>Run Another Study</Button>
        </div>
    </div>
    {/if}

<style>
    .details-container { 
        margin: 16px;
        display: flex; 
        flex-direction: row;
        column-gap: 32px;
        row-gap: 8px; 
        flex-wrap: wrap;
    }
</style>