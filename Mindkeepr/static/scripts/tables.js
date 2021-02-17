
$(document).on('hide.bs.modal',"#eventModal", function (evt) {
    // Assuming that an update just got completed
    $(".element-"+$(evt.target).data("event-type")+"-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
    $(".element-location-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
});

$(document).on('hide.bs.modal',"#eventModal[data-event-type=return]", function (evt) {
    // Assuming that an update just got completed
    $(".element-borrow-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
    $(".element-location-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
});


function load_buy_table(id,is_unique,permission_buy)
{
    $(".element-buy-table[data-element-id="+id+"]").DataTable({
    "dom": '<"top">rt<"bottom"lip><"clear">',
    'serverSide': true,
    "responsive": true,
    'ajax': '/api/v1/buys?element='+id+'&format=datatables',
    "order": [[ 0, "desc" ]],
    "columnDefs": [
      {
          "targets": '_all',
          "defaultContent": ""
      },
      {
          "targets": [1],
          "display": !is_unique
      }
    ],
    columns: [
        { data: "recording_date", title: "Date",
        render: function (data, type, row, meta) {
                if (type === 'display') {
                    if(data){
                        return convertISO8601ToHumanDay(data);
                    }
                    else
                    {
                        return "Undefined";
                    }
                } else {
                    return data;
                }
            }},
            { data: "quantity", title: "Quantity"},
            { data: "price", title: "Price"},
            { data: "supplier", title: "Supplier"},
        { data: "location_destination.id", title: "Destination",
          render: function(data,type,row,meta){
          if(type === "display"){
              link = "<a href=\"/location/"+row.location_destination.id+"\">"+row.location_destination.name+"</a>";
              return link;
          }
          return row.location_destination.name;
        }},
        { data: "project", title: "Project",
                render: function(data,type,row,meta){
                if(data)
                {
                    if(type === "display"){
                        link = "<a href=\"/project/"+data+"\">"+row.project.name+"</a>";
                        return link;
                    }
                    return row.project.name;
                }
              }},
        { data: "comment", title: "Comment"},
        { data: "creator.get_full_name", title: "Creator"},

    ]
});
}

function load_sell_table(id,is_unique,permission_sell)
{
    $(".element-sell-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/sells?element='+id+'&format=datatables',
        "order": [[ 0, "desc" ]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          },
          {
              "targets": [1],
              "display": !is_unique
          }
        ],
        columns: [
            { data: "recording_date", title: "Date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
                { data: "quantity", title: "Quantity"},
                { data: "price", title: "Price"},
            { data: "location_source.id", title: "Source",
              render: function(data,type,row,meta){
              if(type === "display"){
                  link = "<a href=\"/location/"+row.location_source.id+"\">"+row.location_source.name+"</a>";
                  return link;
              }
              return row.location_source.name;
            }},
            { data: "comment", title: "Comment"},
            { data: "creator.get_full_name", title: "Creator"},

        ]
    });
}
function load_consume_table(id)
{
    $(".element-consume-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/consumes?element='+id+'&format=datatables',
        "order" : [[ 0, "desc" ]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          }
        ],
        columns: [
            { data: "recording_date", title: "Date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
              { data: "quantity", title: "Quantity"},
            { data: "location_source.id", title: "Source",
              render: function(data,type,row,meta){
              if(type === "display"){
                  link = "<a href=\"/location/"+row.location_source.id+"\">"+row.location_source.name+"</a>";
                  return link;
              }
              return row.location_source.name;
            }},
            { data: "comment", title: "Comment"},
            { data: "creator.get_full_name", title: "Creator"},
        ]
});
}

function load_reserve_table(id,is_unique,permission_useevent,permission_unuseevent)
{
    $(".element-reserve-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/reserves?element='+id+'&format=datatables',
        "order" : [[ 0, "desc" ]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          },
          {
              "targets": [1],
              "display": !is_unique
          }
        ],
        columns: [
            { data: "recording_date", title: "Date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
            { data: "quantity", title: "Quantity"},
            { data: "location_source.id", title: "Source",
              render: function(data,type,row,meta){
              if(type === "display"){
                  link = "<a href=\"/location/"+row.location_source.id+"\">"+row.location_source.name+"</a>";
                  return link;
              }
              return row.location_source.name;
            }},
            { data: "location_destination.id", title: "Destination",
              render: function(data,type,row,meta){
              if(type === "display"){
                  link = "<a href=\"/location/"+row.location_destination.id+"\">"+row.location_destination.name+"</a>";
                  return link;
              }
              return row.location_source.name;
            }},
            { data: "project.id", title: "Project",
              render: function(data,type,row,meta){
              if(type === "display"){
                  if(data)
                  {
                  link = "<a href=\"/project/"+data+"\">"+row.project.name+"</a>";
                  return link;
                  }
              }
              if(data)
              {
                  return row.project.name;
              }

            }},
            { data: "comment", title: "Comment"},
            { data: "creator.get_full_name", title: "Creator"},

        ]
});
}


function load_borrow_table(id,is_unique,permission_borrow,permission_return)
{


    $(".element-borrow-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/borrowings?element='+id+'&format=datatables',
        "order": [[ 7, "desc"],[ 0, "desc" ]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          },
          {
              "targets": [1],
              "display": !is_unique
          }
        ],
        columns: [
            { data: "recording_date", title: "Date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
                { data: "quantity", title: "Quantity"},
                { data: "scheduled_return_date", title: "Return before",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
            { data: "location_source.id", title: "Source",
              render: function(data,type,row,meta){
              if(type === "display"){
                  link = "<a href=\"/location/"+row.location_source.id+"\">"+row.location_source.name+"</a>";
                  return link;
              }
              return row.location_source.name;
            }},

            { data: "comment", title: "Comment"},
            { data: "creator.get_full_name", title: "By"},
            { data: "id", title: "Return",
              render: function(data,type,row,meta){
                  disabled = false;
                  if(!permission_return || row.return_event )
                  {
                      disabled = true;
                  }

                  button = '<button type="button" class="btn btn-primary event" href="#" data-event-type="return" data-element-id=" '+id+'" data-form="/formreturneventmodal?&borrow='+data+'" title="Return" ' ;
                  if(disabled)
                  {
                      button+=" disabled";
                  }
                  button+= ">Return</button>";
                  return button;
              }},
            { data: "return_event.recording_date", title: "Returned on",
            render: function (data, type, row, meta) {
                    ret = ""
                    if (type === 'display') {
                        if(data){
                             ret = convertISO8601ToHumanDay(data);
                             ret +=" ";
                        }
                        if(data>row.scheduled_return_date)
                             {
                                 ret+= "(LATE)";
                             }
                             else
                             {
                                 ret+= "(ON TIME)"
                             }

                        return ret;
                    } else {
                        return data;
                    }

                }},

            { data: "return_event.location_destination.id", title: "Destination",
              render: function(data,type,row,meta){
              if(type === "display"){
                  if(row.return_event)
                  {
                      link = "<a href=\"/location/"+data+"\">"+row.return_event.location_destination.name+"</a>";
                      return link;
                  }
                  return "-";

              }
              if(row.return_event)
              {
                  return row.return_event.location_destination.name;
              }
              return "";

            }},
            { data: "return_event.comment", title: "Comment"},
            { data: "return_event.creator.get_full_name", title: "Returned by"},


        ]
});

}

function load_incident_table(id,permission)
{
    $(".element-incident-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/incidents?element='+id+'&format=datatables',
        "order":[[0,"desc"]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          }
        ],
        columns: [
            { data: "recording_date", title: "Date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
            { data: "comment", title: "Comment"},
            { data: "get_new_status_display", title: "New status"},
            { data: "creator.get_full_name", title: "Creator"},
        ]
});
}

