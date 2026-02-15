<template>
  <div class="skeleton-loader">
    <div v-if="type === 'card'" class="skeleton-card">
      <div class="skeleton-image"></div>
      <div class="skeleton-content">
        <div class="skeleton-line skeleton-title"></div>
        <div class="skeleton-line skeleton-text"></div>
        <div class="skeleton-line skeleton-text short"></div>
      </div>
    </div>

    <div v-else-if="type === 'list'" class="skeleton-list">
      <div v-for="i in count" :key="i" class="skeleton-list-item">
        <div class="skeleton-avatar"></div>
        <div class="skeleton-lines">
          <div class="skeleton-line"></div>
          <div class="skeleton-line short"></div>
        </div>
      </div>
    </div>

    <div v-else-if="type === 'text'" class="skeleton-text-block">
      <div class="skeleton-line" v-for="i in count" :key="i"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonLoader',
  props: {
    type: {
      type: String,
      default: 'card',
      validator: (value) => ['card', 'list', 'text'].includes(value)
    },
    count: {
      type: Number,
      default: 3
    }
  }
}
</script>

<style scoped>
.skeleton-loader {
  width: 100%;
}

/* Shimmer animation */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton-card,
.skeleton-list-item,
.skeleton-line,
.skeleton-image,
.skeleton-avatar {
  background: linear-gradient(
    90deg,
    var(--surface-2, #f3f4f6) 0%,
    var(--border-color, #e5e7eb) 50%,
    var(--surface-2, #f3f4f6) 100%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite linear;
}

/* Card Skeleton */
.skeleton-card {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.skeleton-image {
  height: 200px;
  width: 100%;
}

.skeleton-content {
  padding: 1.5rem;
}

.skeleton-line {
  height: 12px;
  border-radius: 6px;
  margin-bottom: 0.75rem;
}

.skeleton-title {
  height: 20px;
  width: 70%;
  margin-bottom: 1rem;
}

.skeleton-text {
  width: 100%;
}

.skeleton-text.short {
  width: 60%;
}

/* List Skeleton */
.skeleton-list-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  flex-shrink: 0;
}

.skeleton-lines {
  flex: 1;
}

.skeleton-lines .skeleton-line {
  height: 12px;
  margin-bottom: 0.5rem;
}

.skeleton-lines .skeleton-line:last-child {
  margin-bottom: 0;
}

.skeleton-lines .short {
  width: 70%;
}

/* Text Block Skeleton */
.skeleton-text-block .skeleton-line {
  height: 14px;
  margin-bottom: 0.5rem;
}

.skeleton-text-block .skeleton-line:nth-child(even) {
  width: 85%;
}
</style>
