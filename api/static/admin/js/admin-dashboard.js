document.addEventListener("DOMContentLoaded", function () {
  const activitySelects = document.querySelectorAll("select[data-dependent='categories']");
  const categorySelects = document.querySelectorAll("select[data-dependent='subcategories']");
  const activityFields = document.querySelectorAll("[data-activity-display='true']");

  function fetchOptions(url, target) {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        target.innerHTML = "<option value=''>Select</option>";
        if (Array.isArray(data)) {
          data.forEach((item) => {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.name;
            target.appendChild(option);
          });
        }
      })
      .catch((error) => {
        console.error("Admin select fetch failed", error);
      });
  }

  activitySelects.forEach((activitySelect) => {
    activitySelect.addEventListener("change", function () {
      const categoryTarget = document.querySelector(
        `select[data-parent='${activitySelect.id}']`
      );
      if (!categoryTarget) return;
      const activityId = activitySelect.value;
      if (!activityId) {
        categoryTarget.innerHTML = "<option value=''>Select</option>";
        return;
      }
      fetchOptions(`/api/get-categories/${activityId}`, categoryTarget);
    });
  });

  categorySelects.forEach((categorySelect) => {
    categorySelect.addEventListener("change", function () {
      const activityId = document.querySelector("select[data-dependent='categories']")?.value;
      const subcategoryTarget = document.querySelector(
        `select[data-parent='${categorySelect.id}']`
      );
      if (!subcategoryTarget || !activityId) return;
      const categoryId = categorySelect.value;
      if (!categoryId) {
        subcategoryTarget.innerHTML = "<option value=''>Select</option>";
        return;
      }
      fetchOptions(
        `/api/get-subcategories/activity/${activityId}/category/${categoryId}`,
        subcategoryTarget
      );
    });
  });

  const projectSelect = document.getElementById("id_project");
  const activityDisplay = document.querySelector("[data-activity-display='true']");
  const activityHidden = document.getElementById("id_activity");

  if (projectSelect && activityDisplay && activityHidden) {
    projectSelect.addEventListener("change", function () {
      const projectId = projectSelect.value;
      if (!projectId) {
        activityDisplay.textContent = "None";
        activityHidden.value = "";
        return;
      }
      fetch(`/api/get-project/${projectId}`)
        .then((res) => res.json())
        .then((data) => {
          activityDisplay.textContent = data.subcategory ? data.subcategory.activity.name || "" : "";
          activityHidden.value = data.subcategory ? data.subcategory.activity || "" : "";
        })
        .catch(() => {
          activityDisplay.textContent = "Unable to load activity";
        });
    });
  }
});
