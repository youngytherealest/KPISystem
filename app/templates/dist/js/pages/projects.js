var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

let bangdsdetai = $("#bangdsdetai").DataTable({
  paging: true,
  lengthChange: false,
  searching: true,
  ordering: true,
  info: true,
  autoWidth: false,
  responsive: true,
  ajax: {
    type: "GET",
    url: "get_all_de_tai",
    dataSrc: "",
  },
  columns: [
    { data: "id" },
    { data: "ten" },
    { data: "mota" },
    {
      data: "xoa",
      render: function (data, type, row) {
        if (data == 0) {
          return '<span class="badge badge-success"><i class="fa-solid fa-check"></i> Đang sử dụng</span>';
        } else {
          return '<span class="badge badge-danger"><i class="fa-solid fa-xmark"></i> Ngưng sử dụng</span>';
        }
      },
    },
    {
      data: "id",
      render: function (data, type, row) {
        return (
          '<a class="btn btn-info btn-sm" id="editBtn" data-id="' +
          data +
          '"><i class="fas fa-pencil-alt"></i></a>  <a class="btn btn-danger btn-sm" data-id="' +
          data +
          '" id="deleteBtn"><i class="fas fa-trash"></i></a>'
        );
      },
    },
  ],
});

// Clear modal
function clear_modal() {
  $("#modal_title").empty();
  $("#modal_body").empty();
  $("#modal_footer").empty();
}
// Sửa đề tài
$("#bangdsdetai").on("click", "#editBtn", function () {
  let id = $(this).data("id");
  clear_modal();
  $.ajax({
    type: "GET",
    url: "get_chi_tiet_de_tai_by_id?id=" + id,
    success: function (res) {
      $("#modal_title").text(res.ten);
      $("#modal_body").append(
        '<div class="form-group"><label for="modal_tendetai_input">Tên đề tài</label><input type="email" class="form-control" id="modal_tendetai_input" placeholder="Nhập tên đề tài" value="' +
          res.ten +
          '"></div><div class="form-group"><label for="modal_motadetai_input">Mô tả đề tài</label><textarea id="modal_motadetai_input" rows="10" class="form-control" placeholder="Nhập mô tả đề tài">' +
          res.mota +
          '</textarea></div><div class="form-check"><input type="checkbox" class="form-check-input" id="modal_hoatdong_check"><label class="form-check-label" for="modal_hoatdong_check">Sử dụng đề tài</label></div>'
      );
      if (res.xoa == 0) {
        $("#modal_hoatdong_check").prop("checked", true);
      } else {
        $("#modal_hoatdong_check").prop("checked", false);
      }
      $("#modal_footer").append(
        '<button type="button" class="btn btn-primary" data-id="' +
          res.id +
          '" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu thay đổi</button>'
      );
      $("#modal_id").modal("show");
      // Tính năng lưu thay đổi
      $("#modal_submit_btn").click(function () {
        let id = $(this).data("id");

        let ten = $("#modal_tendetai_input").val();
        let mota = $("#modal_motadetai_input").val();
        let xoa = $("#modal_hoatdong_check").is(":checked");
        let isDeleted = xoa ? 0 : 1;

        $.ajax({
          type: "POST",
          url:
            "update_chi_tiet_de_tai_by_id?id=" +
            parseInt(id) +
            "&ten=" +
            ten +
            "&mota=" +
            mota +
            "&isDeleted=" +
            isDeleted,
          success: function (data) {
            if (data.status == "OK") {
              $("#modal_id").modal("hide");
              bangdsdetai.ajax.reload();
              Toast.fire({
                icon: "success",
                title: "Cập nhật thành công",
              });
            } else {
              Toast.fire({
                icon: "error",
                title: "Đã xãy ra lỗi",
              });
            }
          },
          error: function (xhr, status, error) {
            Toast.fire({
              icon: "error",
              title: "Đã xãy ra lỗi",
            });
          },
        });
      });
    },
  });
});

// Xoá đề tài
$("#bangdsdetai").on("click", "#deleteBtn", function () {
  let id = $(this).data("id");

  Swal.fire({
    title: "Bạn muốn xoá đề tài số " + id,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Xoá",
    cancelButtonText: "Huỷ",
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        url: "update_xoa_de_tai_by_id?id=" + parseInt(id),
        success: function (res) {
          Toast.fire({
            icon: "success",
            title: "Đã xoá",
          });
          bangdsdetai.ajax.reload();
        },
        error: function (xhr, status, error) {
          Toast.fire({
            icon: "error",
            title: "Xoá không thành công",
          });
        },
      });
    }
  });
});

// Modal thêm đề ài
$("#themdetai_btn").click(function(){
  // Clear modal
  clear_modal();
  $("#modal_title").text('Thêm đề tài');
  html = '<div class="form-group"><label for="modal_tendetai_input">Tên đề tài</label><input type="email" class="form-control" id="modal_tendetai_input" placeholder="Nhập tên đề tài"></div><div class="form-group"><label for="modal_motadetai_input">Mô tả đề tài</label><textarea id="modal_motadetai_input" rows="10" class="form-control" placeholder="Nhập mô tả đề tài"></textarea></div><div class="form-check"><input type="checkbox" class="form-check-input" id="modal_hoatdong_check"><label class="form-check-label" for="modal_hoatdong_check">Sử dụng đề tài</label></div>';
  $("#modal_body").append(html);
  $("#modal_footer").append(
    '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu</button>'
  );
  $("#modal_id").modal('show');
  
  $("#modal_submit_btn").click(function(){
    let ten = $("#modal_tendetai_input").val();
    let mota = $("#modal_motadetai_input").val();
    let xoa = $("#modal_hoatdong_check").is(":checked");
    let isDeleted = xoa ? 0 : 1;
  
    $.ajax({
      type: 'POST',
      url: 'them_de_tai_thuc_tap?ten='+ten+'&mota='+mota+'&isDeleted='+isDeleted,
      success: function(res){
        Toast.fire({
          icon: "success",
          title: "Đã thêm đề tài",
        });
        bangdsdetai.ajax.reload();
      },
      error: function (xhr, status, error) {
        Toast.fire({
          icon: "error",
          title: "Thêm đề tài không thành công",
        });
      },
    });
    $("#modal_id").modal('hide');    
  });
});
