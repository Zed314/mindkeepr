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

        return $.ajax({ url: "/api/v1/categoriesFull/"+node_id+"/"});
    }
    function get_children_locations_node_call(node_id){
        return $.ajax({ url: "/api/v1/locationsFull/"+node_id}+"/");
    }


    $("#jstree_category").jstree({
        "core": {
            "html_titles": true,
            /* To get children of nodes when selected */
            "data": function(node, cb) {
                if (node.id === "#") {
                    id = "1"
                } else {
                    id = node.id
                }

                $.ajax({ url: "/api/v1/categories/" + id +"/" }).done(function(json) {
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
        // caution : lazy loading cause grandchildren not to be rendered (unless they were rendered previously)...
        id = data.node.id;

         get_children_node_call(id).done(function(json) {

            children_array = tree_search(json);
            search_string = "^("+id;
            children_array.forEach(child =>
                {
                    search_string+="|"+child.id;
                });
            search_string+=")$"
                // no cache due to sEcho used for keeping track of orders of requests.
            $('#element-table').DataTable().column( 7 ).search(
                search_string , true,
                   false
               ).draw();
        });

    });


    $("#jstree_locations").jstree({
        "core": {
            "html_titles": true,
            "data": function(node, cb) {
                if (node.id === "#") {
                    id = "1"
                } else {
                    id = node.id
                }

                $.ajax({ url: "/api/v1/locationsFull/" + id +"/"}).done(function(json) {
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

    });

    console.log("My body is ready ;)");

});