<template>
  <div class="skeleton-card">
    <div class="skeleton skeleton-image"></div>
    <div class="skeleton-content">
      <div class="skeleton skeleton-title"></div>
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-text short"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonCard'
}
</script>

<style scoped>
.skeleton-card {
  background: var(--surface);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.skeleton-image {
  width: 100%;
  height: 200px;
}

.skeleton-content {
  padding: 1.5rem;
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--surface-2) 25%,
    var(--gray-light) 50%,
    var(--surface-2) 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.skeleton-title {
  height: 24px;
  width: 70%;
  margin-bottom: 1rem;
}

.skeleton-text {
  height: 16px;
  width: 100%;
  margin-bottom: 0.75rem;
}

.skeleton-text.short {
  width: 60%;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
