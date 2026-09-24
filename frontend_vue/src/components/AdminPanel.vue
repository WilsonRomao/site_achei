<template>
    <div class="card shadow-sm border-0 rounded-4 mb-4">

      <!-- CABEÇALHO / ABAS -->
      <div
        class="card-header bg-white border-bottom-0 pt-4 pb-0 d-flex justify-content-between align-items-end"
      >
        <ul class="nav nav-tabs border-bottom-0">

          <!-- USUÁRIOS -->
          <li class="nav-item">
            <button
              class="nav-link fw-bold border-0"
              :class="
                activeTab === 'usuarios'
                  ? 'text-dark border-bottom border-3 border-info'
                  : 'text-muted'
              "
              @click="activeTab = 'usuarios'"
            >
              <i class="bi bi-people me-2"></i>
              Gerenciar Usuários
            </button>
          </li>

          <!-- SOLICITAÇÕES -->
          <li class="nav-item">
            <button
              class="nav-link fw-bold border-0"
              :class="
                activeTab === 'solicitacoes'
                  ? 'text-dark border-bottom border-3 border-info'
                  : 'text-muted'
              "
              @click="activeTab = 'solicitacoes'"
            >
              <i class="bi bi-envelope-paper me-2"></i>
              Solicitações de Perfil
            </button>
          </li>

        </ul>

        <!-- CRIAR USUÁRIO -->
        <button
          v-if="activeTab === 'usuarios'"
          class="btn btn-sm btn-success mb-2"
          data-bs-toggle="modal"
          data-bs-target="#criarUsuarioModal"
        >
          <i class="bi bi-person-plus-fill me-1"></i>
          Criar Usuário
        </button>
      </div>


      <!-- CONTEÚDO -->
      <div class="card-body p-4 bg-light rounded-bottom-4">

        <!-- LOADING -->
        <div
          v-if="loading"
          class="text-center py-4"
        >
          <span class="spinner-border text-info"></span>
        </div>


        <!-- USUÁRIOS -->
        <div
          v-else-if="activeTab === 'usuarios'"
          class="table-responsive bg-white rounded-3 p-3"
        >
          <table class="table table-hover align-middle mb-0">

            <thead>
              <tr>
                <th>Email do Usuário</th>
                <th class="text-center">Padrão</th>
                <th class="text-center">Prescritor</th>
                <th class="text-center">Administrador</th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="usuario in usuarios"
                :key="usuario.id"
              >
                <td class="fw-bold text-secondary">
                  {{ usuario.email }}
                </td>

                <!-- PADRÃO -->
                <td class="text-center">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    :checked="usuario.perfis.includes('padrão')"
                    @change="togglePerfil(usuario, 'padrão')"
                  />
                </td>

                <!-- PRESCRITOR -->
                <td class="text-center">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    :checked="usuario.perfis.includes('prescritor')"
                    @change="togglePerfil(usuario, 'prescritor')"
                  />
                </td>

                <!-- ADMIN -->
                <td class="text-center">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    :checked="usuario.perfis.includes('administrador')"
                    :disabled="usuario.email === 'admin@achei.com'"
                    @change="togglePerfil(usuario, 'administrador')"
                  />
                </td>

              </tr>

            </tbody>
          </table>
        </div>


        <!-- SOLICITAÇÕES -->
        <div
          v-else
          class="table-responsive bg-white rounded-3 p-3"
        >
          <table class="table table-hover align-middle mb-0">

            <thead>
              <tr>
                <th>Data</th>
                <th>Usuário</th>
                <th>Perfil Solicitado</th>
                <th>Status</th>
                <th class="text-end">Ações</th>
              </tr>
            </thead>

            <tbody>

              <!-- SEM SOLICITAÇÕES -->
              <tr v-if="solicitacoes.length === 0">
                <td
                  colspan="5"
                  class="text-center py-3 text-muted"
                >
                  Nenhuma solicitação encontrada.
                </td>
              </tr>


              <!-- SOLICITAÇÕES -->
              <tr
                v-for="solicitacao in solicitacoes"
                v-else
                :key="solicitacao.id"
              >
                <td>
                  {{ solicitacao.data_solicitacao }}
                </td>

                <td class="fw-bold">
                  {{ solicitacao.email_usuario }}
                </td>

                <td>
                  <span class="badge bg-secondary">
                    {{ solicitacao.perfil_solicitado }}
                  </span>
                </td>

                <td>
                  <span
                    class="badge"
                    :class="statusClass(solicitacao.status)"
                  >
                    {{ solicitacao.status }}
                  </span>
                </td>

                <td class="text-end">

                  <template v-if="solicitacao.status === 'pendente'">

                    <button
                      class="btn btn-sm btn-success me-2"
                      @click="
                        processarSolicitacao(
                          solicitacao.id,
                          'aprovar'
                        )
                      "
                    >
                      <i class="bi bi-check-circle"></i>
                      Aprovar
                    </button>

                    <button
                      class="btn btn-sm btn-danger"
                      @click="
                        processarSolicitacao(
                          solicitacao.id,
                          'recusar'
                        )
                      "
                    >
                      <i class="bi bi-x-circle"></i>
                      Recusar
                    </button>

                  </template>

                </td>

              </tr>

            </tbody>
          </table>
        </div>

      </div>
    </div>


    <!-- ========================= -->
    <!-- MODAL CRIAR USUÁRIO -->
    <!-- ========================= -->

    <div
      id="criarUsuarioModal"
      class="modal fade"
      tabindex="-1"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">

        <div class="modal-content border-0 shadow rounded-4">

          <div class="modal-header border-bottom-0">

            <h5 class="modal-title fw-bold text-dark">
              Criar Novo Usuário
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>

          </div>


          <form @submit.prevent="handleCriarUsuario">

            <div class="modal-body py-2">

              <!-- EMAIL -->
              <div class="mb-3">

                <label
                  class="form-label text-muted small fw-bold"
                >
                  E-mail
                </label>

                <input
                  v-model="novoEmail"
                  type="email"
                  required
                  class="form-control"
                />

              </div>


              <!-- SENHA -->
              <div class="mb-3">

                <label
                  class="form-label text-muted small fw-bold"
                >
                  Senha
                </label>

                <input
                  v-model="novaSenha"
                  type="password"
                  required
                  class="form-control"
                />

              </div>


              <!-- PERFIS -->
              <div class="mb-3">

                <label
                  class="form-label text-muted small fw-bold"
                >
                  Perfis Iniciais
                </label>

                <div class="d-flex gap-3 mt-1">

                  <!-- PADRÃO -->
                  <div class="form-check">

                    <input
                      class="form-check-input"
                      type="checkbox"
                      :checked="novoPerfis.includes('padrão')"
                      @change="toggleNovoPerfil('padrão')"
                    />

                    <label class="form-check-label">
                      Padrão
                    </label>

                  </div>


                  <!-- PRESCRITOR -->
                  <div class="form-check">

                    <input
                      class="form-check-input"
                      type="checkbox"
                      :checked="novoPerfis.includes('prescritor')"
                      @change="toggleNovoPerfil('prescritor')"
                    />

                    <label class="form-check-label">
                      Prescritor
                    </label>

                  </div>


                  <!-- ADMIN -->
                  <div class="form-check">

                    <input
                      class="form-check-input"
                      type="checkbox"
                      :checked="novoPerfis.includes('administrador')"
                      @change="toggleNovoPerfil('administrador')"
                    />

                    <label class="form-check-label">
                      Admin
                    </label>

                  </div>

                </div>
              </div>

            </div>


            <!-- RODAPÉ MODAL -->
            <div class="modal-footer border-top-0 pt-0">

              <button
                type="button"
                class="btn btn-light rounded-pill px-4"
                data-bs-dismiss="modal"
              >
                Cancelar
              </button>

              <button
                type="submit"
                class="btn btn-success rounded-pill px-4"
                :disabled="criandoUser"
              >
                {{ criandoUser ? 'Criando...' : 'Salvar Usuário' }}
              </button>

            </div>

          </form>

        </div>
      </div>
    </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import { apiService } from '../services/api'


