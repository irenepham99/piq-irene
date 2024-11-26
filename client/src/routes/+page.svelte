<script lang="ts">
	import Form from './Form.svelte';
    import { goto } from '$app/navigation';
	
    let error : string | null = null; 
	let loading: boolean = false;

    async function runStudy(data : Object)  { 
		let response
        try {
			loading = true;
			error = null;
            response = await fetch("http://127.0.0.1:8000/studies", {
                method: "POST", 
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error(`Error running study ${response.status}`);
            }
            let responseData = await response.json(); 
			console.log(responseData, "POST REQUEST DATA")

            if (responseData && responseData.id) {
                console.log("ID", responseData.id)
                goto(`/study/${responseData.id}`);
            } else {
                throw new Error("Invalid response: 'id' not found");
            }
        } catch (err) {
            error = "Something went wrong when running the study. Try again later."
			if (err && err.message) {
                error += `: ${err.message}`;
            }
            console.log(err)
        } finally { 
			loading = false;
		}
    }
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	{#if loading}
		<h2>Running Your Study - Hang On!...</h2>
	{:else}
		<h1>
			Run A Study!
		</h1>
		<Form {runStudy}/>
		{#if error}
			<h3 style="color: red;">Error: {error}</h3>
		{/if}
	{/if}
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
		gap: 32px; 
	}

	h1 {
		width: 100%;
	}

</style>
