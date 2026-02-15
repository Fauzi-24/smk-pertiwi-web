<template>
  <nav class="breadcrumbs">
    <router-link to="/" class="breadcrumb-item">
      <i class="fas fa-home"></i>
      Home
    </router-link>
    <span v-for="(crumb, index) in crumbs" :key="index" class="breadcrumb-item">
      <i class="fas fa-chevron-right separator"></i>
      <router-link v-if="crumb.to" :to="crumb.to">
        {{ crumb.text }}
      </router-link>
      <span v-else class="active">{{ crumb.text }}</span>
    </span>
  </nav>
</template>

<script>
export default {
  name: 'Breadcrumbs',
  props: {
    crumbs: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.breadcrumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 1rem 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb-item a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb-item a:hover {
  color: var(--primary-color);
}

.breadcrumb-item .active {
  color: var(--text-primary);
  font-weight: 600;
}

.separator {
  font-size: 0.7rem;
  color: var(--text-secondary);
  opacity: 0.5;
}

.breadcrumb-item i.fa-home {
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .breadcrumbs {
    font-size: 0.85rem;
  }
}
</style>
