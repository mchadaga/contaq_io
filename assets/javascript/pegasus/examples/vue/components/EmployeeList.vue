<template>
  <section class="app-card">
    <h1 class="pg-subtitle">All Employees</h1>
    <div class="table-responsive">
      <table class="table pg-table">
        <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
          <th class="pg-text-right">Salary</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
          <employee-table-row v-for="employee in employees"
                              v-bind:key="employee.id"
                              v-bind:employee="employee"
                              v-bind:client="client"
                              v-on:delete-employee="deleteEmployee"
                              v-on:edit-employee="editEmployee"
          />
        </tbody>
      </table>
    </div>
    <button class="pg-button-primary" v-on:click="addEmployee" >
      <span class="icon is-small">
        <i class="fa fa-plus"></i>
      </span>
      <span>Add Employee</span>
    </button>
  </section>
</template>

<script>
import EmployeeTableRow from './EmployeeTableRow.vue'

export default {
  name: 'EmployeeList',
  components: {
    EmployeeTableRow
  },
  props: {
    employees: Array,
    client: Object,
  },
  methods: {
    addEmployee: function () {
      this.$emit('add-employee');
    },
    deleteEmployee: function (employee) {
      this.$emit('delete-employee', employee);
    },
    editEmployee: function (employee) {
      this.$emit('edit-employee', employee);
    },
  }
};
</script>
