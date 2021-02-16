
$(document).on('hide.bs.modal',"#eventModal", function (evt) {
    // Assuming that an update just got completed
    $("#element-"+$(evt.target).data("event-type")+"-table-"+$(evt.target).data("element-id")).DataTable().rows().invalidate().draw();
});

$(document).on('hide.bs.modal',"#eventModal[data-event-type=return]", function (evt) {
    // Assuming that an update just got completed
    $("#element-borrow-table-"+$(evt.target).data("element-id")).DataTable().rows().invalidate().draw();
});
