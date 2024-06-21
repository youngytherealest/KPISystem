var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
  });
  function loadFilterTruong() {
    // load kỳ thực tập
    $.ajax({
      type: 'GET',
      url: '/get_all_truong',
      success: function(data) {
        let filter_truong = $('#filter_truong');
        data.forEach(element => {
          filter_truong.append('<option value=' + element.id + '>' + element.tentruong + '</option>');
        });
      }
    })
   }
   function loadFilterTruong_add() {
    // load kỳ thực tập
    $.ajax({
      type: 'GET',
      url: '/get_all_truong',
      success: function(data) {
        let filter_truong_add = $('#filter_truong_add');
        data.forEach(element => {
            filter_truong_add.append('<option value=' + element.id + '>' + element.tentruong + '</option>');
        });
      }
    })
   }
   function loadFilterTruong_Update() {
    // load kỳ thực tập
    $.ajax({
      type: 'GET',
      url: '/get_all_truong',
      success: function(data) {
        let filter_truong_update = $('#filter_truong_update');
        data.forEach(element => {
            filter_truong_update.append('<option value=' + element.id + '>' + element.tentruong + '</option>');
        });
      }
    })
  }
  function create_table_nganh(id_truong){
    let bangdsnganh = $("#bangdsnganh").DataTable({
        paging: true,
        lengthChange: false,
        searching: true,
        ordering: true,
        info: true,
        autoWidth: false,
        responsive: true,
        destroy: true,
        ajax: {
          type: "GET",
          url: "get_all_nganh_by_id_truong?id="+id_truong,
          dataSrc: "",
        },
        columns: [
          { data: "id" },
          { data: "tennganh" },
          { data: "kyhieu" },
          { data: "tentruong" },
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
                '" data-tennganh="' +
                row.tennganh +
                '" data-kyhieu="' +
                row.kyhieu +
                '" data-trangthai="' +
                row.trangthai +
                '" data-id_truong="' +
                row.id_truong +
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
  }
  
  // Clear modal
  function clear_modal() {
    $("#modal_title").empty();
    $("#modal_body").empty();
    $("#modal_footer").empty();
  }
  // Sửa đề tài
  $("#bangdsnganh").on("click", "#editBtn", function () {
    let id = $(this).data("id");
    let tennganh = $(this).data("tennganh");
    let kyhieu = $(this).data("kyhieu");
    let trangthai = $(this).data("trangthai");
    let id_truong = $(this).data("id_truong");
    clear_modal();
    $.ajax({
      type: "GET",
      url: "get_chi_tiet_nganh_by_id?id=" + id,
      success: function (res) {
        $("#modal_title").text('Thông tin ngành');
        html = '<div class="form-group">'+
        '<div class="row">'+
            '<label>Tên ngành</label>'+
            '<input type="text" class="form-control float-right" id="tennganh_text">'+
        '</div>'+
        '<div class="row">'+
            '<label>Ký hiệu</label>'+
            '<input type="text" class="form-control float-right" id="kyhieu_text">'+
        '</div>'+
        '<div class="row">'+
            '<label for="filter_truong_update">Trường</label>'+
            '<select name="filter_truong_update" id="filter_truong_update" class="form-control select2">'+
            '</select>'+
        '</div>'+
        '<div class="form-check">'+
        '<input type="checkbox" class="form-check-input" id="modal_hoatdong_check">'+
        '<label class="form-check-label" for="modal_hoatdong_check">Sử dụng ngành</label>'+
        '</div>';
        $("#modal_body").append(html);
        loadFilterTruong_Update();
        $("#tennganh_text").val(tennganh);
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
  
          let tennganh = $("#tennganh_text").val().trim();
          let xoa = $("#modal_hoatdong_check").is(":checked");
          let isDeleted = xoa ? 0 : 1;
          let kyhieu = $("#kyhieu_text").val().trim();
          let id_truong = $("#filter_truong_update").val();
          $.ajax({
            type: "POST",
            url:
              "update_chi_tiet_nganh_by_id?id=" +
              parseInt(id) +
              "&tennganh=" +
              tennganh +
              "&kyhieu=" +
              kyhieu +
              "&isDeleted=" +
              isDeleted +
              "&id_truong=" +
              id_truong ,
            success: function (data) {
              if (data.status == "OK") {
                $("#modal_id").modal("hide");
                create_table_nganh('-1');
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
  
  // Xoá 
  $("#bangdsnganh").on("click", "#deleteBtn", function () {
    let id = $(this).data("id");
    let kyhieu = $(this).data("kyhieu");
    Swal.fire({
      title: "Bạn muốn xoá ngành có ký hiệu <span style='color: red;'>" + kyhieu + "</span>",
      showDenyButton: false,
      showCancelButton: true,
      confirmButtonText: "Xoá",
      cancelButtonText: "Huỷ",
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        $.ajax({
          type: "POST",
          url: "update_xoa_nganh_by_id?id=" + parseInt(id),
          success: function (res) {
            Toast.fire({
              icon: "success",
              title: "Đã xoá",
            });
            create_table_nganh('-1');
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
  
  // Modal thêm 
  $("#themnganh_btn").click(function(){
    // Clear modal
    clear_modal();
    $("#modal_title").text('Thêm ngành');
    html = '<div class="form-group">'+
    '<div class="row">'+
        '<label>Tên ngành</label>'+
        '<input type="text" class="form-control float-right" id="tennganh_text">'+
    '</div>'+
    '<div class="row">'+
        '<label>Ký hiệu</label>'+
        '<input type="text" class="form-control float-right" id="kyhieu_text">'+
    '</div>'+
    '<div class="row">'+
        '<label for="filter_truong_add">Trường</label>'+
        '<select name="filter_truong_add" id="filter_truong_add" class="form-control select2">'+
        '</select>'+
    '</div>'+
    '<div class="form-check">'+
    '<input type="checkbox" class="form-check-input" id="modal_hoatdong_check">'+
    '<label class="form-check-label" for="modal_hoatdong_check">Sử dụng ngành</label>'+
    '</div>';
    $("#modal_body").append(html);
    loadFilterTruong_add();
    $("#modal_footer").append(
      '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu</button>'
    );
    $("#modal_id").modal('show');
    
    $("#modal_submit_btn").click(function(){
      let tennganh = $("#tennganh_text").val().trim();
      let xoa = $("#modal_hoatdong_check").is(":checked");
      let isDeleted = xoa ? 0 : 1;
      let kyhieu = $("#kyhieu_text").val().trim();
      let id_truong = $("#filter_truong_add").val();
      $.ajax({
        type: 'POST',
        url: 'them_nganh?tennganh='+tennganh+'&kyhieu='+kyhieu+'&isDeleted='+isDeleted+'&id_truong='+id_truong,
        success: function(res){
          Toast.fire({
            icon: "success",
            title: "Đã thêm ngành",
          });
          create_table_nganh('-1');
        },
        error: function (xhr, status, error) {
          Toast.fire({
            icon: "error",
            title: "Thêm ngành không thành công",
          });
        },
      });
      $("#modal_id").modal('hide');    
    });
  });
  $(document).ready(function(){
    create_table_nganh('-1');
    $('#filter_truong').on('change', function() {
        let truong = $('#filter_truong').val();
        console.log(truong);

        create_table_nganh(parseInt(truong));
      });
      
    loadFilterTruong();
  });

  