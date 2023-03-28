<script lang="ts">
    import type { PageData } from "./$types"


    export let data: PageData
</script>

<div class="bg-slate-200 min-h-screen flow-root">
    <div class="bg-white rounded max-w-6xl mx-auto my-4 p-2">
        <h1 class="text-3xl font-semibold">{data.item.name}</h1>
        {#if data.sparePartsData && data.sparePartsData.length > 0}
            <ul>
                {#each data.sparePartsData as sparePart}
                    <a class="text-lg underline" href={`/details/${sparePart.code}`}><li>{sparePart.code} | {sparePart.name}</li></a>
                {/each}
            </ul>
        {:else}
            No spare parts for this item.
        {/if}
    </div>
</div>
