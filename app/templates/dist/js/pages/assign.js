var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
  });

// Clear modal
function clear_modal() {
    $("#modal_title").empty();
    $("#modal_body").empty();
    $("#modal_footer").empty();
  }

// Modal thêm Công việc
$("#themconviecviec_btn").click(function(){
    // Clear modal
    clear_modal();
    $("#modal_title").text('Thêm công việc');
    html = '<div class="form-group">'+
    '<label>Nhóm thực tập:</label>'+
    ' <div class="input-group"> <select class="form-control" id="dsnhomthuctap" style="width: 100%;"></select> </div> </div><div class="form-group"><label>Thời gian tuần 1:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_1"> </div> </div> <div class="form-group"><label>Công việc tuần 1:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_1" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 2:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_2"> </div> </div> <div class="form-group"><label>Công việc tuần 2:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_2" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 3:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_3"> </div> </div> <div class="form-group"><label>Công việc tuần 3:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_3" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 4:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_4"> </div> </div> <div class="form-group"><label>Công việc tuần 4:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_4" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 5:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_5"> </div> </div> <div class="form-group"><label>Công việc tuần 5:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_5" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 6:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_6"> </div> </div> <div class="form-group"><label>Công việc tuần 6:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_6" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 7:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_7"> </div> </div> <div class="form-group"><label>Công việc tuần 7:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_7" rows="5"></textarea> </div> </div> <div class="form-group"><label>Thời gian tuần 8:</label> <div class="input-group"> <div class="input-group-prepend"><span class="input-group-text"><i class="far fa-calendar-alt"></i></span> </div><input type="text" class="form-control float-right" id="thoigiantuan_8"> </div> </div> <div class="form-group"><label>Công việc tuần 8:</label> <div class="input-group"> <textarea class="form-control" id="congviectuan_8" rows="5"></textarea> </div> </div>';
    $("#modal_body").append(html);
    $("#modal_footer").append(
      '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu</button>'
    );

    $("#thoigiantuan_1").daterangepicker();
    $("#thoigiantuan_2").daterangepicker();
    $("#thoigiantuan_3").daterangepicker();
    $("#thoigiantuan_4").daterangepicker();
    $("#thoigiantuan_5").daterangepicker();
    $("#thoigiantuan_6").daterangepicker();
    $("#thoigiantuan_7").daterangepicker();
    $("#thoigiantuan_8").daterangepicker();
    
    $.ajax({
        url: '/get_ds_nhom_chua_co_cong_viec',
        type: 'GET',
        success: function(res){
            $.each(res, function(idx, val){
                if(val['idcongviec']===null){
                  let tennhom = val['tennhom'].split(' - ');
                    $("#dsnhomthuctap").append('<option value="'+val['id']+'" class="form-control">['+val['ngaybatdau']+'] - '+val['tendetai']+' - '+tennhom[0]+'</option>');
                }
            });
        }
    })

    $("#modal_id").modal('show');
    
    $("#modal_submit_btn").click(function(){
      let idnhom = $("#dsnhomthuctap").val();
      let tuan_1 = $("#thoigiantuan_1").val().split(' - ');
      let tuan_1_bd = moment(tuan_1[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_1_kt = moment(tuan_1[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_1_cv = $("#congviectuan_1").val();
      let tuan_2 = $("#thoigiantuan_2").val().split(' - ');
      let tuan_2_bd = moment(tuan_2[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_2_kt = moment(tuan_2[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_2_cv = $("#congviectuan_2").val();
      let tuan_3 = $("#thoigiantuan_3").val().split(' - ');
      let tuan_3_bd = moment(tuan_3[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_3_kt = moment(tuan_3[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_3_cv = $("#congviectuan_3").val();
      let tuan_4 = $("#thoigiantuan_4").val().split(' - ');
      let tuan_4_bd = moment(tuan_4[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_4_kt = moment(tuan_4[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_4_cv = $("#congviectuan_4").val();
      let tuan_5 = $("#thoigiantuan_5").val().split(' - ');
      let tuan_5_bd = moment(tuan_5[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_5_kt = moment(tuan_5[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_5_cv = $("#congviectuan_5").val();
      let tuan_6 = $("#thoigiantuan_6").val().split(' - ');
      let tuan_6_bd = moment(tuan_6[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_6_kt = moment(tuan_6[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_6_cv = $("#congviectuan_6").val();
      let tuan_7 = $("#thoigiantuan_7").val().split(' - ');
      let tuan_7_bd = moment(tuan_7[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_7_kt = moment(tuan_7[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_7_cv = $("#congviectuan_7").val();
      let tuan_8 = $("#thoigiantuan_8").val().split(' - ');
      let tuan_8_bd = moment(tuan_8[0], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_8_kt = moment(tuan_8[1], 'MM/DD/YYYY').format('YYYY-MM-DD');
      let tuan_8_cv = $("#congviectuan_8").val();

      $.ajax({
        type: 'POST',
        url: 'them_cong_viec_nhom?id='+idnhom
        +'&tungaytuan_1='+tuan_1_bd
        +'&denngaytuan_1='+tuan_1_kt
        +'&congviectuan_1='+tuan_1_cv
        +'&tungaytuan_2='+tuan_2_bd
        +'&denngaytuan_2='+tuan_2_kt
        +'&congviectuan_2='+tuan_2_cv
        +'&tungaytuan_3='+tuan_3_bd
        +'&denngaytuan_3='+tuan_3_kt
        +'&congviectuan_3='+tuan_3_cv
        +'&tungaytuan_4='+tuan_4_bd
        +'&denngaytuan_4='+tuan_4_kt
        +'&congviectuan_4='+tuan_4_cv
        +'&tungaytuan_5='+tuan_5_bd
        +'&denngaytuan_5='+tuan_5_kt
        +'&congviectuan_5='+tuan_5_cv
        +'&tungaytuan_6='+tuan_6_bd
        +'&denngaytuan_6='+tuan_6_kt
        +'&congviectuan_6='+tuan_6_cv
        +'&tungaytuan_7='+tuan_7_bd
        +'&denngaytuan_7='+tuan_7_kt
        +'&congviectuan_7='+tuan_7_cv
        +'&tungaytuan_8='+tuan_8_bd
        +'&denngaytuan_8='+tuan_8_kt
        +'&congviectuan_8='+tuan_8_cv,
        success: function(res){
            if(res.status == 'OK'){
                Toast.fire({
                  icon: "success",
                  title: "Đã công việc thực tập",
                });
                bangdskythuctap.ajax.reload();
            }else{
                Toast.fire({
                    icon: "error",
                    title: "Thêm công việc thực tập không thành công",
                });      
            }
        },
        error: function (xhr, status, error) {
          Toast.fire({
            icon: "error",
            title: "Thêm công việc không thành công",
          });
        },
      });
      $("#modal_id").modal('hide');    
    });
  });

// DS nhóm đã có công việc
$.ajax({
    type: 'GET',
    url: 'get_ds_nhom_da_co_cong_viec',
    success: function(res){
        $.each(res, function(idx, val){
            $("#dsnhomdacoviec").append('<option value="'+val.id+'">['+val.ngaybatdau+'] - '+val.tendetai+'</option>');
        });
    }
});

$("#dsnhomdacoviec").on('change', function(){
    let id = $("#dsnhomdacoviec").val();
    $("#dscongviec").empty();

    $.ajax({
        type: 'GET',
        url: 'get_ds_cong_viec_by_id_nhom?id='+id,
        success: function(res){
            let html = '';
            for (var i = res.length -1; i >= 0; i--){
                if(res[i]['congviectuan'] !== ''){
                    html += '<div class="time-label"><span class="bg-success" id="tuan">Tuần '+(i+1)+'</span></div>';
                    html += '<div><i class="fas fa-arrow-right bg-primary"></i><div class="timeline-item"><h3 class="timeline-header"><b id="ngay">'+res[i]['tungaytuan']+' - '+res[i]['denngaytuan']+'</b></h3><div class="timeline-body" id="congviec">'+res[i]['congviectuan']+'</div><div class="timeline-footer"></div></div></div>';
                }
            };
            html += '<div><i class="far fa-clock bg-gray"></i></div>';
            $("#dscongviec").append(html);
        }
    });
});