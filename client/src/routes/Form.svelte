<script lang="ts">
    import { Card } from 'flowbite-svelte';
    export let runStudy : (data : object) => Promise<void>;
    let error : string | null = null;

    //Ensure start date is before end date
    const validDates = (startDateVal : FormDataEntryValue, endDateVal: FormDataEntryValue) => {
        const startDate = new Date(startDateVal as string);
        const endDate = new Date(endDateVal as string);

        if (!isNaN(startDate.getTime()) && !isNaN(endDate.getTime())) { 
            return startDate < endDate
        }  else { 
            error = "start date and end date are not properly formated"
            return false; 
        }

    }

    // Submit From and Run Study
	async function handleSubmit(e : SubmitEvent) {
		e.preventDefault(); 

        const form = e.target; 
        const formData = new FormData(form as HTMLFormElement); 

        const data : Record<string, FormDataEntryValue> = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        
        //errors are handled in the parent component
        if (validDates(data["start_time"], data["end_time"])) {
            await runStudy(data);
        } else { 
            error = "Start Date must be before End Date";
        }
	}
</script>

<Card>
	<form class="form-container m-4" onsubmit={(e) => handleSubmit(e)}>
        <div class="field-container">
            <label for="num_scenarios">Number of Scenarios</label>
            <input type="number" name="num_scenarios" id="num_scenarios" required/>
        </div>
        
        <div class="field-container">
            <label for="scenario_type">Scenario Type</label>
            <select id="scenario_type" name="scenario_type">
                <option value="summer peak">Summer Peak</option>
                <option value="winter peak">Winter Peak</option>
                <option value="light load">Light Load</option>
            </select>
        </div>
        
        <div class="field-container">
            <label for="start_time">Start Time</label>
            <input type="datetime-local" id="start_time" name="start_time" required/>
        </div>
        

        <div class="field-container">
            <label for="end_time">End Time</label>
            <input type="datetime-local" id="end_time" name="end_time" required/>
        </div>
        
        <input class="button bg-primary-700 text-white hover:bg-primary-800 p-2 rounded-lg" type="submit"/>
    </form>
    {#if error}
        <p style="color: red;">Error: {error}</p>
    {/if}
</Card>

<style>
    .form-container { 
        display: flex; 
        flex-direction: column;
        gap: 32px;
    }

    .field-container { 
        display: flex; 
        flex-direction: column;
        gap: 4px;
    }
</style>
