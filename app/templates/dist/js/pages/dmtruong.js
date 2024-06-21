var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
  });
  
  let bangdstruong = $("#bangdstruong").DataTable({
    paging: true,
    lengthChange: false,
    searching: true,
    ordering: true,
    info: true,
    autoWidth: false,
    responsive: true,
    ajax: {
      type: "GET",
      url: "get_all_truong",
      dataSrc: "",
    },
    columns: [
      { data: "id" },
      { data: "tentruong" },
      { data: "kyhieu" },
      {
        data: "trangthai",
        render: function (data, type, row) {
          if (data == 0) {
            return '<span class="badge badge-success"><i class="fa-solid fa-check"></i> Hoạt động</span>';
          } else {
            return '<span class="badge badge-danger"><i class="fa-solid fa-xmark"></i> Đã khóa</span>';
          }
        },
      },
      {
        data: "id",
        render: function (data, type, row) {
          return (
            '<a class="btn btn-info btn-sm" id="editBtn" data-id="' +
            data +
            '" data-tentruong="' +
            row.tentruong +
            '" data-kyhieu="' +
            row.kyhieu +
            '" data-trangthai="' +
            row.trangthai +
            '"><i class="fas fa-pencil-alt"></i></a>  <a class="btn btn-danger btn-sm" data-id="' +
            data +
            '" data-kyhieu="' +
            row.kyhieu +
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
  $("#bangdstruong").on("click", "#editBtn", function () {
    let id = $(this).data("id");
    let tentruong = $(this).data("tentruong");
    let kyhieu = $(this).data("kyhieu");
    let trangthai = $(this).data("trangthai");
    clear_modal();
    $.ajax({
      type: "GET",
      url: "get_chi_tiet_truong_by_id?id=" + id,
      success: function (res) {
        $("#modal_title").text('Thông tin trường');
        html = '<div class="form-group">'+
          '<div class="row">'+
              '<label>Tên trường</label>'+
              '<input type="text" class="form-control float-right" id="tentruong_text">'+
          '</div>'+
          '<div class="row">'+
              '<label>Ký hiệu</label>'+
              '<input type="text" class="form-control float-right" id="kyhieu_text">'+
          '</div>'+
          '<div class="form-check">'+
          '<input type="checkbox" class="form-check-input" id="modal_hoatdong_check">'+
          '<label class="form-check-label" for="modal_hoatdong_check">Sử dụng trường</label>'+
          '</div>';
        $("#modal_body").append(html);
        $("#tentruong_text").val(tentruong);
        $("#kyhieu_text").val(kyhieu);
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
  
          let tentruong = $("#tentruong_text").val().trim();
          let xoa = $("#modal_hoatdong_check").is(":checked");
          let isDeleted = xoa ? 0 : 1;
          let kyhieu = $("#kyhieu_text").val().trim();
          $.ajax({
            type: "POST",
            url:
              "update_chi_tiet_truong_by_id?id=" +
              parseInt(id) +
              "&tentruong=" +
              tentruong +
              "&kyhieu=" +
              kyhieu +
              "&isDeleted=" +
              isDeleted,
            success: function (data) {
              if (data.status == "OK") {
                $("#modal_id").modal("hide");
                bangdstruong.ajax.reload();
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
  
  // Xoá trường
  $("#bangdstruong").on("click", "#deleteBtn", function () {
    let id = $(this).data("id");
    let kyhieu = $(this).data("kyhieu");
    Swal.fire({
      title: "Bạn muốn xoá trường có ký hiệu <span style='color: red;'>" + kyhieu + "</span>",
      showDenyButton: false,
      showCancelButton: true,
      confirmButtonText: "Xoá",
      cancelButtonText: "Huỷ",
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          url: "update_xoa_truong_by_id?id=" + parseInt(id),
          success: function (res) {
            Toast.fire({
              icon: "success",
              title: "Đã xoá",
            });
            bangdstruong.ajax.reload();
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
  $("#themtruong_btn").click(function(){
    // Clear modal
    clear_modal();
    $("#modal_title").text('Thêm trường');
    html = '<div class="form-group">'+
    '<div class="row">'+
        '<label>Tên trường</label>'+
        '<input type="text" class="form-control float-right" id="tentruong_text">'+
    '</div>'+
    '<div class="row">'+
        '<label>Ký hiệu</label>'+
        '<input type="text" class="form-control float-right" id="kyhieu_text">'+
    '</div>'+
    '<div class="form-check">'+
    '<input type="checkbox" class="form-check-input" id="modal_hoatdong_check">'+
    '<label class="form-check-label" for="modal_hoatdong_check">Sử dụng trường</label>'+
    '</div>';
    $("#modal_body").append(html);
    $("#modal_footer").append(
      '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu</button>'
    );
    $("#modal_id").modal('show');
    
    $("#modal_submit_btn").click(function(){
      let tentruong = $("#tentruong_text").val().trim();
      let xoa = $("#modal_hoatdong_check").is(":checked");
      let isDeleted = xoa ? 0 : 1;
      let kyhieu = $("#kyhieu_text").val().trim();
      $.ajax({
        type: 'POST',
        url: 'them_truong?tentruong='+tentruong+'&kyhieu='+kyhieu+'&isDeleted='+isDeleted,
        success: function(res){
          Toast.fire({
            icon: "success",
            title: "Đã thêm trường",
          });
          bangdstruong.ajax.reload();
        },
        error: function (xhr, status, error) {
          Toast.fire({
            icon: "error",
            title: "Thêm trường không thành công",
          });
        },
      });
      $("#modal_id").modal('hide');    
    });
  });
  