// ==========================
// ESTADO
// ==========================

const activeTab = ref('usuarios')

const usuarios = ref([])
const solicitacoes = ref([])

const loading = ref(false)


// ==========================
// NOVO USUÁRIO
// ==========================

const novoEmail = ref('')
const novaSenha = ref('')

const novoPerfis = ref([
  'padrão'
])

const criandoUser = ref(false)


// ==========================
// CARREGAR DADOS
// ==========================

const carregarDados = async () => {

  loading.value = true

  try {

    if (activeTab.value === 'usuarios') {

      const data =
        await apiService.getUsuarios()

      usuarios.value = data

    } else {

      const data =
        await apiService.getSolicitacoes()

      solicitacoes.value = data

    }

  } catch (error) {

    console.error(error)

  } finally {

    loading.value = false

  }
}


// Carrega ao abrir componente
onMounted(() => {
  carregarDados()
})


// Recarrega ao trocar de aba
watch(activeTab, () => {
  carregarDados()
})


// ==========================
// ALTERAR PERFIL
// ==========================

const togglePerfil = async (
  usuario,
  perfil
) => {

  try {

    const temPerfil =
      usuario.perfis.includes(perfil)

    let novosPerfis = [
      ...usuario.perfis
    ]

    if (temPerfil) {

      novosPerfis =
        novosPerfis.filter(
          p => p !== perfil
        )

    } else {

      novosPerfis.push(perfil)

    }


    await apiService.setUsuarioPerfis(
      usuario.id,
      novosPerfis
    )


    await carregarDados()

  } catch (error) {

    alert(error.message)

  }
}