function load_maintenance_table(id,permission)
{

    $(".element-maintenance-table").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': "/api/v1/maintenances?element="+id+"&format=datatables",
        "order":[[4, "desc"],[0,"desc"]],
        "columnDefs": [
        {
            "targets": '_all',
            "defaultContent": ""
        }
        ],
        columns: [
            { data: "scheduled_date", title: "Scheduled date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return  convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "Undefined";
                        }
                    } else {
                        return data;
                    }
                }},
                { data: "is_done", title: "Is completed ?",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return "Yes";
                        }
                        else
                        {
                            return "No";
                        }
                    } else {
                        return data;
                    }
                }},
            { data: "comment", title: "Comment"},
            { data: "assignee.get_full_name", title: "Assignee"},
            { data: "completion_date", title: "Completion date",
            render: function (data, type, row, meta) {
                    if (type === 'display') {
                        if(data){
                            return convertISO8601ToHumanDay(data);
                        }
                        else
                        {
                            return "-";
                        }
                    } else {
                        return data;
                    }
                }},
                { data: "id", title: "Complete maintenance",
                render: function (data, type, row, meta) {
                    if (type === 'display') {

                    ret = '<button type="button" class="btn btn-primary event" href="#" data-element-id="'+id+'" data-event-type="maintenance" data-form="/formmaintenanceeventmodal/';
                    ret += row.id;
                    ret += '" title="Proceed"';
                    if(row.is_done)
                    {
                        ret+=" disabled";
                    }
                    ret+=" data-element-id="+id+" data-event-type=\"maintenance\">Proceed</button>";
                    return ret;
                    } else {
                        return data;
                    }
                }},
        ]
    });
}