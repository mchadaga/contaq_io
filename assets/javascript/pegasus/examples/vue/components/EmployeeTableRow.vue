<template>
  <tr>
    <td>{{ employee.name }}</td>
    <td>{{ employee.department }}</td>
    <td class="pg-text-right">{{ formattedSalary }}</td>
    <td class="pg-inline-buttons pg-justify-content-end">
      <a class="pg-button-secondary" v-on:click="editEmployee">
        <span class="icon is-small"><i class="fa fa-edit" /></span>
        <span class="pg-hidden-mobile-inline">Edit</span>
      </a>
      <a class="pg-button-danger pg-ml" v-on:click="deleteEmployee">
        <span class="icon is-small"><i class="fa fa-times" /></span>
        <span class="pg-hidden-mobile-inline">Delete</span>
      </a>
    </td>
  </tr>
</template>

<script>

export default {
  name: 'EmployeeTableRow',
  props: {
    employee: Object,
    client: Object,
  },
  computed: {
    formattedSalary: function () {
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      return formatter.format(this.employee.salary);
    }
  },
  methods: {
    editEmployee: function () {
      this.$emit('edit-employee', this.employee);
    },
    deleteEmployee: function () {
      this.$emit('delete-employee', this.employee);
    },
  }
};
</script>

<style scoped>
</style>
