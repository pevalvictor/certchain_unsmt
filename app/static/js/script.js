""// script.js

// ✅ Alternar visibilidad del sidebar (modo colapsado)
document.addEventListener('DOMContentLoaded', function () {
  const toggleSidebarBtn = document.getElementById('toggleSidebar');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('main-content');

  if (toggleSidebarBtn) {
    toggleSidebarBtn.addEventListener('click', function () {
      sidebar.classList.toggle('collapsed');
      mainContent.classList.toggle('expanded');
    });
  }

  // ✅ Cierre automático de alertas flash en 3 segundos
  const alertList = document.querySelectorAll('.alert-dismissible');
  alertList.forEach(function (alert) {
    setTimeout(function () {
      if (alert.classList.contains('show')) {
        alert.classList.remove('show');
        alert.classList.add('fade');
        alert.style.opacity = '0';
      }
    }, 3000);
  });
});
""

document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('toggleSidebar');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
    });
  }
});

function cargarEditar(id) {
  fetch(`/admin/obtener_curso/${id}`)
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      document.getElementById('edit-id').value = data.id;
      document.getElementById('edit-nombre').value = data.nombre;
      document.getElementById('edit-tipo').value = data.tipo;
      document.getElementById('edit-fecha-inicio').value = data.fecha_inicio;
      document.getElementById('edit-fecha-fin').value = data.fecha_fin;
      document.getElementById('edit-horas').value = data.duracion_horas;
      document.getElementById('edit-responsable').value = data.responsable_firma;
      document.getElementById('edit-cargo').value = data.cargo_responsable;
    });
}


<script>
  function cargarEditar(id) {
    fetch(`/admin/cursos/obtener/${id}`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("formEditarCurso").action = `/admin/cursos/editar/${id}`;
        document.getElementById("edit_nombre").value = data.nombre;
        document.getElementById("edit_tipo").value = data.tipo;
        document.getElementById("edit_fecha_inicio").value = data.fecha_inicio;
        document.getElementById("edit_fecha_fin").value = data.fecha_fin;
        document.getElementById("edit_horas").value = data.duracion_horas;
        document.getElementById("edit_responsable").value = data.responsable_firma;
        document.getElementById("edit_cargo").value = data.cargo_responsable;
      });
  }
</script>
