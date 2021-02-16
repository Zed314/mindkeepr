$(document).ready(function() {
    function tree_search(parent)
    {
        var res = [parent];
        parent.children.forEach(elt => {
            gc = tree_search(elt);
            res = res.concat(gc);
        });

        return res;
    }
    function get_children_node_call(node_id){
        // do this as temporary as jstree is lazy loading and we need all
        // children for a node for our research
       // var children_array = null;
        return $.ajax({ url: "/api/v1/categoriesFull/"+node_id});
       // children_array.shift();
       // return children_array;
    }
    function get_children_locations_node_call(node_id){
        // do this as temporary as jstree is lazy loading and we need all
        // children for a node for our research
       // var children_array = null;
        return $.ajax({ url: "/api/v1/locationsFull/"+node_id});
       // children_array.shift();
       // return children_array;
    }
    //get_children_node("1");

    $("#jstree_category").jstree({
        "core": {
            "html_titles": true,
            /* To get children of nodes when selected */
            //"whole_node" :true,
            /*"keep_selected_style": true,
            "cascade":"down",*/

            "data": function(node, cb) {
                if (node.id === "#") {
                    id = "1"
                } else {
                    id = node.id
                }

                $.ajax({ url: "/api/v1/categories/" + id }).done(function(json) {
                    res = {
                        id: json["id"],
                        text: json["name"],
                        children: [],
                        state: "closed"
                    };
                    json.children.forEach(child => res["children"].push({ id: child["id"], text: child["name"], state: "closed", children: child["nb_children"] != 0 }));
                    cb(
                        [res]
                    )
                });
            },
        },
        "plugins": ["themes", "ui", "cookies", "crrm", "sort"]
    });
    $('#jstree_category').on("select_node.jstree", function(e, data) {
        // caution : lazy loading cause grandchildren not to be rendered (unless they were rendered previously)…
        id = data.node.id;

         get_children_node_call(id).done(function(json) {

            children_array = tree_search(json);
            search_string = "^("+id;
            children_array.forEach(child =>
                {
                    search_string+="|"+child.id;
                });
            search_string+=")$"


            $('#element-table').DataTable().column( 3 ).search(
                search_string , true,
                   false
               ).draw();
        });
        // children includes current node


    });
    /*
    $('#jstree_category').on('click', '.jstree-clicked', function () {
        $("#jstree_category").jstree().deselect_all(true);
        $('#element-table').DataTable().column( 3 ).search("").draw();
      });*/



    $("#jstree_locations").jstree({
        "core": {
            "html_titles": true,
            "data": function(node, cb) {
                if (node.id === "#") {
                    id = "1"
                } else {
                    id = node.id
                }

                $.ajax({ url: "/api/v1/locationsFull/" + id }).done(function(json) {
                    res = {
                        id: json["id"],
                        text: json["name"],
                        children: [],
                        state: "closed"
                    };
                    json.children.forEach(child => res["children"].push({ id: child["id"], text: child["name"], state: "closed", children: child["nb_children"] != 0 }));
                    cb(
                        [res]
                    )
                });
            },
        },
        "plugins": ["themes", "ui", "cookies", "crrm", "sort"]
    });
    $('#jstree_locations').on("select_node.jstree", function(e, data) {
        id = data.node.id;

        get_children_locations_node_call(id).done(function(json) {
            children_array = tree_search(json);
            search_string = "^("+id;
            children_array.forEach(child =>
                {
                    search_string+="|"+child.id;
                });
            search_string+=")$"


            $('#location-table').DataTable().column( 0 ).search(
                search_string , true,
                   false
               ).draw();
        });

       /* $('#location-table').DataTable().column( 3 ).search(

            '^'+id+'$' , true,
               false
           ).draw();*/
    });/*
    $('#jstree_locations').on('click', '.jstree-clicked', function () {
        $("#jstree_locations").jstree().deselect_all(true);
        $('#location-table').DataTable().column( 3 ).search("").draw();
      });*/



    console.log("My body is ready");

});