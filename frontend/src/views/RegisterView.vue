<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthLayout from "@/components/AuthLayout.vue";

const router = useRouter();
const name = ref('');
const email = ref('');
const password = ref('');

const handleRegister = () => {
  console.log('Registering...', { name: name.value, email: email.value, password: password.value });
  router.push('/');
};

const goToSignIn = () => {
  router.push('/sign-in');
};
</script>

<template>
  <AuthLayout>
    <template #eyebrow> Join Us</template>
    <template #title>Create<br>your garden.</template>
    <template #subtitle>Your plants are waiting.</template>
    <template #form>
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="name">NAME</label>
          <input
              type="text"
              id="name"
              v-model="name"
              placeholder="Your name"
              required
          />
        </div>

        <div class="form-group">
          <label for="email">EMAIL ADDRESS</label>
          <input
              type="email"
              id="email"
              v-model="email"
              placeholder="you@grove.com"
              required
          />
        </div>

        <div class="form-group">
          <label for="password">PASSWORD</label>
          <input
              type="password"
              id="password"
              v-model="password"
              placeholder="••••••••••••"
              required
          />
        </div>

        <button type="submit" class="submit-btn">
          JOIN THE GROVE
        </button>

        <div class="divider">
          <span>OR</span>
        </div>

        <p class="switch-mode">
          Already a member? <a @click.prevent="goToSignIn" href="#">Login to your garden</a>
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

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
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