
$(document).on('hide.bs.modal',"#eventModal", function (evt) {
    // Assuming that an update just got completed
    if($(evt.target).data("element-id"))
    {
        console.log($(evt.target).data("element-id"));
        $(".element-"+$(evt.target).data("event-type")+"-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
        $(".element-stock-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
    }
});

$(document).on('hide.bs.modal',"#eventModal[data-event-type=return]", function (evt) {
    // Assuming that an update just got completed
    if($(evt.target).data("element-id"))
    {
        $(".element-borrow-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
        $(".element-stock-table[data-element-id="+$(evt.target).data("element-id")+"]").DataTable().rows().invalidate().draw();
    }
});

//
$(document).on('hide.bs.modal',"#eventModal", function (evt) {
    // Assuming that an update just got completed
    if($(evt.target).data("location-id"))
    {
        $(".location-stock-table[data-location-id="+$(evt.target).data("location-id")+"]").DataTable().rows().invalidate().draw();
    }
});

$(document).on('hide.bs.modal',"#eventModal", function (evt) {
    // Assuming that an update just got completed
    if($(evt.target).data("project-id"))
    {
        $(".project-stock-table[data-project-id="+$(evt.target).data("project-id")+"]").DataTable().rows().invalidate().draw();
    }
});

$(document).on("click",".event", function(ev) { // for each edit contact url
    ev.preventDefault(); // prevent navigation
    var url = $(this).data("form"); // get form from url

    $("#eventModal").load(url, function() { // load the url into the modal
        $(this).modal('show'); // display the modal on url load
    });
    var evttype=$(this).data("event-type");

    if(evttype === undefined)
    {
        evttype="";
    }
    var idelement=$(this).data("element-id");

    if(idelement === undefined)
    {
        idelement="";
    }

    var idlocation=$(this).data("location-id");
    if(idlocation === undefined)
    {
        idlocation ="";
    }
    var idproject=$(this).data("project-id");
    if(idproject === undefined)
    {
        idproject ="";
    }
    // To know which event modal got closed, to refresh the right data
    $("#eventModal").attr("data-event-type",evttype);
    $("#eventModal").attr("data-element-id",idelement);
    $("#eventModal").attr("data-location-id",idlocation);
    $("#eventModal").attr("data-project-id",idproject);
    return false; // prevent the click propagation
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


function load_borrow_table(id,is_unique,permission_borrow)
{
    $(".element-borrow-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/borrowings?element='+id+'&format=datatables',
       //"order": [[ 6, "desc"],[ 2, "desc" ]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          }
        ],
        columns: [
            { data: "id", title: "ID", visible:false},
            { data: "beneficiary.get_full_name", title: "For"},
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
                { data: "quantity", title: "Quantity", visible: !is_unique },
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
            },visible: !is_unique},
            //{ data: "comment", title: "Comment"},
         /*   { data: "return_event.recording_date", title: "Returned on",
            render: function (data, type, row, meta) {
                if (type === 'display') {

                if(data){
                    ret = convertISO8601ToHumanDay(data);
                    ret +=" ";
                    if(Date.parse(data)>Date.parse(row.scheduled_return_date))
                    {
                        ret+= "(LATE)";
                    }
                    else
                    {
                        ret+= "(ON TIME)"
                    }
                    return ret;
                }
                else
                {
                    disabled = false;
                    comment = ""
                    btn = ""
                    if(Date.now()>Date.parse(row.scheduled_return_date))
                    {
                        comment = "(Late !)";
                        btn = "btn-danger"
                    }
                    else
                    {
                        comment = "(On Time !)"
                        btn = "btn-success"
                    }
                    button = '<button type="button" class="btn '+btn+' event" href="#" data-event-type="return" data-element-id=" '+id+'" data-form="TODO&borrow='+row.id+'" title="Return '+comment+'" ' ;
                    if(disabled)
                    {
                        button+=" disabled";
                    }
                    button+= ">Return "+comment+"</button>";
                    return button;
                }

            }
            else
            {
                return data;
            }
                ret = ""
                if (type === 'display') {

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

            },visible: !is_unique},
            { data: "return_event.comment", title: "Feedback"},*/
        ]
});

}


function load_potentialborrow_table(id)
{


    $(".element-potentialborrow-table[data-element-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': '/api/v1/borrowings?element='+id+'&format=datatables',
        //"order": [[ 6, "desc"],[ 2, "desc" ]],
        "columnDefs": [
          {
              "targets": '_all',
              "defaultContent": ""
          }
        ],
        columns: [
            { data: "id", title: "ID", visible:false},
            { data: "beneficiary.get_full_name", title: "For"},
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
                { data: "scheduled_borrow_date", title: "From",
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
                { data: "scheduled_return_date", title: "To",
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
                { data: 'id', title: "Borrow",
                render: function(data, type, row, meta){
                    project = "";
                            if(row.project)
                            {
                                project = row.project.id;
                            }
                        if(type === 'display'){

                            button = '<button type="button" class="btn btn-primary event" href="#"  data-event-type="borrow" data-form="/formborroweventmodal?project='+project+'&potentialborrow='+data+'&beneficiary='+row.beneficiary.id+'" title="Borrow" ' ;
                            // TODO : check if free

                            button+= ">Borrow</button>";
                            return button;
                        }

                        return "";
                    }},

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

    $(".element-maintenance-table[data-element-id="+id+"]").DataTable({
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

function load_element_stock_table(id,
    permission_borrow,
    permission_use,
    permission_unuse,
    permission_consume,
    permission_sell,
    permission_move)
{
    load_location_stock_table(id,
        permission_borrow,
        permission_use,
        permission_unuse,
        permission_consume,
        permission_sell,
        permission_move,
        src="element")
}

function load_project_stock_table(id,
    permission_borrow,
    permission_use,
    permission_unuse,
    permission_consume,
    permission_sell,
    permission_move)
{
    load_location_stock_table(id,
        permission_borrow,
        permission_use,
        permission_unuse,
        permission_consume,
        permission_sell,
        permission_move,
        src="project")
}
function load_location_stock_table(id,
    permission_borrow,
    permission_use,
    permission_unuse,
    permission_consume,
    permission_sell,
    permission_move,
    src="location")
{
    var columntohide = {
        "location" : [3,4],
        "project" : [2,3,6,9],
        "element" : [0,3,5]
      };
    $("."+src+"-stock-table[data-"+src+"-id="+id+"]").DataTable({
        "dom": '<"top">rt<"bottom"lip><"clear">',
        'serverSide': true,
        "responsive": true,
        'ajax': "/api/v1/stocks?"+src+"="+id+"&format=datatables",
        //"order":[[4, "desc"],[0,"desc"]],
        "columnDefs": [
        {
            "targets": '_all',
            "defaultContent": ""
        },
        {
            "targets": columntohide[src],
            "visible": false,
        }
        ],
        columns: [
            //{ data: "id", title: "ID"},
            { data: "element", title: "Element",
            render: function (data, type, row, meta) {
                if (type === 'display') {
                ret = '<a href="/element/';
                ret += data.id;
                ret += "\"";
                ret+= ">"+data.name+"</a>";
                return ret;
                } else {
                    return data.name;
                }
            }},
            { data: "quantity", title: "Quantity"},
            { data: "project", title: "Project",
                render: function(data,type,row,meta){
                    if(!data)
                    {
                        return "-";
                    }
                    if (type === 'display') {
                    ret = '<a href="/project/';
                    ret += data.id;
                    ret += "\"";
                    ret+= ">"+data.name+"</a>";
                    return ret;
                    } else {
                        return data.name;
                    }
                }},
                {data:"status", title: "Status"},
                { data: "location", title: "Location",
                render: function(data,type,row,meta){
                    if (type === 'display') {
                    ret = '<a href="/location/';
                    ret += data.id;
                    ret += "\"";
                    ret+= ">"+data.name+"</a>";
                    return ret;
                    } else {
                        return data.name;
                    }
                }},
                {data:"element.type",title:"Type"},
                { data: 'id', title: "Borrow",
                render: function(data, type, row, meta){
                    project = "";
                            if(row.project)
                            {
                                project = row.project.id;
                            }
                        if(type === 'display'){

                            button = '<button type="button" class="btn btn-primary event" href="#" data-stock="'+data+'" data-event-type="borrow" data-'+src+'-id="'+id+'" data-form="/formborroweventmodal?stock='+data+'&project='+project+'" title="Borrow" ' ;
                            if(!permission_borrow || row.status!="FREE")
                            {
                                button+="disabled";
                            }
                            button+= ">Borrow</button>";
                            return button;
                        }

                        return "";
                    }},
              { data: 'id', title: "Reserve",
                render: function(data, type, row, meta){
                        if(type === 'display'){
                            button = "";
                            if(row.project)//if not reserved
                            {
                                button = '<button type="button" class="btn btn-primary event" href="#" data-'+src+'-id="'+id+'" data-event-type="unreserve" data-stock="'+data+'"  data-form="/formunuseeventmodal?stock='+data+'" title="Unreserve"'
                                if(!permission_unuse)
                                {
                                    button +=  "disabled";
                                }
                                button += '>Unreserve</button>';
                            }
                            else
                            {
                                button = '<button type="button" class="btn btn-primary event" href="#" data-stock="'+data+'" data-'+src+'-id="'+id+'" data-event-type="reserve" data-form="/formuseeventmodal?stock='+data+'" title="Reserve"'
                                if(!permission_use)
                                {
                                    button +=  "disabled";
                                }
                                button += '>Reserve</button>';
                            }
                            return button;
                        }

                        return "";
                    }},


                    { data: "id", title: "Consume",
                    render: function(data,type,row,meta){
                    if(type === 'display'){
                            button = '<button type="button" class="btn btn-primary event" href="#" data-stock="'+data+'" data-'+src+'-id="'+id+'" data-event-type="consume"  data-form="/formconsumeeventmodal?stock='+data+'" title="Consume"';
                            if(!permission_consume)
                            {
                                button +=  "disabled";
                            }
                            button += '>Consume</button>';

                            return button;
                        }

                        return "";
                    }},
                    { data: 'id', title: "Sell",
                    render: function(data, type, row, meta){
                        if(type === 'display'){
                            button = '<button type="button" class="btn btn-primary event" href="#" data-stock="'+data+'" data-event-type="sell" data-'+src+'-id="'+id+'" data-form="/formselleventmodal?stock='+data+'" title="Sell"';

                            if(row.status!="FREE" || !permission_sell)
                            {
                                button +=  "disabled";
                            }

                            button += '>Sell</button>';

                            return button;
                        }

                        return "";
                    }},
                    { data: 'id', title: "Move",
                    render: function(data, type, row, meta){
                        if(type === 'display'){
                            project = "";
                            if(row.project)
                            {
                                project = row.project.id;
                            }
                            button = '<button type="button" class="btn btn-primary event" href="#" data-stock="'+data+'" data-event-type="move" data-'+src+'-id="'+id+'" data-form="/formmoveeventmodal?stock='+data+'&project='+project+'" title="Move"';
                            if(!permission_move)
                            {
                                button +=  "disabled";
                            }

                            button += '>Move</button>';

                            return button;
                        }

                        return "";
                    }},
        ]
    });
}