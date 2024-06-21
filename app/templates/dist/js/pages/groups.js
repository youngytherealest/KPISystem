var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

let bangdsnhomthuctap = $("#bangdsnhomthuctap").DataTable({
  paging: true,
  lengthChange: false,
  searching: true,
  ordering: true,
  info: true,
  autoWidth: false,
  responsive: true,
  ajax: {
    type: "GET",
    url: "get_ds_nhom_thuc_tap",
    dataSrc: "",
  },
  columns: [
    { data: "id" },
    { data: "ngaybatdau"
    },
    { data: "tendetai" },
    { data: "nguoihuongdan" },
    {
      data: "xoa",
      render: function(data, type, row){
        if (data == 0) {
          return '<span class="badge badge-success"><i class="fa-solid fa-check"></i> Đang hoạt động</span>';
        } else {
          return '<span class="badge badge-danger" ><i class="fa-solid fa-xmark"></i> Ngưng hoạt động</span>';
        }
      }
    },
    {
      data: "id",
      render: function (data, type, row) {
        return (
          '<a class="btn btn-info btn-sm" id="editBtn" data-id="' +
          data +
          '" data-id_ktt="' +
          row.id_ktt +
          '" data-id_nhd="' +
          row.id_nhd +
          '" data-id_dt="' +
          row.id_dt +
          '" data-id_xoa="' +
          row.xoa +
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
$("#bangdsnhomthuctap").on("click", "#editBtn", function () {
  let id = $(this).data("id");
  let id_ktt = $(this).data("id_ktt");
  let id_nhd = $(this).data("id_nhd");
  let id_dtai = $(this).data("id_dt");
  let xoa = $(this).data("id_xoa");
  clear_modal();
  $.ajax({
    type: "GET",
    url: "get_chi_tiet_chinh_sua_nhom",
    success: function (res) {
      $("#modal_title").text('Nhóm '+id);

      html = '<div class="form-group"><label for="modal_kythuctap_select">Kỳ thực tập</label><select id="modal_kythuctap_select" class="form-control select2"></select></div><div class="form-group"><label for="modal_detai_select">Đề tài</label><select id="modal_detai_select" class="form-control select2"></select></div><div class="form-group"><label for="modal_nguoihuongdan_select">Người hướng dẫn</label><select id="modal_nguoihuongdan_select" class="form-control select2"></select></div><div class="form-check"><input type="checkbox" class="form-check-input" id="modal_hoatdong_check"><label class="form-check-label" for="modal_hoatdong_check">Sử dụng nhóm</label></div>';
      $("#modal_body").append(html);
      $.each(res.kythuctap, function(idx, val){
        $('#modal_kythuctap_select').append('<option value="'+val.id+'">'+moment(val.ngay, 'YYYY-MM-DD').format('DD/MM/YYYY')+'</option>');
      });
      $('#modal_kythuctap_select').val(id_ktt);
      $.each(res.detai, function(idx, val){
        $('#modal_detai_select').append('<option value="'+val.id+'">'+val.ten+'</option>');
      });
      $('#modal_detai_select').val(id_dtai);
      $.each(res.nguoihuongdan, function(idx, val){
        $('#modal_nguoihuongdan_select').append('<option value="'+val.id+'">'+val.hoten+'</option>');
      });
      $('#modal_nguoihuongdan_select').val(id_nhd);
      if (xoa == 0) {
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

        let xoa = $("#modal_hoatdong_check").is(":checked");
        let isDeleted = xoa ? 0 : 1;
        let kytt = $("#modal_kythuctap_select").val();
        let detai = $("#modal_detai_select").val();
        let nhd = $("#modal_nguoihuongdan_select").val();

        $.ajax({
          type: "POST",
          url:
            "update_chi_tiet_nhom_thuc_tap_by_id?id=" +
            parseInt(id) +
            "&kytt=" +
            parseInt(kytt) +
            "&nguoihd=" +
            parseInt(nhd) +
            "&detai=" +
            parseInt(detai) +
            "&isDeleted=" +
            isDeleted,
          success: function (data) {
            if (data.status == "OK") {
              $("#modal_id").modal("hide");
              bangdsnhomthuctap.ajax.reload();
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

// Xoá nhóm thực tập
$("#bangdsnhomthuctap").on("click", "#deleteBtn", function () {
  let id = $(this).data("id");

  Swal.fire({
    title: "Bạn muốn xoá nhóm thực tập số " + id,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Xoá",
    cancelButtonText: "Huỷ",
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        url: "update_xoa_nhom_thuc_tap_by_id?id=" + parseInt(id),
        success: function (res) {
          Toast.fire({
            icon: "success",
            title: "Đã xoá",
          });
          bangdsnhomthuctap.ajax.reload();
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
$("#themkythuctap_btn").click(function(){
  clear_modal();
  $.ajax({
    type: "GET",
    url: "get_chi_tiet_chinh_sua_nhom",
    success: function(res){
      $("#modal_title").text('Thêm nhóm thực tập');
      html = '<div class="form-group"><label for="modal_kythuctap_select">Kỳ thực tập</label><select id="modal_kythuctap_select" class="form-control select2"></select></div><div class="form-group"><label for="modal_detai_select">Đề tài</label><select id="modal_detai_select" class="form-control select2"></select></div><div class="form-group"><label for="modal_nguoihuongdan_select">Người hướng dẫn</label><select id="modal_nguoihuongdan_select" class="form-control select2"></select></div><div class="form-check"><input type="checkbox" class="form-check-input" id="modal_hoatdong_check"><label class="form-check-label" for="modal_hoatdong_check">Sử dụng nhóm</label></div>';

      $("#modal_body").append(html);
      $.each(res.kythuctap, function(idx, val){
        $('#modal_kythuctap_select').append('<option value="'+val.id+'">'+moment(val.ngay, 'YYYY-MM-DD').format('DD/MM/YYYY')+'</option>');
      });
      $.each(res.detai, function(idx, val){
        $('#modal_detai_select').append('<option value="'+val.id+'">'+val.ten+'</option>');
      });
      $.each(res.nguoihuongdan, function(idx, val){
        $('#modal_nguoihuongdan_select').append('<option value="'+val.id+'">'+val.hoten+'</option>');
      });

      $("#modal_footer").append(
        '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu</button>'
      );
      $("#modal_id").modal('show');
      
      $("#modal_submit_btn").click(function(){
        let xoa = $("#modal_hoatdong_check").is(":checked");
        let isDeleted = xoa ? 0 : 1;
        let kytt = $("#modal_kythuctap_select").val();
        let detai = $("#modal_detai_select").val();
        let nhd = $("#modal_nguoihuongdan_select").val();
    
        $.ajax({
          type: 'POST',
          url: "them_nhom_thuc_tap?kytt=" + parseInt(kytt) + "&nguoihd=" + parseInt(nhd) + "&detai=" + parseInt(detai) + "&isDeleted=" + isDeleted,
          success: function(res){
            Toast.fire({
              icon: "success",
              title: "Đã thêm kỳ thực tập",
            });
            bangdsnhomthuctap.ajax.reload();
          },
          error: function (xhr, status, error) {
            Toast.fire({
              icon: "error",
              title: "Thêm kỳ thực tập không thành công",
            });
          },
        });
        $("#modal_id").modal('hide');    
      });
    },
    error: function(xhr, status, error){
      console.log(error)
    }
  });
});
