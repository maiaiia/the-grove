<script setup>
import BrandLogo from "@/components/BrandLogo.vue";
import BrandDescription from "@/components/BrandDescription.vue";
</script>

<template>
  <div class="auth-container">
    <div class="left-panel">
      <BrandLogo theme="dark"/>
      <BrandDescription theme="dark"/>
    </div>
    <div class="right-panel">
      <div class="corner-decoration top-left" />
      <div class="form-container">
        <div class="form-header">
          <p class="welcome-text"><slot name="eyebrow" /></p>
          <h1 class="main-heading"><slot name="title" /></h1>
          <p class="subtitle"><slot name="subtitle" /></p>
        </div>
        <slot name="form"/>
      </div>
      <div class="corner-decoration bottom-right" />
    </div>
  </div>
</template>

<style scoped>
* {
  font-family: var(--space-mono), monospace;
}
.form-container {
  width: 100%;
  max-width: 450px;
}

.form-header {
  margin-bottom: 40px;
}

.welcome-text {
  font-size: 14px;
  letter-spacing: 2px;
  color: var(--avocado);
  margin-bottom: 10px;
  font-weight: lighter;
  text-transform: uppercase;
}

.main-heading {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  color: var(--green-kelp);
  margin-bottom: 12px;
  font-family: 'Playfair Display', serif;
}

.subtitle {
  font-size: 14px;
  color: var(--avocado);
  font-weight: lighter;
  letter-spacing: 2px;
}

.form-group label {
  font-size: 11px;
  letter-spacing: 1.5px;
  color: var(--avocado);
  font-weight: 500;
  text-transform: uppercase;
}

.form-group input {
  padding: 12px 0;
  border: none;
  border-bottom: 1px solid var(--mongoose);
  background: transparent;
  font-size: 15px;
  color: var(--green-kelp);
  transition: border-color 0.3s;
}

.form-group input::placeholder {
  color: #b5a895;
}

.form-group input:focus {
  outline: none;
  border-bottom-color: var(--green-kelp);
}

.checkbox-label input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border: 1.5px solid var(--mongoose);
  background-color: transparent;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.checkbox-label input[type="checkbox"]:hover {
  border-color: var(--green-kelp);
}

.checkbox-label input[type="checkbox"]:checked {
  background-color: var(--green-kelp);
  border-color: var(--green-kelp);
}

.checkbox-label input[type="checkbox"]:checked::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid var(--cream);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.switch-mode a {
  color: var(--green-kelp);
  text-decoration: underline;
  cursor: pointer;
  font-weight: 500;
}

.switch-mode a:hover {
  color: var(--avocado);
}

.auth-container{
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}

.left-panel {
  background-color: var(--green-kelp);

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 5vh;
  padding: 0 2vw;
  position: relative;
}
.right-panel{
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
}
.corner-decoration {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 1px solid;
}

.corner-decoration.top-left {
  top: 20px;
  left: 20px;
  border-right: none;
  border-bottom: none;
  border-color: var(--mongoose);
}

.corner-decoration.bottom-right {
  bottom: 20px;
  right: 20px;
  border-left: none;
  border-top: none;
  border-color: var(--mongoose);
}
</style>