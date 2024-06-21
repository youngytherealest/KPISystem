$(document).ready(function() {
    let username = window.location.href.split('?id=')[1];
    

    $.ajax({
        type: 'GET',
        url: 'get_ds_de_tai_profile?id='+username,
        success: function(res){
            let html = '';
            // Gom nhóm dữ liệu theo ngày
            let data = res.reduce((groups, item) => {
                            const ngay = item.ngay;
                            if (!groups[ngay]) {
                            groups[ngay] = [];
                            }
                            groups[ngay].push(item);
                            return groups;
                        }, {});
            
            
            // Lặp qua các ngày
            for (const ngay in data) {
                if (data.hasOwnProperty(ngay)) {
                // console.log(`Ngày: ${ngay}`);
                html += '<div class="time-label"><span class="bg-success" id="ngay">'+ngay+'</span></div>';
                
                // Lặp qua các đối tượng trong mảng
                data[ngay].forEach(item => {
                    html += '<div><i class="fas fa-envelope bg-primary"></i><div class="timeline-item"><h3 class="timeline-header"><b id="tendetai">'+item.ten+'</b></h3><div class="timeline-body" id="mota">'+item.mota+'</div><div class="timeline-footer"></div></div></div>';
                    // console.log(`  Tên: ${item.ten}`);
                    // console.log(`  Mô tả: ${item.mota}`);
                });
                }
            }
            html += '<div><i class="far fa-clock bg-gray"></i></div>';
            $("#dsdetai").append(html);
        }
    });
});
    