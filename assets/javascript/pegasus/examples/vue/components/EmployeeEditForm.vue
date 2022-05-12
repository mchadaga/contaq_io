<template>
  <section class="app-card">
    <form>
      <h2 class="pg-subtitle">Employee Details</h2>
      <div class="pg-input-group">
        <label class="pg-label">Name</label>
        <input class="pg-control" type="text" placeholder="Michael Scott" v-model="name">
        <p class="pg-help">Your employee's name.</p>
      </div>
      <div class="mb-3">
        <label class="pg-label">Department</label>
        <div class="pg-select">
          <select v-model="department">
            <option v-for="option in departmentOptions" v-bind:value="option.id">
              {{ option.name }}
            </option>
          </select>
        </div>
        <p class="pg-help">What department your employee belongs to.</p></div>
      <div class="pg-input-group">
        <label class="pg-label">Salary</label>
        <input class="pg-control" type="number" min="0" placeholder="50000" v-model="salary">
        <p class="pg-help">Your employee's annual salary.</p></div>
      <div class="pg-inline-buttons">
        <button class="pg-button-primary" v-on:click.prevent="saveEdit">
          <span class="icon is-small"><i :class="getSaveIconClass"></i></span>
          <span>{{ getSaveIconText }}</span>
        </button>
        <button class="pg-button-light mx-2" v-on:click.prevent="$emit('cancel-edit')">
          <span>Cancel</span>
        </button>
      </div>
    </form>
  </section>
</template>

<script>
export default {
  name: 'EmployeeEditForm',
  components: {},
  data() {
    if (this.employee) {
      return {
        id: this.employee.id,
        name: this.employee.name,
        department: this.employee.department,
        salary: this.employee.salary,
      };
    } else {
      return {
        id: null,
        name: "",
        department: "",
        salary: null,
      };
    }

  },
  props: {
    // initialName: String,
    // initialDepartment: String,
    // initialSalary: Number,
    employee: Object,
    client: Object,
    departmentOptions: Array,
  },
  computed: {
    getSaveIconClass: function () {
      return `fa ${this.employee === null  ? 'fa-plus' : 'fa-check'}`;
    },
    getSaveIconText: function () {
      return `${this.employee === null  ? 'Add' : 'Save'} Employee`;
    },
  },
  methods: {
    saveEdit: function () {
      // pass all data back through the event
      this.$emit('save-edit', this.$data);
    }
  }
};
</script>
