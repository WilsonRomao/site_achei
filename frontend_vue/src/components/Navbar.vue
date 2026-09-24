<template>
  <nav
    class="navbar navbar-expand-lg"
    style="background-color: var(--achei-teal)"
  >
    <div class="container">
      <!-- Logo -->
      <a class="navbar-brand text-white fw-bold" href="#">
        <i class="bi bi-search me-2"></i>
        Achei!
      </a>

      <!-- Botão mobile -->
      <button
        class="navbar-toggler border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div
        id="navbarNav"
        class="collapse navbar-collapse justify-content-end"
      >
        <ul class="navbar-nav align-items-center">

          <li class="nav-item">
            <a class="nav-link text-white" href="#">
              Consulta
            </a>
          </li>

          <!-- Prescritores -->
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle text-white"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
            >
              Prescritores
            </a>

            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <a class="dropdown-item" href="#">
                  Área Restrita
                </a>
              </li>
            </ul>
          </li>

          <li class="nav-item ms-lg-3">
            <i class="bi bi-search text-white fw-bold"></i>
          </li>

          <!-- Usuário -->
          <li
            v-if="user"
            class="nav-item dropdown ms-lg-4 mt-2 mt-lg-0"
          >
            <button
              class="btn btn-sm btn-outline-light rounded-pill px-3 dropdown-toggle"
              data-bs-toggle="dropdown"
            >
              <i class="bi bi-person-circle me-1"></i>

              {{ nomeUsuario }}
            </button>

            <ul
              class="dropdown-menu dropdown-menu-end shadow border-0 p-3"
              style="min-width: 250px"
            >
              <li class="mb-2">
                <span class="text-muted small fw-bold text-uppercase">
                  Meus Perfis
                </span>

                <div class="d-flex flex-wrap gap-1 mt-1">
                  <span
                    v-for="perfil in user.perfis"
                    :key="perfil"
                    class="badge bg-info text-dark"
                  >
                    {{ perfil }}
                  </span>
                </div>
              </li>

              <li>
                <hr class="dropdown-divider" />
              </li>

              <!-- Solicitar perfil -->
              <li>
                <button
                  class="dropdown-item text-primary"
                  data-bs-toggle="modal"
                  data-bs-target="#solicitarPerfilModal"
                >
                  <i class="bi bi-person-plus me-2"></i>

                  Solicitar Novo Perfil
                </button>
              </li>

              <!-- Logout -->
              <li>
                <button
                  class="dropdown-item text-danger"
                  @click="emit('logout')"
                >
                  <i class="bi bi-box-arrow-right me-2"></i>

                  Sair do Sistema
                </button>
              </li>
            </ul>
          </li>

        </ul>
      </div>
    </div>
  </nav>


  <!-- ========================= -->
  <!-- MODAL SOLICITAR PERFIL -->
  <!-- ========================= -->

  <div
    id="solicitarPerfilModal"
    class="modal fade"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4">

        <div class="modal-header border-bottom-0">

          <h5 class="modal-title fw-bold text-dark">
            <i class="bi bi-shield-lock text-info me-2"></i>

            Solicitar Acesso
          </h5>

          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>

        </div>


        <div class="modal-body py-2">

          <p class="text-muted small">
            Selecione o nível de permissão que você deseja
            solicitar ao Administrador do sistema:
          </p>

          <select
            v-model="perfilSelecionado"
            class="form-select form-select-lg bg-light"
          >
            <option value="prescritor">
              Prescritor
            </option>

            <option value="administrador">
              Administrador
            </option>
          </select>

        </div>


        <div class="modal-footer border-top-0 pt-0">

          <button
            type="button"
            class="btn btn-light rounded-pill px-4"
            data-bs-dismiss="modal"
          >
            Cancelar
          </button>


          <button
            type="button"
            class="btn text-white rounded-pill px-4 fw-bold"
            style="background-color: var(--achei-teal)"
            :disabled="loading"
            @click="handleSolicitar"
          >
            {{ loading ? 'Enviando...' : 'Enviar Solicitação' }}
          </button>

        </div>

      </div>
    </div>
  </div>
</template>


<script setup>
import { computed, ref } from 'vue'
import { apiService } from '../services/api'


// ==========================
// PROPS
// ==========================

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})


// ==========================
// EVENTOS
// ==========================

const emit = defineEmits(['logout'])


// ==========================
// ESTADO
// ==========================

const perfilSelecionado = ref('prescritor')

const loading = ref(false)


// ==========================
// NOME DO USUÁRIO
// ==========================

const nomeUsuario = computed(() => {
  return props.user.email.split('@')[0]
})


// ==========================
// SOLICITAR PERFIL
// ==========================

const handleSolicitar = async () => {

  loading.value = true

  try {

    const res = await apiService.solicitarPerfil(
      perfilSelecionado.value
    )

    alert(res.message)


    // Fecha o modal Bootstrap
    const modal = document.getElementById(
      'solicitarPerfilModal'
    )

    const bootstrapModal =
      window.bootstrap.Modal.getInstance(modal)

    if (bootstrapModal) {
      bootstrapModal.hide()
    }

  } catch (error) {

    alert(error.message)

  } finally {

    loading.value = false

  }
}
</script>