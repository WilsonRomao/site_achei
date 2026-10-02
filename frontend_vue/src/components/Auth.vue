<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div
      class="card shadow-sm border-0 p-4 rounded-4"
      style="width: 100%; max-width: 400px"
    >
      <div class="text-center mb-4">
        <i
          class="bi bi-shield-lock text-primary"
          style="
            font-size: 3rem;
            color: var(--achei-teal) !important;
          "
        ></i>

        <h3 class="fw-bold text-dark mt-2">
          {{ isLogin ? 'Acesso Restrito' : 'Novo Cadastro' }}
        </h3>

        <p class="text-muted small">
          {{
            isLogin
              ? 'Faça login para consultar o estoque das UBS'
              : 'Cadastre-se para acessar o sistema'
          }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <input
            v-model="email"
            type="email"
            class="form-control form-control-lg bg-light border-0"
            placeholder="Seu e-mail"
            required
          />
        </div>

        <div class="mb-3">
          <input
            v-model="senha"
            type="password"
            class="form-control form-control-lg bg-light border-0"
            placeholder="Sua senha"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-lg w-100 text-white fw-bold rounded-pill shadow-sm"
          style="background-color: var(--achei-teal)"
          :disabled="loading"
        >
          {{
            loading
              ? 'Aguarde...'
              : isLogin
                ? 'Entrar no Achei!'
                : 'Criar minha conta'
          }}
        </button>
      </form>

      <div class="text-center mt-4">
        <button
          type="button"
          class="btn btn-link text-decoration-none text-secondary"
          @click="alternarModo"
        >
          {{
            isLogin
              ? 'Ainda não tem conta? Clique aqui'
              : 'Já possui conta? Voltar ao Login'
          }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiService } from '../services/api'

const emit = defineEmits(['login'])

const isLogin = ref(true)
const email = ref('')
const senha = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true

  try {
    if (isLogin.value) {
      const data = await apiService.login(
        email.value,
        senha.value
      )

      emit('login', data.usuario)
    } else {
      await apiService.register(
        email.value,
        senha.value
      )

      alert(
        'Cadastro realizado! O seu usuário Padrão foi criado. Faça o login.'
      )

      isLogin.value = true
      senha.value = ''
    }
  } catch (error) {
    alert(error.message)
  } finally {
    loading.value = false
  }
}

const alternarModo = () => {
  isLogin.value = !isLogin.value
}
</script>
