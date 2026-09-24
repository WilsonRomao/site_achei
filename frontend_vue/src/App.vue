<template>
  <!-- Se não estiver logado -->
  <Auth
    v-if="!user"
    @login="handleLogin"
  />

  <!-- Se estiver logado -->
  <div
    v-else
    class="app-wrapper bg-light min-vh-100"
  >
    <Navbar
      :user="user"
      @logout="handleLogout"
    />

    <Hero />

    <main class="container pb-5">
      <Mapa />

      <!-- Área exclusiva do administrador -->
      <div
        v-if="user.perfis.includes('administrador')"
        class="mt-4"
      >
        <Upload @success="handleUploadSuccess" />

        <div class="mt-4">
          <AdminPanel />
        </div>
      </div>

      <MedicamentoList
        :medicamentos="medicamentos"
        :lista-estabelecimentos="listaEstabelecimentos"
        :filtros="filtros"
        :page="page"
        :total-pages="totalPages"
        :loading="loading"
        @filter-change="handleFilterChange"
        @update:page="page = $event"
      />
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'

import Auth from './components/Auth.vue'
import Navbar from './components/Navbar.vue'
import Hero from './components/Hero.vue'
import Mapa from './components/Mapa.vue'
import Upload from './components/Upload.vue'
import AdminPanel from './components/AdminPanel.vue'
import MedicamentoList from './components/MedicamentoList.vue'

import { apiService } from './services/api'

import './App.css'


// ==========================
// USUÁRIO
// ==========================

const user = ref(null)


// ==========================
// MEDICAMENTOS
// ==========================

const medicamentos = ref([])

const listaEstabelecimentos = ref([])

const loading = ref(false)

const page = ref(1)

const totalPages = ref(1)


// ==========================
// FILTROS
// ==========================

const filtros = reactive({
  q: '',
  catmat: '',
  estabelecimento: ''
})


// ==========================
// LOGIN SALVO
// ==========================

onMounted(() => {
  const savedUser = localStorage.getItem('usuario')

  if (savedUser) {
    const parsedUser = JSON.parse(savedUser)

    // Proteção contra versão antiga
    // anterior aos múltiplos perfis
    if (!parsedUser.perfis) {
      localStorage.removeItem('usuario')
      localStorage.removeItem('token')

      window.location.reload()
      return
    }

    user.value = parsedUser
  }
})


// ==========================
// CARREGAR ESTABELECIMENTOS
// ==========================

const carregarEstabelecimentos = async () => {
  if (!user.value) return

  try {
    const dados = await apiService.getEstabelecimentos()

    listaEstabelecimentos.value = dados
  } catch (error) {
    console.error('Erro ao carregar estabelecimentos:', error)
  }
}


// ==========================
// CARREGAR MEDICAMENTOS
// ==========================

const fetchMedicamentos = async () => {
  if (!user.value) return

  loading.value = true

  try {
    const data = await apiService.getMedicamentos({
      page: page.value,
      q: filtros.q,
      catmat: filtros.catmat,
      estabelecimento: filtros.estabelecimento
    })

    medicamentos.value = data.items || []

    totalPages.value = data.pages || 1
  } catch (error) {
    console.error('Erro ao carregar medicamentos:', error)
  } finally {
    loading.value = false
  }
}


// ==========================
// LOGIN
// ==========================

const handleLogin = (usuario) => {
  user.value = usuario
}


// ==========================
// LOGOUT
// ==========================

const handleLogout = () => {
  apiService.logout()

  user.value = null

  medicamentos.value = []

  listaEstabelecimentos.value = []
}


// ==========================
// ALTERAÇÃO DOS FILTROS
// ==========================

const handleFilterChange = (novoFiltro) => {
  Object.assign(filtros, novoFiltro)

  page.value = 1
}


// ==========================
// UPLOAD CONCLUÍDO
// ==========================

const handleUploadSuccess = () => {
  fetchMedicamentos()
}


// ==========================
// OBSERVADORES
// ==========================

// Quando usuário logar
watch(user, async (novoUsuario) => {
  if (!novoUsuario) return

  await carregarEstabelecimentos()

  await fetchMedicamentos()
})


// Quando mudar página ou filtro
watch(
  [
    page,
    () => filtros.q,
    () => filtros.catmat,
    () => filtros.estabelecimento
  ],
  () => {
    fetchMedicamentos()
  }
)
</script>
