/*
 * Author: Abdullah A Almsaeed
 * Date: 4 Jan 2014
 * Description:
 *      This is a demo file used only for the main dashboard (index.html)
 **/

/* global moment:false, Chart:false, Sparkline:false */

$(function () {
  "use strict";

  // Make the dashboard widgets sortable Using jquery UI
  $(".connectedSortable").sortable({
    placeholder: "sort-highlight",
    connectWith: ".connectedSortable",
    handle: ".card-header, .nav-tabs",
    forcePlaceholderSize: true,
    zIndex: 999999,
  });
  $(".connectedSortable .card-header").css("cursor", "move");

  // bootstrap WYSIHTML5 - text editor
  $(".textarea").summernote();

  $(".daterange").daterangepicker(
    {
      ranges: {
        Today: [moment(), moment()],
        Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
        "Last 7 Days": [moment().subtract(6, "days"), moment()],
        "Last 30 Days": [moment().subtract(29, "days"), moment()],
        "This Month": [moment().startOf("month"), moment().endOf("month")],
        "Last Month": [
          moment().subtract(1, "month").startOf("month"),
          moment().subtract(1, "month").endOf("month"),
        ],
      },
      startDate: moment().subtract(29, "days"),
      endDate: moment(),
    },
    function (start, end) {
      // eslint-disable-next-line no-alert
      alert(
        "You chose: " +
          start.format("MMMM D, YYYY") +
          " - " +
          end.format("MMMM D, YYYY")
      );
    }
  );

  /* jQueryKnob */
  $(".knob").knob();

  // jvectormap data
  var visitorsData = {
    US: 398, // USA
    SA: 400, // Saudi Arabia
    CA: 1000, // Canada
    DE: 500, // Germany
    FR: 760, // France
    CN: 300, // China
    AU: 700, // Australia
    BR: 600, // Brazil
    IN: 800, // India
    GB: 320, // Great Britain
    RU: 3000, // Russia
  };
  // --------------------------------------------------------------------------------------------------------------
  /* Chart.js Charts */
  $.ajax({
    type: "GET",
    url: "get_so_luong_sinh_vien_theo_truong",
    success: function (response) {
      // Donut chart for major
      let truong = [];
      let soluong = [];

      $.each(response, function (idx, val) {
        truong.push(val["truong"]);
        soluong.push(val["soluong"]);
      });

      var collegeChart = document
        .getElementById("college-chart-canvas")
        .getContext("2d");
      var myCollegeChart = new Chart(collegeChart, {
        type: "bar",
        data: {
          labels: truong,
          datasets: [
            {
              data: soluong,
              borderWidth: 1,
              backgroundColor: [
                "rgba(255, 99, 132, 0.8)",
                "rgba(255, 159, 64, 0.8)",
                "rgba(255, 205, 86, 0.8)",
                "rgba(75, 192, 192, 0.8)",
                "rgba(54, 162, 235, 0.8)",
                "rgba(153, 102, 255, 0.8)",
                "rgba(201, 203, 207, 0.8)",
              ],
            },
          ],
          hoverOffset: 1,
        },
        options: {
          responsive: true,
          plugins: {
            legend: false,
          },
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  });

  // Clear modal
  let clearmodal = function clear_modal() {
    $("#modal_title").empty();
    $("#modal_body").empty();
    $("#modal_footer").empty();
  }

  $.ajax({
    type: "GET",
    url: "get_so_luong_sinh_vien_theo_nganh",
    success: function (response) {
      // Donut chart for major
      let nganh = [];
      let soluong = [];

      $.each(response, function (idx, val) {
        nganh.push(val["nganh"]);
        soluong.push(val["soluong"]);
      });
      var majorChart = document.getElementById("world_map").getContext("2d");
      var myMajorChart = new Chart(majorChart, {
        type: "pie",
        data: {
          labels: nganh,
          datasets: [
            {
              data: soluong,
              borderWidth: 1,
              backgroundColor: [
                "rgba(255, 99, 132, 0.8)",
                "rgba(255, 159, 64, 0.8)",
                "rgba(255, 205, 86, 0.8)",
                "rgba(75, 192, 192, 0.8)",
                "rgba(54, 162, 235, 0.8)",
                "rgba(153, 102, 255, 0.8)",
                "rgba(201, 203, 207, 0.8)",
              ],
            },
          ],
          hoverOffset: 4,
        },
        options: {
          responsive: true,
          cutoutPercentage: 70, // Độ lớn của lỗ trống ở giữa (giữa các vòng)
          plugins: {
            legend: {
              position: "bottom",
            },
          },
        },
      });
    },
  });

let bangdssv = $("#dashboard_bangdssv").DataTable({
    paging: true,
    lengthChange: false,
    searching: true,
    ordering: true,
    info: true,
    autoWidth: false,
    responsive: true,
    ajax: {
      type: "GET",
      url: "get_all_sinh_vien",
      dataSrc: "",
    },
    columns: [
      { data: "mssv" },
      { data: "hoten" },
      { data: "gioitinh" },
      { data: "nganh" },
      { data: "truong" },
      {
        data: "trangthai",
        render: function(data, type, row){
          if(data==0){
            return '<span class="badge badge-danger"><i class="fa-solid fa-triangle-exclamation"></i> Chưa có nhóm</span>';
          }else if(data==1){
            return '<span class="badge badge-warning"><i class="fa-solid fa-circle-exclamation"></i> Chưa đánh giá</span>';
          }else{
            return '<span class="badge badge-success"><i class="fa-solid fa-check"></i> Đã đánh giá</span>';
          }
        }
      },
      {
        data: "id",
        render: function (data, type, row) {
          return (
            '<a data-id="' +
            data +
            '" class="btn btn-sm" id="viewBtn"  style="color: green; text-align: center; "><i class="fa-solid fa-eye"></i></a>'
          );
        },
      },
    ],
  });
});

$("#dashboard_bangdssv").on('click', '#viewBtn', function(){
  let id = $(this).data('id');
  // Clear modal
  $("#modal_title").empty();
  $("#modal_body").empty();
  $("#modal_footer").empty();
  $.ajax({
    type: 'GET',
    url: 'get_chi_tiet_sinh_vien_by_id?id=' + id,
    success: function(res){
      $('.modal-dialog').addClass('modal-lg');
      $('#modal_title').text('Thông tin sinh viên');
      let html='';

      if(res.trangthai==0){
        html='<table class="table" id="thongtinsinhvien"><tr>    <td>Họ tên</td>    <td>'+res.hoten+'</td></tr><tr>    <td>MSSV</td>    <td>'+res.mssv+'</td></tr><tr>    <td>Giới tính</td>    <td>'+res.gioitinh+'</td></tr><tr>    <td>SĐT</td>    <td>'+res.sdt+'</td></tr><tr>    <td>Email</td>    <td>'+res.email+'</td></tr><tr>    <td>Điạ chỉ</td>    <td>'+res.diachi+'</td></tr><tr>    <td>Mã lớp</td>    <td>'+res.malop+'</td></tr><tr>    <td>Khoá</td>    <td>'+res.khoa+'</td></tr><tr>    <td>Ngành</td>    <td>'+res.nganh+'</td></tr><tr>    <td>Trường</td>    <td>'+res.truong+'</td></tr></table>';
      }else if(res.trangthai==1){
        html='<table class="table" id="thongtinsinhvien"><tr>    <td>Họ tên</td>    <td>'+res.hoten+'</td></tr><tr>    <td>MSSV</td>    <td>'+res.mssv+'</td></tr><tr>    <td>Giới tính</td>    <td>'+res.gioitinh+'</td></tr><tr>    <td>SĐT</td>    <td>'+res.sdt+'</td></tr><tr>    <td>Email</td>    <td>'+res.email+'</td></tr><tr>    <td>Điạ chỉ</td>    <td>'+res.diachi+'</td></tr><tr>    <td>Mã lớp</td>    <td>'+res.malop+'</td></tr><tr>    <td>Khoá</td>    <td>'+res.khoa+'</td></tr><tr>    <td>Ngành</td>    <td>'+res.nganh+'</td></tr><tr>    <td>Trường</td>    <td>'+res.truong+'</td></tr><tr>    <td>Kỳ thực tập</td>    <td>'+res.ngaybatdau+'</td></tr><tr>    <td>Đề tài</td>    <td>'+res.tendetai+'</td></tr><tr>    <td>Người hướng dẫn</td>    <td>'+res.nguoihuongdan+'</td></tr></table>';
      }else{
        html = '<table class="table" id="thongtinsinhvien"> <tr> <td>Họ tên</td> <td>'+res.hoten+'</td> </tr> <tr> <td>MSSV</td> <td>'+res.mssv+'</td> </tr> <tr> <td>Giới tính</td> <td>'+res.gioitinh+'</td> </tr> <tr> <td>SĐT</td> <td>'+res.sdt+'</td> </tr> <tr> <td>Email</td> <td>'+res.email+'</td> </tr> <tr> <td>Điạ chỉ</td> <td>'+res.diachi+'</td> </tr> <tr> <td>Mã lớp</td> <td>'+res.malop+'</td> </tr> <tr> <td>Khoá</td> <td>'+res.khoa+'</td> </tr> <tr> <td>Ngành</td> <td>'+res.nganh+'</td> </tr> <tr> <td>Trường</td> <td>'+res.truong+'</td> </tr> <tr> <td>Kỳ thực tập</td> <td>'+res.ngaybatdau+'</td> </tr> <tr> <td>Đề tài</td> <td>'+res.tendetai+'</td> </tr> <tr> <td>Người hướng dẫn</td> <td>'+res.nguoihuongdan+'</td> </tr> <tr> <td> Ý thức kỷ luật </td> <td> <span class="badge badge-primary"> '+res.ythuckyluat_number+' </span> '+res.ythuckyluat_text+' </td> </tr> <tr> <td> Tuân thủ thời gian </td> <td> <span class="badge badge-primary"> '+res.tuanthuthoigian_number+' </span> '+res.tuanthuthoigian_text+' </td> </tr> <tr> <td> Kiến thức </td> <td> <span class="badge badge-primary"> '+res.kienthuc_number+' </span> '+res.kienthuc_text+' </td> </tr> <tr> <td> Kỷ năng nghề </td> <td> <span class="badge badge-primary"> '+res.kynangnghe_number+' </span> '+res.kynangnghe_text+' </td> </tr> <tr> <td> Khả năng làm việc độc lập </td> <td> <span class="badge badge-primary"> '+res.khanangdoclap_number+' </span> '+res.khanangdoclap_text+' </td> </tr> <tr> <td> Khả năng làm việc nhóm </td> <td> <span class="badge badge-primary"> '+res.khanangnhom_number+' </span> '+res.khanangnhom_text+' </td> </tr> <tr> <td> Khả năng giải quyết công việc </td> <td> <span class="badge badge-primary"> '+res.khananggiaiquyetcongviec_number+' </span> '+res.khananggiaiquyetcongviec_text+' </td> </tr> <tr> <td> Đánh giá chung </td> <td> <span class="badge badge-primary"> '+res.danhgiachung_number+' </span> </td> </tr> </table>';
      }
      $('#modal_body').append(html);
      $('#modal_id').modal('show');
    }
  })
});