// ==========================
// PROCESSAR SOLICITAÇÃO
// ==========================

const processarSolicitacao = async (
  id,
  acao
) => {

  try {

    await apiService.processarSolicitacao(
      id,
      acao
    )

    await carregarDados()

    alert(
      `Solicitação ${
        acao === 'aprovar'
          ? 'Aprovada'
          : 'Recusada'
      }!`
    )

  } catch (error) {

    alert(error.message)

  }
}


// ==========================
// CRIAR USUÁRIO
// ==========================

const handleCriarUsuario = async () => {

  criandoUser.value = true

  try {

    await apiService.criarUsuario(
      novoEmail.value,
      novaSenha.value,
      novoPerfis.value
    )


    alert(
      'Usuário criado com sucesso!'
    )


    // Limpa formulário
    novoEmail.value = ''
    novaSenha.value = ''

    novoPerfis.value = [
      'padrão'
    ]


    await carregarDados()


    // Fecha modal
    const modal =
      document.getElementById(
        'criarUsuarioModal'
      )

    const bootstrapModal =
      window.bootstrap.Modal.getInstance(
        modal
      )

    if (bootstrapModal) {
      bootstrapModal.hide()
    }

  } catch (error) {

    alert(error.message)

  } finally {

    criandoUser.value = false

  }
}


// ==========================
// PERFIS DO NOVO USUÁRIO
// ==========================

const toggleNovoPerfil = (perfil) => {

  if (
    novoPerfis.value.includes(perfil)
  ) {

    novoPerfis.value =
      novoPerfis.value.filter(
        p => p !== perfil
      )

  } else {

    novoPerfis.value = [
      ...novoPerfis.value,
      perfil
    ]

  }
}


// ==========================
// COR DO STATUS
// ==========================

const statusClass = (status) => {

  if (status === 'pendente') {
    return 'bg-warning text-dark'
  }

  if (status === 'aprovado') {
    return 'bg-success'
  }

  return 'bg-danger'
}
</script>