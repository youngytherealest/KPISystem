var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

let bangdskythuctap = $("#bangdskythuctap").DataTable({
  paging: true,
  lengthChange: false,
  searching: true,
  ordering: true,
  info: true,
  autoWidth: false,
  responsive: true,
  ajax: {
    type: "GET",
    url: "get_all_ky_thuc_tap",
    dataSrc: "",
  },
  columns: [
    { data: "id" },
    { data: "ngaybatdau" },
    { data: "ngayketthuc" },
    {
      data: "thoihan",
      render: function (data, type, row) {
        if (data == 0) {
          return '<span class="badge badge-success"><i class="fa-solid fa-check"></i> Đang diễn ra</span>';
        } else {
          return '<span class="badge badge-danger"><i class="fa-solid fa-xmark"></i> Đã kết thúc</span>';
        }
      },
    },
    {
      data: "id",
      render: function (data, type, row) {
        return (
          '<a class="btn btn-info btn-sm" id="editBtn" data-id="' +
          data +
          '" data-thoihan="' +
          row.thoihan +
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
$("#bangdskythuctap").on("click", "#editBtn", function () {
  let id = $(this).data("id");
  let thoihan = $(this).data("thoihan");
  clear_modal();
  $.ajax({
    type: "GET",
    url: "get_chi_tiet_ky_thuc_tap_by_id?id=" + id,
    success: function (res) {
      $("#modal_title").text('Kỳ thực tập '+res.ngaybatdau);
      html = '<div class="form-group"><label>Thời gian thực tập:</label><div class="input-group"><div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span></div><input type="text" class="form-control float-right" id="reservation"></div></div><script>$("#reservation").daterangepicker();</script><div class="form-check"><input type="checkbox" class="form-check-input" id="modal_hoatdong_check"><label class="form-check-label" for="modal_hoatdong_check">Sử dụng kỳ thực tập</label></div>';
      $("#modal_body").append(html);
      $("#reservation").val(moment(res.ngaybatdau, 'DD/MM/YYYY').format('MM/DD/YYYY')+' - '+moment(res.ngayketthuc, 'DD/MM/YYYY').format('MM/DD/YYYY'))
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

        let dates = $("#reservation").val().split('-');
        let xoa = $("#modal_hoatdong_check").is(":checked");
        let isDeleted = xoa ? 0 : 1;
        let ngaybatdau = moment(dates[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
        let ngayketthuc = moment(dates[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
        console.log(dates[0]);
        $.ajax({
          type: "POST",
          url:
            "update_chi_tiet_ky_thuc_tap_by_id?id=" +
            parseInt(id) +
            "&ngaybatdau=" +
            ngaybatdau +
            "&ngayketthuc=" +
            ngayketthuc +
            "&isDeleted=" +
            isDeleted,
          success: function (data) {
            if (data.status == "OK") {
              $("#modal_id").modal("hide");
              bangdskythuctap.ajax.reload();
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

// Xoá kỳ thực tập
$("#bangdskythuctap").on("click", "#deleteBtn", function () {
  let id = $(this).data("id");

  Swal.fire({
    title: "Bạn muốn xoá kỳ thực tập số " + id,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Xoá",
    cancelButtonText: "Huỷ",
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      $.ajax({
        type: "POST",
        url: "update_xoa_ky_thuc_tap_by_id?id=" + parseInt(id),
        success: function (res) {
          Toast.fire({
            icon: "success",
            title: "Đã xoá",
          });
          bangdskythuctap.ajax.reload();
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
  // Clear modal
  clear_modal();
  $("#modal_title").text('Thêm kỳ thực tập');
  html = '<div class="form-group"><label>Thời gian thực tập:</label><div class="input-group"><div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span></div><input type="text" class="form-control float-right" id="reservation"></div></div><script>$("#reservation").daterangepicker();</script><div class="form-check"><input type="checkbox" class="form-check-input" id="modal_hoatdong_check"><label class="form-check-label" for="modal_hoatdong_check">Sử dụng kỳ thực tập</label></div>';
  $("#modal_body").append(html);
  $("#modal_footer").append(
    '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu</button>'
  );
  $("#modal_id").modal('show');
  
  $("#modal_submit_btn").click(function(){
    let dates = $("#reservation").val().split(' - ');
    let xoa = $("#modal_hoatdong_check").is(":checked");
    let isDeleted = xoa ? 0 : 1;
    let ngaybatdau = moment(dates[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
    let ngayketthuc = moment(dates[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
    $.ajax({
      type: 'POST',
      url: 'them_ky_thuc_tap?ngaybatdau='+ngaybatdau+'&ngayketthuc='+ngayketthuc+'&isDeleted='+isDeleted,
      success: function(res){
        Toast.fire({
          icon: "success",
          title: "Đã thêm kỳ thực tập",
        });
        bangdskythuctap.ajax.reload();
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
});
