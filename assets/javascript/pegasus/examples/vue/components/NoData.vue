<template>
  <section class="app-card">
    <div class="pg-columns">
        <div class="pg-column-one-third">
            <img class="img-fluid" alt="Nothing Here" :src="staticFiles.undraw_empty"/>
        </div>
        <div class="pg-column">
            <h1 class="pg-title">No Employees Yet!</h1>
            <h2 class="pg-subtitle">Create your first employee below to get started.</h2>
            <p>
                <a class="pg-button-primary my-3" v-on:click="$emit('add-employee')">
                    <span class="icon is-small"><i class="fa fa-plus"></i></span>
                    <span>Create Employee</span>
                </a>
            </p>
        </div>
    </div>
</section>
</template>

<script>
export default {
  name: 'NoData',
  props: {
    static_files: Object
  },
}

</script>
