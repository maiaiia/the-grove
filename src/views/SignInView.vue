<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthLayout from "@/components/AuthLayout.vue";

const router = useRouter();
const email = ref('');
const password = ref('');
const rememberMe = ref(false);

const handleSignIn = () => {
  console.log('Signing in...', { email: email.value, password: password.value });
  router.push('/');
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<template>
  <AuthLayout>
    <template #eyebrow> Welcome Back</template>
    <template #title>Login to<br>your garden.</template>
    <template #subtitle>Your plants have been waiting.</template>
    <template #form>
      <form @submit.prevent="handleSignIn" class="auth-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
              type="email"
              id="email"
              v-model="email"
              placeholder="you@grove.com"
              required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
              type="password"
              id="password"
              v-model="password"
              placeholder="••••••••••••"
              required
          />
        </div>

        <div class="form-row">
          <label class="checkbox-label">
            <input type="checkbox" v-model="rememberMe" />
            <span>Remember me</span>
          </label>
          <a href="#" class="forgot-link">Forgot password?</a>
        </div>

        <button type="submit" class="submit-btn">
          Enter the grove
        </button>

        <div class="divider">
          <span>OR</span>
        </div>

        <p class="switch-mode">
          New here? <a @click.prevent="goToRegister" href="#">Join the community</a>
        </p>
      </form>
    </template>
  </AuthLayout>
</template>

<style scoped>
* {
  font-family: var(--space-mono), monospace;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

.form-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-family: monospace;
  color: var(--avocado);
  cursor: pointer;
  user-select: none;
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

.checkbox-label:hover {
  color: var(--green-kelp);
}

.forgot-link {
  font-size: 13px;
  color: var(--avocado);
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-link:hover {
  color: var(--green-kelp);
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: var(--green-kelp);
  color: var(--cream);
  border: none;
  font-size: 12px;
  letter-spacing: 2px;
  font-weight: 400;
  cursor: pointer;
  transition: background-color 0.3s;
  text-transform: uppercase;
}

.submit-btn:hover {
  background-color: var(--avocado);
}

.divider {
  text-align: center;
  position: relative;
  margin: 8px 0;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 45%;
  height: 1px;
  background-color: var(--mongoose);
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background-color: var(--color-background);
  padding: 0 12px;
  font-size: 12px;
  color: var(--mongoose);
}

.switch-mode {
  text-align: center;
  font-size: 14px;
  color: var(--mongoose);
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
</style>