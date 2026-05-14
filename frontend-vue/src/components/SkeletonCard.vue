<template>
  <div class="news-card">
    <div class="skeleton skeleton-title"></div>
    <div class="skeleton skeleton-text"></div>
    <div class="skeleton skeleton-text"></div>
    <div class="skeleton skeleton-text" style="width: 60%"></div>
    <div class="card-actions">
      <div class="skeleton skeleton-btn"></div>
      <div class="skeleton" style="width: 24px; height: 24px; border-radius: 50%"></div>
    </div>
  </div>
</template>

<style scoped>
@keyframes shimmer {
  0% { background-position: -468px 0; }
  100% { background-position: 468px 0; }
}

.skeleton {
  background: #1e293b;
  background-image: linear-gradient(
    90deg,
    #1e293b 0px,
    #334155 40px,
    #1e293b 80px
  );
  background-size: 800px 100%;
  background-repeat: no-repeat;
  display: inline-block;
  line-height: 1;
  width: 100%;
  animation: shimmer 1.5s infinite linear;
  border-radius: 4px;
}

.skeleton-title {
  height: 24px;
  margin-bottom: 10px;
  width: 80%; 
}

.skeleton-text { 
  height: 18px; 
  margin-bottom: 12px; 
  width: 100%; 
}

.skeleton-btn { 
  height: 30px; 
  width: 100px; 
  border-radius: 6px; 
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}
</style>