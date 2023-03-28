<script lang="ts">
    import type { PageData } from "./$types"


    export let data: PageData
</script>

<div class="bg-slate-200 min-h-screen flow-root">
    <div class="bg-white rounded max-w-6xl mx-auto my-4 p-2">
        <div class="flex flex-col items-center mb-4">
            <h1 class="text-3xl font-semibold">Items {data.page * 10 + 1} - {(data.page + 1) * 10} out of {data.items_count}</h1>
        </div>

        <ul>
            {#each data.items as item}
                <li>
                    <a class="text-lg underline" href={`/details/${item.code}`}><div>{item.name}</div></a>
                </li>
            {/each}
        </ul>

        <nav class="font-bold text-2xl mt-4 flex flex-row justify-between">
            <div>
                {#if data.page > 0}
                    <a href={`/items/${data.page - 1}`}>Previous</a>
                {/if}
            </div>
            <div>
                {#if data.page < Math.floor(data.items_count / 10)}
                    <a href={`/items/${data.page + 1}`}>Next</a>
                {/if}
            </div>
        </nav>
    </div>
</div>
